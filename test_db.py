import mysql.connector

try:

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Muskaan25",
        database="campus_skill_gap"
    )

    print("MySQL connection successful!")

    connection.close()

except mysql.connector.Error as error:

    print("MySQL connection failed:")
    print(error)