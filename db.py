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
    
    """
    We will need to make a create TABLE function that runs once somehow when deploying to heroku. Usually we can check if the db exists by running the function again and if 
    their is an error we can use try/except to ignore it 
    """
    def checkguildInDb(self, guildID):
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select 1 from disc_users where guild = %s;",(guildID,))
        checked = cur.fetchone()
        cur.close()
        self.con.close()
        return checked #this will either return NONE or 1. if using this just check if NONE or NOT NONE because the dictionary it returns is fucking weird

    def getGuildProfile(self,guildID):
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select * from disc_users where guild = %s;",(guildID,))
        userProfile = cur.fetchone()
        cur.close()
        self.con.close()
        return userProfile #this returns a dictionary the KEY is the column name in the database (we can use this for checking anything) 
    
    def addGuildID(self, newguildID):
        cur = self.con.cursor()
        cur.execute("insert into disc_users (guild,init) values(%s,%s)", (newguildID,False,)) #This SHOULD ONLY  execute when the user first types init we need a checker BECAUSE your making a NEW row
        self.con.commit()
        cur.close() 
        self.con.close()

    def addSecretAndKey(self, newSecret, newKey,guildID):
        cur = self.con.cursor()
        cur.execute("update disc_users set secret = %s, key = %s, init = %s where guild = %s", (newSecret, newKey, True,guildID,)) #IF this were to run then that would mean that the secret and key are correct and init is then made TRUE
        self.con.commit()
        cur.close()
        self.con.close()

db = database()
#s = db.checkguildInDb("121212121")
#v = db.getGuildProfile("121212121")
db.addSecretAndKey("1c475f21b3be07678881010db6f0d207","0aed61ccaff6e2bdbb85018b9b787fbc05f51704a","722984937468198978")