import os
import sqlite3
import sys
from sqlite3 import Connection, Error
from string import ascii_lowercase
from typing import Optional

import requests


def create_connection(db_file: str) -> Optional[Connection]:
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn: Connection, create_table_sql: str) -> None:
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_podcast(conn: Connection, podcast: str) -> int:
    """
    Create a new podcast into the podcasts table
    :param conn:
    :param podcast:
    :return: podcast id
    """
    sql = """ INSERT INTO podcasts(name)
              VALUES(?) """
    cur = conn.cursor()
    try:
        cur.execute(sql, [podcast])
        conn.commit()
    except Exception as e:
        if not "UNIQUE constraint failed" in str(e):
            print("Error:")
            print(e)

    return cur.lastrowid


def populateDatabase(url: str, conn: Connection) -> None:
    if isinstance(BEARER_TOKEN, str):
        headers = {"Authorization": "Bearer " + BEARER_TOKEN}
    else:
        raise Exception("Bearer token not defined")
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        data = r.json()
        for show in data["shows"]["items"]:
            create_podcast(conn, show["name"])
        if data["shows"]["next"]:
            populateDatabase(data["shows"]["next"], conn)
    elif r.status_code == 401:
        print("Error while requesting:")
        print(r.text)


if __name__ == "__main__":

    try:
        from dotenv import load_dotenv

        load_dotenv("")
        BEARER_TOKEN: Optional[str] = os.getenv("BEARER_TOKEN")
    except ImportError as e:
        print(e)
        exit()

    database_path = r"./data/podcasts.db"
    sql_create_podcasts_table = """ CREATE TABLE IF NOT EXISTS podcasts (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL UNIQUE
                                    ); """
    conn = create_connection(database_path)

    # create tables
    if conn is not None:
        # create podcast table
        create_table(conn, sql_create_podcasts_table)

        for letter in ascii_lowercase:
            url = "https://api.spotify.com/v1/search?type=show&limit=50&q=" + letter

            if len(sys.argv) > 1:
                language = sys.argv[1]
                url + "&market=" + language

            print("Populating database for letter: " + letter)
            populateDatabase(url, conn)

    else:
        print("Error! cannot create the database connection.")

    if conn:
        conn.close()
