import psycopg2
import psycopg2.extras
import os

class database():
    def __init__(self):
        self.con = psycopg2.connect(
            host = "ec2-54-85-80-92.compute-1.amazonaws.com",
            database = "d6kmshmo9tirmk",
            user = " ggafqzhfpirbcv",
            password = "380e30db212700a1427a48f143f59bd21b6563131387821e5eeb22157982a4c4",
            port = 5432
            )
            
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
    
    def createTable(self):
        cur = self.con.cursor()
        cur.execute("Create Table disc_users (guild bigint primary key, secret text, key text, init boolean, class_code bigint, user_code bigint, discuser_id bigint)")
        self.con.commit
        cur.close()
        self.con.close()