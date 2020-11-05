"""
Used to create the initial Mailchimp subscriber table

explore this: https://mailchimp.com/developer/api/transactional/exports/export-activity-history/

pip install git+https://github.com/mailchimp/mailchimp-marketing-python.git
11-5-2020
"""
import csv
from pathlib import Path
from rc.db.sqlite_3.oop import Database

HOME_DIR = Path(__file__).resolve().parent


def build_user_table(database):
    db = Database(database)


def main():
    build_user_table(database=HOME_DIR.joinpath('db/test.db'))


if __name__ == '__main__':
    main()
