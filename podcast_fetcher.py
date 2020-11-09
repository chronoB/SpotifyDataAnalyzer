import os
import sqlite3
import sys
from sqlite3 import Error
from string import ascii_lowercase

import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def create_connection(db_file):
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


def create_table(conn, create_table_sql):
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


def create_podcast(conn, podcast):
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


def populateDatabase(letter, language="de"):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = spotify.search(
        q="shows:" + letter, type="show", limit=50, market=language
    )

    for show in results["shows"]["items"]:
        create_podcast(conn, show["name"])

    while results["shows"]["next"]:
        for show in results["shows"]["items"]:
            create_podcast(conn, show["name"])
        results = spotify.next(results["shows"])


if __name__ == "__main__":
    try:
        from dotenv import load_dotenv

        load_dotenv("")
        if not os.getenv("SPOTIPY_CLIENT_ID") or not os.getenv("SPOTIPY_CLIENT_SECRET"):
            print(
                "ERROR: Environment variables for spotipy not set. See https://spotipy.readthedocs.io/en/2.16.1/ for more details. Use .env file."
            )
            sys.exit(1)
    except ImportError as e:
        print(e)
        sys.exit(1)

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

            print("Populating database for letter: " + letter)
            if len(sys.argv) > 1:
                language = sys.argv[1]
                populateDatabase(letter, language)
            else:
                populateDatabase(letter)

    else:
        print("Error! cannot create the database connection.")

    if conn:
        conn.close()
