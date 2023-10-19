Для запуска необходимо создать файл .env в папке проекта и задать следующие переменные:

Данные для доступа к БД:

- DB_NAME=
- DB_USERNAME=
- DB_PASSWORD=

Токен телеграм бота

- TG_API=


Ссылки для проверки:
- /habit/
- /habit/1/
- /habit/1/delete/
- /habit/1/update/
- /habit/create/
- /users/token/
- /users/register/

_Для запуска celery:_

```
celery -A config worker --loglevel=info
```

_Для запуска django-celery-beat:_

```
celery -A config beat --loglevel=info
```

_Для запуска приложения:_

```
python3 manage.py runserver
```

_Для запуска телеграм-бота и синхронизации аккаунтов:_

```
python3 manage.py bot
```

_Для тестирования проекта запустить команду:_

```
python3 manage.py test
```

_Для запуска подсчета покрытия и вывода отчета запустить команды:_

```
coverage run --source='.' manage.py test

coverage report
```

_Для создания образа из Dockerfile и запуска контейнера:_

```
docker compose build
docker compose up
```


Документация проекта: http://127.0.0.1:8000/swagger/