# Бот для рассылки замен ВГПГК

## Функциональность

*   **Подписка на рассылку:** Пользователь может подписаться на рассылку замен, используя команду /sub.
*   **Отписка от рассылки:** Пользователь может отписаться от рассылки, чтобы прекратить получение уведомлений /unsub.
*   **Автоматическая проверка замен:** Бот раз в 30 минут проверяет сайт колледжа на наличие новых замен.
*   **Отправка уведомлений:** При обнаружении новых замен, бот отправляет сообщение с заменами для группы всем подписанным пользователям.
*   **Отображение текущих замен:** Пользователь может запросить текущий список замен в любой момент /zam.

## Технологии

*   **Python:** Основной язык программирования.
*   **aiogram:** Библиотека для работы с Telegram Bot API.
*   **Beautiful Soup 4 (bs4):** Библиотека для парсинга HTML-кода сайта колледжа.
*   **aiohttp:** Библиотека для отправки HTTP-запросов к сайту колледжа.
*   **asyncio:** Библиотека для планирования периодических задач.
*   **MongoDB:** Для хранения информации о подписанных пользователях.
*   **Redis:** Для кеширования замен групп и проверки обновлений на сайте коллледжа




## Установка



1.  **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/Aeksar/replace_vgpgk_tgbot.git
    ```

2.  **Настройте файлы `.env` и  `mongo.env` в корневой директории:**

    Файл`.env`:

    ```
    TELEGRAM_BOT_TOKEN=[ваш токен бота]
    R_PORT= [порт редиса]
    R_HOST= [хост редиса]
    R_DB= [База данных в редисе]
    
    MONGO_URL=[url базы данных в монго]
    ```

    Фалй`mongo.env`:

    ```
    MONGO_INITDB_ROOT_USERNAME=[имя пользователя]
    
    MONGO_INITDB_ROOT_PASSWORD=[пароль]
    ```

3. **Соберите контейнер**

   ```bash
    docker compose up --build
    ```
    


