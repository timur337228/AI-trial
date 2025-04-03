from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
BASE_DIR = Path(__file__ + r'\backend').parent.parent

APPENDIX_ITEMS = [
    "Расчёт задолженности",
    "Подтверждение перевода денежных средств должнику",
    "Распечатка CMC сообщений",
    "Индивидуальные условия по договору",
    "Выдержка из договора цессии",
    "Выписка из уступаемых прав по договору цессии",
    "Учредительные документы взыскателя",
    "Платёжное поручение об оплате государственной пошлины",
    "Копия договора управления",
    "Копия выписки лицевого счета",
    "Копия свидетельства о гос. регистрации права",
    "Выписка из ЕГРЮЛ",
    "Доверенность",
    "Платежное поручение об оплате гос пошлины",
    "Уведомление об уступке права в требований"
]

MAIN_TERMS = [
    'благовещенск', 'амурская', 'область', 'снилс', 'гос', 'пошлина', 'егрюл',
    'ооо', 'общество', 'ограниченной', 'ответственностью', 'судебный', 'приказ',
    'заявление', 'взыскание', 'должник', 'истец', 'ответчик', 'регистрация',
    'собственник', 'жилищный', 'коммунальные', 'услуги', 'договор', 'управление',
    'многоквартирный', 'дом', 'платеж', 'задолженность', 'пени', 'расчет',
    'свидетельство', 'выписка', 'лицевой', 'счет', 'реквизиты', 'копия',
    'доверенность', 'платежное', 'поручение', 'госпошлина', 'подпись',
    'представитель', 'законодательство', 'кодекс', 'российская', 'федерация',
    'требование', 'обязанность', 'срок', 'оплата', 'просрочка', 'взыскатель',
    'документ', 'требования', 'суд', 'запрос', 'орган', 'государственный',
    'регистрации', 'право', 'собственности', 'жилое', 'помещение', 'адрес',
    'дата', 'рождения', 'паспорт', 'идентификатор', 'инн', 'кпп', 'огрн',
    'банковский', 'расчетный', 'счет', 'период', 'сумма', 'рубль', 'квартира',
    'долг', 'погашение', 'принудительное', 'взыскание', 'исполнение',
    'обязательство', 'закон', 'статья', 'пункт', 'основание', 'решение',
    'собрание', 'собственников', 'управляющая', 'организация', 'доказательство',
    'приложение', 'документы', 'подтверждение', 'требовать', 'исковое',
    'заявление', 'прошение', 'ходатайство', 'судья', 'заседание', 'производство',
    'исполнительный', 'лист', 'арбитраж', 'инстанция', 'жалоба', 'апелляция'
]

LEGAL_TERMS = MAIN_TERMS + APPENDIX_ITEMS

NAME_COOKIE_AUTH = 'session_id'
BASE_PARAM_COOKIE = {"path": "/",
                     "httponly": True,
                     "secure": False,
                     "samesite": "lax", }


class BASE_JWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'


class AuthJWT(BASE_JWT):
    access_token_expire_minutes: int = 1
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    BASE_URL: str = 'http://localhost:3000'
    BASE_BACKEND_URL: str = "http://localhost:8080"
    AUTH_JWT: AuthJWT = AuthJWT()
    TESSERACT_PATH: str
    KEY_OPENROUTER: str
    OPENAI_API_KEY: str = ''
    EMAIL: str
    SMTP: str
    EMAIL_SALT: str
    SESSION_SECRET: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DATABASE_URL_psycopg(self):
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='./.env')


settings = Settings()
