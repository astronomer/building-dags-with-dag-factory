"""
etl_helpers.py

Functions to be called using PythonOperator in the etl.yml and dynamic_etl.yml file.
"""


def extract_helper():
    pass


def transform_helper(ds_nodash):
    print(f"ds_nodash: {ds_nodash}")


def load_helper(database_name, table_name):
    print(f"database_name: {database_name}, table_name: {table_name}")
