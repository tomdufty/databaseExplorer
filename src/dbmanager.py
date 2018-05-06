import mysql.connector
DB = 'test_schema'
ENTRY_TABLE = "test_schema.swltable"


def test_connection():
    try:
        cnx = mysql.connector.connect(user='remote_user', password='turbo',
                              host='10.4.3.71',
                              database='test_schema')
        cnx.close()
        print('connected to database')
    except mysql.connector.Error as err:
        print('failed to connect:{}'.format(err))
        print('check mysql server running')


def get_all_descriptions():
    try:
        cnx = mysql.connector.connect(user='remote_user', password='turbo',
                              host='10.4.3.71',
                              database='test_schema')
        cursor = cnx.cursor()
        #cursor.execute('SELECT * FROM %s', (ENTRY_TABLE,))
        first = 'first'
        cursor.execute("SELECT * FROM test_schema.swltable")

        print('query successful')
        results = cursor.fetchall()
        cnx.close()
        return results
    except mysql.connector.Error as err:
        print('query failed:{}'.format(err))
        print('check mysql server running')