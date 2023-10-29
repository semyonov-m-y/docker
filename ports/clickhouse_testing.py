'''
Попробуем подключение к БД
Для начала поднимаем clickhouse-server:  docker run --rm -d -p 8123:8123 -p 9000:9000 --name ch_db yandex/clickhouse_server
1) Потом подгружаем tabix - веб-морду для clickhouse: docker pull spoonest/clickhouse-tabix-web-client и запускаем его docker run -d -p 8080:80 spoonest/clickhouse-tabix-web-client.
 а потом в браузере зайти на localhost:8080
2) А если работаем с Postgres, то поднимаем его: docker run -d --rm -e POSTGRES_PASSWORD=admin POSTGRESS_USER=admin -e POSTGRESS_DB=todo_db -p 5432:5432 postgres:14,
и для примера подгружаем superset: docker run --rm -d -p 8080:8088 --name superset apache/superset, запускаем его командой
docker exec -it superset superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin,
потом добавим роли: docker exec -it superset superset init, а потом в браузере зайти на localhost:8080
Если при создании БД не удается подключиться через 127.0.0.1 и порт 5432, то заменить ip на 172.17.0.2
'''
from pprint import pprint
from clickhouse_driver import connect

conn = connect(
    host="localhost",
    user="default",
    password="",
    port=9000,
    database="default"
)

cursor = conn.cursor()
cursor.execute("""SELECT * FROM todo_list""")
pprint(cursor.fetchall())