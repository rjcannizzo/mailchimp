"""
Insert data from a csv file into the Mailchimp user table.
11-5-2020
"""
import csv
from pathlib import Path
from rc.db.sqlite_3 import oop
from rc.api.utils import get_md5_hash, get_date_from_timestamp

HOME_DIR = Path(__file__).resolve().parent


def read_csv(csv_file):
    """
    Yield objects from csv file.
    :param csv_file
    :yield: order dict from csv.DictReader()
    """
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row['Email Address']
            email_id = get_md5_hash(email)
            status = 'subscribed'
            rating = int(row['MEMBER_RATING'])
            created = get_date_from_timestamp(row['OPTIN_TIME'])
            updated = get_date_from_timestamp(row['LAST_CHANGED'])
            yield email_id, email, status, rating, created, updated


def insert_user_data(db, csv_file):
    """
    Insert user date from API into the 'user' table.
    Notes:
        This was created to use API output but batch processing is poorly documented
        7-28-2020: I cannot get mailchimp API batch processing to work
        Will need to use csv files until resolved
    :param csv_file:
    :param db: database to use
    :return: none
    """
    query = """INSERT INTO user (email_id, email, status, rating, created, updated) VALUES(?,?,?,?,?,?);"""
    db.insert_many(query, read_csv(csv_file))


if __name__ == '__main__':
    database = oop.Database(HOME_DIR.joinpath('db/test.db'))
    csv_data = HOME_DIR.joinpath('data/subscribers/subscribed_segment_export.csv')
    insert_user_data(database, csv_data)
