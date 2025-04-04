from openai import AsyncOpenAI
import asyncio
from backend.config import settings

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.KEY_OPENROUTER,
)


def get_text_to_ai(message):
    return f"""Извлеки из текста нужную информацию, и отправь ее в виде: ключ значение новая строка. вот все ключи: Наименование суда, Взыскатель, Юридический адрес
взыскателя. Телефон взыскателя. ИНН взыскателя,
Адрес взыскателя для корреспонденции, Должник,
Адрес должника, Дата рождения должника, Место
рождения лица, Паспорт серия должника, Паспорт
номер должника, Паспорт дата выдачи должника,
Паспорт орган выдавший паспорт должника, ИНН
должника, СНИЛС должника, Сущность взыскания,
Адрес взыскания, Пропорциональный порядок
взыскания, Доли взыскания, Солидарный порядок
взыскания, Наименование услуги, Долг, Сумма долга,
Начало периода долга, Конец периода долга, Пеня,
Сумма пени, Начало периода пени, Конец периода
пени, Процент, Сумма по процентам, Начало периода
по процентам, Конец периода по процентам, Штраф,
Сумма штрафа, Начало периода штрафа, Конец
периода штрафа, Иное взыскание Сумма иного
взыскания, Начало периода иного взыскания, Конец
периода иного взыскания, Общая сумма взыскания,
Госпошлина, Приложение\n
Вот текст, из которого нужно извлечь информацию: {message}"""


async def get_completion(user_input: str, model: str = "deepseek/deepseek-r1:free", temperature: float = 1,
                         top_p: float = 0.5, extra_body: dict = {}):
    completion = await client.chat.completions.create(
        # extra_headers={
        #     "HTTP-Referer": "<YOUR_SITE_URL>",
        #     "X-Title": "<YOUR_SITE_NAME>",
        # },
        extra_body=extra_body,
        model=model,
        temperature=temperature,
        top_p=top_p,
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    return completion.choices[0].message.content


async def get_completion_stream(message: str, is_think: bool = False, is_search: bool = False,
                                model: str = "deepseek/deepseek-r1:free", temperature: float = 1,
                                top_p: float = 0.5, ):
    # if model == "deepseek":
    #     if is_think:
    #         model = 'deepseek/deepseek-r1:free'
    #     else:
    #         model = 'deepseek/deepseek-chat:free'
    messages = [{"role": "user",
                 "content": get_text_to_ai(message)}]
    stream = await client.chat.completions.create(
        # extra_headers={
        #     "HTTP-Referer": "<YOUR_SITE_URL>",
        #     "X-Title": "<YOUR_SITE_NAME>",
        # },
        model=model,
        temperature=temperature,
        top_p=top_p,
        messages=messages,
        stream=True
    )

    async for chunk in stream:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content is not None:
            yield chunk_content
