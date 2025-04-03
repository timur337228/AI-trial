import fitz
import pytesseract
from PIL import Image
import tempfile
import cv2
import numpy as np
import re
from pathlib import Path
from difflib import get_close_matches
from dotenv import load_dotenv, find_dotenv
from backend.config import APPENDIX_ITEMS, LEGAL_TERMS, settings, BASE_DIR


pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH


def is_scanned_page(page) -> bool:
    text = page.get_text()
    return len(text.strip()) < 50


def enhance_image_quality(image):
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=1)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    img = clahe.apply(img)
    img = cv2.adaptiveThreshold(img, 255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 15, 4)
    return Image.fromarray(img)


def correct_spelling(word: str) -> str:
    if not word:
        return word

    matches = get_close_matches(word.lower(), [term.lower() for term in LEGAL_TERMS], n=1, cutoff=0.7)

    if not matches:
        return word

    original_term = next((term for term in LEGAL_TERMS if term.lower() == matches[0]), None)

    if original_term:
        if word.isupper():
            return original_term.upper()
        elif word.istitle():
            return original_term.capitalize()
        else:
            return original_term.lower()

    return word


def process_paragraphs(text: str) -> str:
    start_phrase = "ЗАЯВЛЕНИЕ о выдаче судебного приказа"
    parts = text.split(start_phrase)

    if len(parts) > 1:
        before = parts[0]
        after = parts[1]

        after_processed = re.sub(r'(\n{2,})', '\n\n', after)
        return f"{before}{start_phrase}\n\n{after_processed}"

    return text


def extract_columned_text(page) -> str:
    width = page.rect.width
    column_threshold = width * 0.2
    blocks = page.get_text("blocks")
    blocks = [b for b in blocks if b[6] == 0]
    blocks.sort(key=lambda b: (b[1], b[0]))

    if not blocks:
        return ""

    columns = []
    current_column = [blocks[0]]
    prev_x1 = blocks[0][2]

    for block in blocks[1:]:
        x0 = block[0]
        if x0 - prev_x1 > column_threshold:
            columns.append(current_column)
            current_column = [block]
            prev_x1 = block[2]
        else:
            current_column.append(block)
            prev_x1 = max(prev_x1, block[2])
    columns.append(current_column)

    column_texts = []
    for col in columns:
        col_sorted = sorted(col, key=lambda b: b[1])
        col_lines = []
        for b in col_sorted:
            lines = b[4].strip().split('\n')
            col_lines.extend(lines)
        column_text = '\n'.join(col_lines)
        column_texts.append(column_text.strip())

    return '\n\n'.join(column_texts)


def replace_appendix_items(text: str, threshold: float = 0.7) -> str:
    def find_best_match(sentence):
        return get_close_matches(
            sentence.lower(),
            [item.lower() for item in APPENDIX_ITEMS],
            n=1,
            cutoff=threshold
        )

    sentences = re.split(r'(?<!\w\.\w.)(?<![A-ZА-Я][a-zа-я]\.)(?<=\.|\?|\!)\s+', text)
    result = []

    for sent in sentences:
        clean_sent = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9\s]', '', sent.strip()).lower()
        matches = find_best_match(clean_sent)

        if matches:
            original = next((item for item in APPENDIX_ITEMS
                             if item.lower() == matches[0]), None)
            if original:
                result.append(original)
                continue

        result.append(sent)

    return ' '.join(result)


def clean_text(text: str) -> str:
    words = re.findall(r'\b\w+\b', text)
    corrected = [correct_spelling(word) for word in words]
    text = ' '.join(corrected)
    text = replace_appendix_items(text)

    text = re.sub(r'-\s+(\w)', r'\1', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r'\b\w\b', '', text)
    text = re.sub(r'\s+', ' ', text)

    text = process_paragraphs(text)

    return text.strip()


def pdf_to_text(filename: str, language: str = 'rus+eng') -> str:
    pdf_path = BASE_DIR / 'static' / filename

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    text = []
    pdf_document = fitz.open(pdf_path)

    try:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)

            if not is_scanned_page(page):
                page_text = extract_columned_text(page)
                text.append(clean_text(page_text))
                continue

            with tempfile.TemporaryDirectory() as temp_dir:
                pix = page.get_pixmap(dpi=300, colorspace="rgb", alpha=False)
                img_path = Path(temp_dir) / f"page_{page_num + 1}.png"
                pix.save(img_path)

                img = Image.open(img_path)
                enhanced_img = enhance_image_quality(img)

                custom_config = r'''
                    --oem 3 --psm 3 
                    -c tessedit_char_whitelist=... 
                    preserve_interword_spaces=1
                '''

                page_text = pytesseract.image_to_string(
                    enhanced_img,
                    lang=language,
                    config=custom_config
                )
                text.append(clean_text(page_text))

        return "\n\n".join(text)
    except Exception as e:
        raise RuntimeError(f"Error processing PDF: {str(e)}")
    finally:
        pdf_document.close()
