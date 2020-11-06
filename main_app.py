"""
Purpose:
    To generate a list of emails to archive or unsubscribe.
    We combine two criteria for this:
        - subscribers who have not opened an email in a while (arbitrary)
        - subscribers who have spent less than an arbitrary threshold (probably $0)
Methods:
    build_sales_table():
        build the Shopify sales table (built from a fresh Customer export)
        We use this table to find users with little or no money spent
    build_mailchimp_users_table():
        build the Mailchimp user (subscriber) table
        We use this table to track user's last open, rating, etc.
    get_subscriber_email_set():
        Returns a set of email addresses found in the Mailchimp user (subscriber) table.
        Used to avoid adding duplicate records to the table.
    insert_user_data():
        insert data into the Mailchimp user table from a csv
        This can be run at anytime (at the start of project or when adding new subscribers)

Maintenance:
    We need to rebuild the Shopify sales table EVERYTIME we want to search for users to unsubscribe
    The Shopify sales table uses a Customer export from Shopify (not Orders!)
    We need to add new Mailchimp subscribers to the user table periodically
    We need to update Mailchimp subscribers data periodically (last open, etc)
    Best Practice: update Mailchimp user table monthly

Other Info:
    created 11-5-2020
"""
from pathlib import Path
from rc.db.sqlite_3.oop import Database

from build_mailchimp_user_table import build_mailchimp_users_table
from build_shopify_sales_table import build_sales_table
from insert_mailchimp_user_data import (get_subscriber_email_set, insert_user_data)

HOME_DIR = Path(__file__).resolve().parent


if __name__ == '__main__':
    database = Database(HOME_DIR.joinpath('db/test.db'))
    shopify_data_folder = HOME_DIR.joinpath('data/shopify')
    build_sales_table(database, shopify_data_folder)
    build_mailchimp_users_table(database)
    csv_data = HOME_DIR.joinpath('data/subscribers/subscribed_segment_export.csv')
    email_set = get_subscriber_email_set(database)
    insert_user_data(database, csv_data, email_set)
