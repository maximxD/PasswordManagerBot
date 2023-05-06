START_CMD = 'start'
SET_CMD = 'set'
GET_CMD = 'get'
DELETE_CMD = 'del'
HELP_CMD = 'help'
COMMANDS = [SET_CMD, GET_CMD, DELETE_CMD, HELP_CMD]

START_MSG = f'Я бот - менеджер паролей.\n' \
            f'Чтобы узнать, мои команды, напишите /{HELP_CMD}.'
INCORRECT_SET_SERVICE_FORMAT_MSG = 'Некорректный формат ввода.\n' \
                                   'Введите /set *<сервис> <логин> <пароль>*.'

INCORRECT_GET_SERVICE_FORMAT_MSG = 'Некорректный формат ввода.\n' \
                                   'Введите /get *<сервис>*.'

INCORRECT_DELETE_SERVICE_FORMAT_MSG = 'Некорректный формат ввода.\n' \
                                      'Введите /del *<сервис>*.'
HELP_MSG = 'Доступные команды:\n' \
           '/set *<сервис> <логин> <пароль>* - добавить/обновить данные для сервиса.\n' \
           '/get *<сервис>* - получить данные для сервиса.\n' \
           '/del *<сервис>* - удалить данные для сервиса.\n' \
           '/help - вывести список допустимых команд.'

YES_MSG = 'Да'
NO_MSG = 'Нет'

OVERWRITE_SERVICE_ACCEPTED_CB = 'overwrite_accepted'
OVERWRITE_SERVICE_CANCELED_CB = 'overwrite_canceled'
DELETE_SERVICE_ACCEPTED_CB = 'delete_accepted'
DELETE_SERVICE_CANCELED_CB = 'delete_canceled'


def there_was_service_data_msg(service_name: str):
    return f'Здесь были данные для *{service_name}*'


def service_deleted_msg(service_name: str):
    return f'Данные для *{service_name}* удалены.'


def delete_service_cancel_msg(service_name: str):
    return f'Удаления данных для *{service_name}* отменено.'


def service_delete_confirm_msg(service_name: str):
    return f'Вы уверены, что хотите удалить данные для *{service_name}*?'


def service_is_not_exists_msg(service_name: str):
    return f'Данные для *{service_name}* не найдены.'


def service_data_msg(service_name: str, login: str, password: str, delete_delay: int):
    return f'Данные для *{service_name}*\n' \
           f'Логин: `{login}`\n' \
           f'Пароль: `{password}`\n' \
           f'Чтобы скопировать логин/пароль, нажмите на него.\n' \
           f'Это сообщение будет автоматически удалено через {delete_delay} минуту.'


def overwrite_service_cancel_msg(service_name: str):
    return f'Данные для *{service_name}* не перезаписаны.'


def service_already_exists_msg(service_name: str) -> str:
    return f'Данные для *{service_name}* были сохранены ранее.\n' \
           f'Перезаписать их?'


def set_service_success_msg(service_name: str) -> str:
    return f'Логин и пароль для *{service_name}* успешно сохранен.'
