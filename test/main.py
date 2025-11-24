import psycopg2

# Соединение с сервером и базой данных
conn = psycopg2.connect(
    dbname="testdb",
    user="test",
    password="abcd",
    host="localhost",
    port=5432
)

# Создаем объект, который будет взаимодействовать с базой данных
cur = conn.cursor()
# Создаем запрос, отправляем на сервер и получаем ответ
cur.execute("SELECT * FROM users;")
# Распечатываем все строки, которые вернул SELECT
print(cur.fetchall())
# Закрываем соединение
conn.close()