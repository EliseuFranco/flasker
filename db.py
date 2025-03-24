import psycopg2


my_db = psycopg2.connect(
    host="localhost",
    database = "blog",
    user = "postgres",
    password = "@Samulolo26",
    port = 5432
)

cursor = my_db.cursor()

cursor.execute("SELECT * FROM ")

data = cursor.fetchall()
print(data)