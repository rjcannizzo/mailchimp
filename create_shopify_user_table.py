"""
Create and populate Shopify 'sales' database



11-4-2020
"""
import csv
from pathlib import Path
from rc.db.sqlite_3.oop import Database

HOME_DIR = Path(__file__).resolve().parent


def count_email_occurrences(shopify_data_folder=HOME_DIR.joinpath('data/shopify')):
    counts = dict()

    files = (f for f in Path(shopify_data_folder).glob('*.csv'))
    for file in files:
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Email']:
                    counts[row['Email']] = counts.get(row['Email'], 0) + 1

    for email in counts:
        if counts[email] > 1:
            print(f"'{email}', {counts[email]}")


def get_shopify_user_values(shopify_data_folder):
    """
    Generator that yields email, total spent and total orders from any csv files found in the 'shopify_data_folder'.
    This data is used when inserting data into the 'sales' table.
    :param shopify_data_folder: directory with 1 or more 'Customer' csv files exported from Shopify.
    :yield: tuple
    """
    files = (f for f in Path(shopify_data_folder).glob('*.csv'))
    for file in files:
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Email']:
                    yield row['Email'], row['Total Spent'], row['Total Orders']


def create_shopify_sales_table(database):
    """
    This function is used to both create AND populate the shopify 'sales' table.
    NOTE: We drop and recreate the table each time rather than updating values.
    :return:
    """
    drop_table_query = """DROP TABLE IF EXISTS 'sales'; """
    insert_query = """INSERT INTO sales ('email', 'total_spent', 'order_count') VALUES (?,?,?);"""
    create_table_query = """CREATE TABLE "sales" (
    "email"	TEXT, "total_spent" REAL, "order_count" INTEGER, PRIMARY KEY("email"));"""

    db = Database(database)
    db.run_script(drop_table_query)
    db.create_table(create_table_query)
    values = get_shopify_user_values(shopify_data_folder=HOME_DIR.joinpath('data/shopify'))
    db.insert_many(query=insert_query, values=values)
    print(f"Added {db.get_total_changes()} rows to Shopify 'sales' table.")


def main():
    create_shopify_sales_table(HOME_DIR.joinpath('db/test.db'))


if __name__ == '__main__':
    main()
