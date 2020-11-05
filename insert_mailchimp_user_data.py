"""
Insert data from a csv file into the Mailchimp 'user' table. Used for both updating and creating the table.
Existing users are ignored when updating.
11-5-2020
"""
import csv
from pathlib import Path
from rc.db.sqlite_3 import oop
from rc.api.utils import get_md5_hash, get_date_from_timestamp

HOME_DIR = Path(__file__).resolve().parent


def get_subscriber_email_set(db):
    """
    Return a set of Mailchimp subscribers from the 'user' table.
    :param db: database OOP object
    :return: set
    """
    email_query = """SELECT email FROM user WHERE status = 'subscribed';"""
    fetchall_object = db.fetch(email_query)
    return {item['email'] for item in fetchall_object}


def read_csv(csv_file, subscriber_set):
    """
    Yield objects from csv file.
    :param subscriber_set: a set of subscribers retrieved from the Mailchimp 'user' table.
    :param csv_file:
    Note: subscriber_set will be empty the first time the 'user' table is created
    :yield: order dict from csv.DictReader()
    """
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row['Email Address']
            if email not in subscriber_set:
                email_id = get_md5_hash(email)
                status = 'subscribed'
                rating = int(row['MEMBER_RATING'])
                created = get_date_from_timestamp(row['OPTIN_TIME'])
                updated = get_date_from_timestamp(row['LAST_CHANGED'])
                yield email_id, email, status, rating, created, updated


def insert_user_data(db, csv_file, subscriber_set):
    """
    Insert user data from a Mailchimp exported csv into the 'user' table.
    :param csv_file: path to a csv file with Mailchimp subscriber data.
    :param subscriber_set: a set of subscribers retrieved from the Mailchimp 'user' table. Passed to read_csv().
    :param db: database OOP object
    :return: none
    """
    query = """INSERT INTO user (email_id, email, status, rating, created, updated) VALUES(?,?,?,?,?,?);"""
    rowcount = db.insert_many(query, read_csv(csv_file, subscriber_set))
    print(f"Added {rowcount} rows to Mailchimp 'user' table.")


if __name__ == '__main__':
    database = oop.Database(HOME_DIR.joinpath('db/test.db'))
    csv_data = HOME_DIR.joinpath('data/subscribers/subscribed_segment_export.csv')
    email_set = get_subscriber_email_set(database)
    insert_user_data(database, csv_data, email_set)
