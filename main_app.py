"""
Purpose:

Methods:

Maintenance:

Other Info:
11-5-2020
"""
from pathlib import Path
from rc.db.sqlite_3.oop import Database

from build_mailchimp_user_table import build_mailchimp_users_table
from build_shopify_sales_table import build_sales_table
from insert_mailchimp_user_data import (get_subscriber_email_set, insert_user_data)

HOME_DIR = Path(__file__).resolve().parent


def main():
    pass


if __name__ == '__main__':
    database = Database(HOME_DIR.joinpath('db/test.db'))
    shopify_data_folder = HOME_DIR.joinpath('data/shopify')
    build_sales_table(database, shopify_data_folder)
    build_mailchimp_users_table(database)
    csv_data = HOME_DIR.joinpath('data/subscribers/subscribed_segment_export.csv')
    email_set = get_subscriber_email_set(database)
    insert_user_data(database, csv_data, email_set)
