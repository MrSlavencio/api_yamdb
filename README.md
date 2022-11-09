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
