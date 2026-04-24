import mysql.connector
try:
    db = mysql.connector.connect(host="localhost", user="root", password="anushka333", database="skillify")
    cursor = db.cursor()
    cursor.execute("SHOW TABLES;")
    print("Tables:", cursor.fetchall())
    cursor.execute("DESCRIBE requests;")
    print("Requests schema:", cursor.fetchall())
except Exception as e:
    print("Error:", e)
