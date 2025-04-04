## Установка проекта

Добавление .env файла

![.env.png](img_to_readme%2F.env.png)

TESSERACT_PATH=Путь к tesseract

KEY_OPENROUTER=ключ к API OPENROUTER

OPENAI_API_KEY='' Оставьте пустым, это обязательный параметр для библиотеки OpenAI

EMAIL=почта
SMTP=SMTP ключ для gmail

EMAIL_SALT=соль ждя шифрования token для email, генерируется с помощью py-secrets или openSSL

SESSION_SECRET=Для шифрования сессии, генерируется с помощью py-secrets или openSSL

DB_HOST=host postgres

DB_PORT=port postgres

DB_USER=user postgres

DB_PASSWORD=password postgres

DB_NAME=name postgres


## Добавьте приватный и публичный ключ для JWT в папку certs

![img.png](img_to_readme/cert.png)

это можно сделать с помощью OpenSSL
-----BEGIN PRIVATE KEY-----
-----BEGIN PUBLIC KEY-----

## В фронтенде нужно будет добавить серфитикаты: 

![img.png](img_to_readme/img.png)

-----BEGIN CERTIFICATE-----
-----BEGIN PRIVATE KEY-----