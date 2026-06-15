import mariadb
import settings

conn = mariadb.connect(
    host=settings.db_host,
    port=settings.db_port,
    user=settings.db_user,
    password=settings.db_password,
    database=settings.db_name
)

cur = conn.cursor()
sql = "SELECT * FROM "
sql += settings.tbl_name
sql += ";"
print(sql)
cur.execute(sql)
res = cur.fetchall()
for r in res:
    print(r)
cur.close()
conn.close()