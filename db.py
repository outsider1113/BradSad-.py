import psycopg2

con = psycopg2.connect(
    host = "localhost",
    database = "postgres",
    user = "postgres",
    password = "ballsdeep69",
    port = 5432)
#bot_guilds
cur = con.cursor()
cur.execute("select 1 from bot_guilds where guild = '121212212'  ")
rows = cur.fetchall()
print (rows)
cur.close()
con.close()