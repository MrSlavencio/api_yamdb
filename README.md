# YaMDb

Групповой проект по созданию сервиса по сбору отзывов пользователей на произведения.

## Как развернуть проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/MrSlavencio/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Выполнить миграции:

```
python3 manage.py migrate
```

## Как наполнить SQL-БД тестовыми данными
В командной строке выполните команду:

```
python manage.py upload_demo_data --u
```

Чтобы очистить таблицы проекта от данных, выполните команду:

```
python manage.py upload_demo_data --c
```

## Алгоритм регистрации пользователей

- Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
- YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
- Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
- При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

### Пример регистрации
#### POST-запрос на `/api/v1/auth/signup/`
```json
{
    "email": "user@mail.ru",
    "username": "user"
}
```
#### POST-запрос на `/api/v1/auth/token/`
```json
{
    "username": "user",
    "confirmation_code": "65r-4913ecce962f48e05657"
}
```
#### PATCH-запрос на `/api/v1/users/me/`
Для доступа используем токен полученный в результате предыдущего запроса.
```json
{
    "username": "user",
    "email": "new-user-mail@mail.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Обычный пользователь. Не умею менять свою роль :(",
}
```

### Пример запросов к API
#### GET-запрос на `/api/v1/titles/{title_id}/reviews/`
Получение списка всех отзывов
#### POST-запрос на `/api/v1/titles/{title_id}/reviews/`
Добавление нового отзыва (доступно авторизированным пользователям)
```json
{
"text": "perfecto!",
"score": 1
}
```
#### PATCH-запрос на `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`
Частичное обновление комментария к отзыву по id (доступно только автору комментария, администратору или модератору)
```json
{
"text": "это просто прекрасно!"
}
```
#### GET-запрос на `/api/v1/titles/`
Получение списка всех произведений

## Используемые библиотеки

В проекте используются следующие зависимости:
* requests==2.26.0
* django==2.2.16
* djangorestframework==3.12.4
* PyJWT==2.1.0
* pytest==6.2.4
* pytest-django==4.4.0
* pytest-pythonpath==0.7.3
* pandas==1.3.5
* djangorestframework-simplejwt==4.7.2
* django-filter==2.4.0

## Rest-API

Документацию по API Вы можете прочитать, запустив проект(```
python3 manage.py runserver
```) по ссылке ```/redoc/```

## Об авторах

Авторы проекта - студенты когорты 44 факультета Бэкенд разработки Яндекс-практикума.</br>
* **Кобзев Вячеслав** - тимлид [*Git - MrSlavencio*](https://github.com/MrSlavencio "MrSlavencio")
* **Осипенков Денис** - участник [*Git - DannyDies*](https://github.com/DannyDies "DannyDies")
* **Костюнина Светлана** - участник [*Git - Kostiunina*](https://github.com/Kostiunina "Kostiunina")
