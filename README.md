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
