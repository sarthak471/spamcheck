import sqlite3
from faker import Faker
import random

fake = Faker()

""" Kindly Register and login through APIs to get encryped password save in Database """

try:
    #Pass the complete path of the db.sqlite3 file with respect to your system
    url = '/django/django_task/db.sqlite3'
    sqliteConnection = sqlite3.connect(url)
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")


    for i in range (1,100):
        name = str(fake.name())
        email = str(fake.email())
        unique_id1 = random.randrange(1, 9999, 1)
        unique_id2 = random.randrange(1, 9999, 1)
        phoneno =  random.randrange(1111111111, 9999999999, 10)
        password =  str(random.randrange(1111111111, 9999999999, 10))
        is_spam = bool(random.getrandbits(1))
        is_registered = True
        cursor.execute("INSERT INTO spam_check_registor_user VALUES (?,?,?,?,?)",(unique_id1,name, password ,phoneno,email))
        cursor.execute("INSERT INTO spam_check_registor_contact VALUES (?,?,?,?,?,?)",(unique_id2,phoneno,name, is_spam ,unique_id1,is_registered))
        sqliteConnection.commit()
    
    print("Data inserted in spam_check_registor_user and spam_check_registor_contact table")
    cursor.close()

except sqlite3.Error as error:
    print("Error while inserting data in a sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("sqlite connection is closed")