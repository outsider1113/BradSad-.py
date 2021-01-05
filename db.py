import psycopg2
import psycopg2.extras
"""
con = psycopg2.connect(
    host = "localhost",
    database = "postgres",
    user = "postgres",
    password = "ballsdeep69",
    port = 5433)
#bot_guilds
cur = con.cursor()
cur.execute("select 1 from disc_users where guild = '121212212'  ")
rows = cur.fetchall()
print (rows)
cur.close()
con.close()
"""

class database:
    def __init__(self):
        self.con = psycopg2.connect(
            host = "localhost",
            database = "postgres",
            user = "postgres",
            password = "ballsdeep69",
            port = 5433)#5432 if brando
    
    def checkguildInDb(self, guildID):
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select 1 from disc_users where guild = %s;",(guildID,))
        checked = cur.fetchone()
        cur.close()
        self.con.close()
        return checked #this will either return NONE or 1. if using this just check if NOT NONE because the dictionary it returns is fucking weird

    def getGuildProfile(self,guildID):
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select * from disc_users where guild = %s;",(guildID,))
        userProfile = cur.fetchone()
        cur.close()
        self.con.close()
        return userProfile #this returns a dictionary the KEY is the column name in the database (we can use this for checking anything) 
    
    def addGuildID(self, newguildID):
        cur = self.con.cursor()
        cur.execute("insert into disc_users (guild,init) values(%s,%s)", (newguildID,False,)) #This SHOULD ONLY  execute when the user first types init we need a checker
        self.con.commit()
        cur.close() 
        self.con.close()

    def addSecretAndKey(self, newSecret, newKey):
        cur = self.con.cursor()
        cur.execute()
        cur.close()
        self.con.close()

db = database()
#s = db.checkguildInDb("121212121")
#v = db.getGuildProfile("121212121")
db.addGuildID("722984937468198978")