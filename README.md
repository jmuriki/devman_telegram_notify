# devman_telegram_notify

Данный скрипт помогает студенту Devman автоматизировать процесс осведомления о статусе учебных работ, отправленных им на проверку.
Уведомдения будут приходить в чат с telegram ботом.

## Установка

Должен быть установлен python3.
Затем используйте pip (или pip3, если есть конфликт с python2) для установки зависимостей:

```
pip install -r requirements.txt
```

или

```
pip3 install -r requirements.txt
```

Рекомендуется использовать venv для изоляции проекта.


## Ключи и параметры

Сохраните ключи/токены в `.env` файл в директорию проекта в следующем формате:

```
KEY=вместо этого текста вставьте ключ
```

```
DEVMAN_TOKEN=вставьте Devman API Authorization Token
```
Узнать свой Devman API Authorization Token можно по [ссылке](https://dvmn.org/api/docs/).

```
TELEGRAM_TOKEN=вставьте Telegram API token
```
Для получения Telegram API token создайте бота c помощью [BotFather](https://telegram.me/BotFather).

```
TELEGRAM_CHAT_ID=вставьте Telegram Chat ID
```
Чтобы узнать свой Telegram Chat ID, воспользуйтесь [userinfobot](https://telegram.me/userinfobot).


## Запуск


### devman_telegram_notify.py

Находясь в директории проекта, откройте с помощью python3 файл `devman_telegram_notify.py`

```
python3 devman_telegram_notify.py
```

В случае успеха, ожидайте уведомлений о статусе работ в telegram чате с вашим ботом.


### Docker-контейнер

Должен быть установлен docker. Находясь в директории, содержащей актуальный файл .env, введите команду:
```
docker run --restart always -d --env-file .env jmuriki/devman-telegram-notify
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков https://dvmn.org/.
