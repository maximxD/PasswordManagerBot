# Профильное задание: Разработчик системы кластеризации Tarantool
### Запуск бота:
* #### Создать `.env` файл в корне проекта вида:
```
POSTGRES_DB=password_bot_db
POSTGRES_USER=password_bot_user
POSTGRES_PASSWORD=123123
POSTGRES_HOST=postgresql
POSTGRES_PORT=5432

PASSWORD_MANAGER_BOT_TOKEN=<telegram_bot_token>
```
* #### Выполнить `docker-compose up`
### Доступные команды:
* #### /set <service_name> \<login> \<password> - добавить/обновить данные для сервиса.
* #### /get <service_name> - получить данные для сервиса.
* #### /del <service_name> - удалить данные для сервиса.
* #### /help - вывести доступные команды