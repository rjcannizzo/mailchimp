"""
build_sales_table()
    - Create and populate the Shopify 'sales' table.
    - NOTE: We don't update the table; we recreate it everytime we need to run queries.
    - this table has the following columns: 'email', 'total_spent', 'order_count'
get_shopify_sales_data()
    - A generator that yields the data for the 'sales' table.
    - To get the data, export all Customers from Shopify to the 'shopify_data_folder'.
WARNINGS:
    - Shopify customer exports contains empty values ('') for some emails causing insertion errors.
11-4-2020
"""
import csv
from pathlib import Path
from rc.db.sqlite_3.oop import Database

HOME_DIR = Path(__file__).resolve().parent


def get_shopify_sales_data(shopify_data_folder):
    """
    Generator that yields from all csv files found in the 'shopify_data_folder'.
    data yielded: email, total spent and total orders
    This is used when inserting data into the 'sales' table.
    To get the raw csv data, export all Customers from Shopify to the 'shopify_data_folder'.
    :param shopify_data_folder: directory with 1 or more csv files exported from Shopify ('Customer' export).
    :yield: tuple
    """
    files = (f for f in Path(shopify_data_folder).glob('*.csv'))
    for file in files:
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Email']:
                    yield row['Email'], row['Total Spent'], row['Total Orders']


def build_sales_table(db, shopify_data_folder):
    """
    This function is used to create AND populate the Shopify 'sales' table.
    NOTE: We drop and recreate the table each time rather than updating its values.
    :return: None
    """
    insert_query = """INSERT INTO sales ('email', 'total_spent', 'order_count') VALUES (?,?,?);"""
    create_table_query = \
        """CREATE TABLE "sales" ("email" TEXT, "total_spent" REAL, "order_count" INTEGER, PRIMARY KEY("email"));"""

    db.run_script("""DROP TABLE IF EXISTS 'sales';""")
    db.create_table(create_table_query)
    values = get_shopify_sales_data(shopify_data_folder)
    db.insert_many(query=insert_query, values=values)
    print(f"Added {db.get_total_changes()} rows to Shopify 'sales' table.")


def main():
    database = Database(HOME_DIR.joinpath('db/test.db'))
    shopify_data_folder = HOME_DIR.joinpath('data/shopify')
    build_sales_table(database, shopify_data_folder)


if __name__ == '__main__':
    main()
