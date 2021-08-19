import boto3
import sqlite3
from sqlite3 import Error
import pandas as pd
from sqlalchemy import create_engine


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def execute_query(conn, sql_string):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param sql_string: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql_string)
    except Error as e:
        print(e)


if __name__ == '__main__':
    s3 = boto3.client(
        's3',
        aws_access_key_id="aws_access_key_id",
        aws_secret_access_key="aws_secret_access_key"
    )
    response = s3.list_objects(
        Bucket='remotesome-data-engineer-task1'
    )

    create_connection("remote_db.db")
    conn = sqlite3.connect("remote_db.db")
    engine = create_engine('sqlite://', echo=False)

    s3.download_file('remotesome-data-engineer-task1', '2012-1.csv', '2012-1.csv')
    s3.download_file('remotesome-data-engineer-task1', '2012-2.csv', '2012-2.csv')
    s3.download_file('remotesome-data-engineer-task1', '2012-3.csv', '2012-3.csv')
    s3.download_file('remotesome-data-engineer-task1', '2012-4.csv', '2012-4.csv')
    s3.download_file('remotesome-data-engineer-task1', '2012-5.csv', '2012-5.csv')

    df1 = pd.read_csv('2012-1.csv')
    df2 = pd.read_csv('2012-2.csv')
    df3 = pd.read_csv('2012-3.csv')
    df4 = pd.read_csv('2012-4.csv')
    df5 = pd.read_csv('2012-5.csv')

    df1.to_sql('data_2012', con=engine, if_exists='append')
    df2.to_sql('data_2012', con=engine, if_exists='append')
    df3.to_sql('data_2012', con=engine, if_exists='append')
    df4.to_sql('data_2012', con=engine, if_exists='append')
    df5.to_sql('data_2012', con=engine, if_exists='append')

    print("count of rows : %s" % sum([len(df1), len(df2), len(df3), len(df4), len(df5)]))
    engine.execute("SELECT min(price) FROM data_2012").fetchall()
    engine.execute("SELECT max(price) FROM data_2012").fetchall()
    engine.execute("SELECT avg(price) FROM data_2012").fetchall()

    s3.download_file('remotesome-data-engineer-task1', 'validation.csv', 'validation.csv')
    df_val = pd.read_csv('validation.csv')
    df_val.to_sql('val_2012', con=engine, if_exists='append')
    engine.execute("SELECT * FROM val_2012").fetchall()





