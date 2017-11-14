import psycopg2
from psycopg2 import extras

db = psycopg2.connect("dbname='test_db' user='test' host='db' password='test'")
c = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
c.execute("SELECT * FROM deepstyle_job")

print (c.fetchall())
