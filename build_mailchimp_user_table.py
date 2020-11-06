"""
This should only be run ONCE unless the project needs to be created from scratch.
Used to create the initial Mailchimp subscriber table
11-5-2020
"""

from pathlib import Path
from rc.db.sqlite_3.oop import Database

HOME_DIR = Path(__file__).resolve().parent


def build_mailchimp_users_table(db):
    db.run_script("""DROP TABLE IF EXISTS 'user';""")
    create_query = \
        """CREATE TABLE user (id INTEGER PRIMARY KEY, email_id TEXT, email TEXT NOT NULL UNIQUE, 
        status TEXT, rating INTEGER, created DATE, updated DATE, last_open DATE)"""
    db.create_table(create_query)


if __name__ == '__main__':
    database = Database(HOME_DIR.joinpath('db/test.db'))
    build_mailchimp_users_table(database)
