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
        cursor.execute("SELECT * FROM test_schema.swltable")

        print('query successful')
        results = cursor.fetchall()
        cnx.close()
        return results
    except mysql.connector.Error as err:
        print('query failed:{}'.format(err))
        print('check mysql server running')

def run_search_query(searchtext):
    try:
        cnx = mysql.connector.connect(user='remote_user', password='turbo',
                              host='10.4.3.71',
                              database='test_schema')
        cursor = cnx.cursor()
        search = '%' + searchtext + '%'
        print('running query')
        cursor.execute("SELECT * FROM test_schema.swltable WHERE description LIKE (%s);",(search,))
        print('query successful')
        results = cursor.fetchall()
        cnx.close()
        print(results)
        return results
    except mysql.connector.Error as err:
        print('query failed:{}'.format(err))
        print('check mysql server running')


def add_entry(entry):
    try:
        cnx = mysql.connector.connect(user='remote_user', password='turbo',
                              host='10.4.3.71',
                              database='test_schema')
        cursor = cnx.cursor()
        # cursor.execute("INSERT INTO test_schema.swltable(description, category, subcat, group, model, quality, "
        #                "reference, measparam, notes, checked, dba, oct31_5, oct63, oct125, oct250, oct500, oct1k,"
        #                "oct2k, oct4k, oct8k, oct16k) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
        #                "%s,%s,%s)",entry)
        cursor.execute("INSERT INTO test_schema.swltable VALUES (0,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                       "%s,%s,%s,%s,%s,%s,%s,%s)",entry)

        print('import successful')
        cnx.commit()
        cnx.close()
        return
    except mysql.connector.Error as err:
        print('query failed:{}'.format(err))
        print('check mysql server running')
