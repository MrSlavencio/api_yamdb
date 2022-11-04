import pandas as pd
import os
import sqlite3


db_path = os.path.join(os.getcwd(), 'db.sqlite3')

sql_conn = sqlite3.connect(db_path)

uploading_tables = {
    'category.csv': 'reviews_categories',
    #'comments.csv': '',
    'genre_title.csv': 'reviews_genretitle',
    'genre.csv': 'reviews_genres',
    #'review.csv': '',
    'titles.csv': 'reviews_titles',
    #'users.csv': '',
}


def clean_db():
    for value in uploading_tables.values():
        cursor = sql_conn.cursor()
        cursor.executescript(f'DELETE FROM {value}')


def upload_data():
    clean_db()
    for key, value in uploading_tables.items():
        filepath = os.path.join(os.getcwd(), 'static', 'data', key)
        df = pd.read_csv(filepath)
        df.to_sql(value, sql_conn, if_exists='append', index=False)


if __name__ == '__main__':
    clean_db()
    upload_data()
