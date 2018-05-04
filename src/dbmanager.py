import mysql.connector

cnx = mysql.connector.connect(user='remote_user', password='turbo',
                              host='10.4.3.71',
                              database='test_schema')
cnx.close()