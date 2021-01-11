import psycopg2
import psycopg2.extras
import os
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

class database():
    def __init__(self):
        self.con = psycopg2.connect(
            host = "localhost",
            database = "postgres",
            user = "postgres",
            password = "ballsdeep69",
            port = 5432
            )#5432 if brando, 5433 if joel
    """
    We will need to make a create TABLE function that runs once somehow when deploying to heroku. Usually we can check if the db exists by running the function again and if 
    their is an error we can use try/except to ignore it

    Also maybe add a HASH for encrypting secret and key(if you have time then you can but i doubt that many people will use it) if in more than 2000 guilds discord kinda
    requires that but we good i think
    """
    def checkguildInDb(self, guildID):
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select 1 from disc_users where guild = %s;",(guildID,))
        checked = cur.fetchone()
        cur.close()
        self.con.close()
        return checked #this will either return NONE or 1. if using this just check if NONE or NOT NONE because the dictionary it returns is fucking weird
    
    def checkuserInDb(self, userID):
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select 1 from disc_users where discuser_id = %s;",(userID,))
        checked = cur.fetchone()
        cur.close()
        self.con.close()
        return checked

    def getGuildProfile(self,guildID):
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select * from disc_users where guild = %s;",(guildID,))
        userProfile = cur.fetchone()
        cur.close()
        self.con.close()
        return userProfile #this returns a dictionary the KEY is the column name in the database (we can use this for checking anything)

    def getGuildProfile2 (self, userID):
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select * from disc_users where discuser_id = %s;",(userID,))
        userProfile = cur.fetchone()
        cur.close()
        self.con.close()
        return userProfile

    def addGuildID(self, newguildID, discid):
        cur = self.con.cursor()
        cur.execute("insert into disc_users (guild,init,discuser_id) values(%s,%s,%s)", (newguildID,False,discid,)) #This SHOULD ONLY  execute when the user first types init we need a checker BECAUSE your making a NEW row
        self.con.commit()
        cur.close()             #I THINK we should also add the user who initialized it
        self.con.close()    #UniqueViolation error if duplicate item is added - should add try/except to counter this

    def addFinalSecretAndKey(self, newKey, newSecret, guildID):
        cur = self.con.cursor()
        cur.execute("update disc_users set secret = %s, key = %s, init = %s where guild = %s", (newSecret, newKey, True,guildID,)) #IF this were to run then that would mean that the secret and key are correct and init is then made TRUE
        self.con.commit()
        cur.close()
        self.con.close()

    def addClasscode(self, newClasscode, guildID):
        cur = self.con.cursor() #InterfaceError
        cur.execute("update disc_users set class_code = %s, init = %s where guild = %s", (newClasscode, True,guildID,))         
        self.con.commit()
        cur.close()
        self.con.close()

    def addUsercode_id(self, usercode, guildID):
        cur = self.con.cursor()
        cur.execute("update disc_users set user_code = %s, init = %s where guild = %s", (usercode,True,guildID,))         
        self.con.commit()
        cur.close()
        self.con.close()

    def deleteRow(self, guildID):
        cur = self.con.cursor()
        cur.execute("delete from disc_users where guild = %s", (guildID,))
        self.con.commit()
        cur.close()
        self.con.close()
    
    def checkUserinAGuild(self, userID):
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select 1 from disc_users where discuser_id = %s;",(userID,))
        checked = cur.fetchone()
        cur.close()
        self.con.close()
        return checked
    
    def addSecret(self, newSecret, userID):
        cur = self.con.cursor()
        cur.execute("update disc_users set secret = %s where discuser_id = %s", (newSecret,userID,)) #IF this were to run then that would mean that the secret and key are correct and init is then made TRUE
        self.con.commit()
        cur.close()
        self.con.close()
    
    def addKey(self, newKey, userID):
        cur = self.con.cursor()
        cur.execute("update disc_users set key = %s where discuser_id = %s", (newKey,userID,)) #IF this were to run then that would mean that the secret and key are correct and init is then made TRUE
        self.con.commit()
        cur.close()
        self.con.close()



db = database()
#db.addGuildID("445070783258165288")   -penthouse
#s = db.checkguildInDb("121212121")
#v = db.getGuildProfile("121212121")
#db.addSecretAndKey("6c457bdf6661e60b42292540a754394e05faf105c","7595214e6c1a35452960e2fbfe0bafe9","445070783258165288")
#db.addClasscode("3372963514", "445070783258165288")
#db.addUsercode_id("55633162", "445070783258165288") brando user and discid, for penthouse
#db.addGuildID("722984937468198978", "343403664175792128") 
#db.addClasscode("3372963610", "722984937468198978") #interfaceerror- connection already closed, if you were to run 93 and 94 (where the guildid originally doesnt exist) it adds another row for the guildid, but places the classcode in the first row.
#t = db.getGuildProfile("722984937468198978")
#db.deleteRow("722984937468198978") #the guild/row was obvi already deleted
#db.deleteRow("722984937468198978")
"""
whats left to do is finish the bot part using this module 
ill figure it out some other day but you can explore some
stuff with sql adn what else a db can do
"""
"""
Todo: 
-add a delete row function incase they kick the bot or use a command to clear themselves or if the first init command call fails(this should delete the row by looking for the row with the guildID)
    DONE- deletes the row as it should, however if you run the function again for the row you just deleted nothing happens, no errors nothing in the table changes. possibly good or bad. must confer later
-add function that adds the class code/ user code to db  
    DONE- put them into seperate functions because it makes more sense
-add a function that can change the class code / user code  
    DONE- if you run the same function that adds them it overides the previous value so it works, woopty doo ez pz
"""