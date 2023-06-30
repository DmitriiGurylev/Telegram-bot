import psycopg2


db_port = 5432
db_host = 'localhost'
db_name = 'my_db'
db_user = 'user_pg'
db_pass = 'my_pass'

conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
cursor = conn.cursor()

# docker run --name pg-db -e POSTGRES_DB=my_db -e POSTGRES_USER=user_pg -e POSTGRES_PASSWORD=my_pass -p 5432:5432 -d postgres:alpine3.18

# psql -h localhost -p 5432 --username="user_pg" -W -d my_db
