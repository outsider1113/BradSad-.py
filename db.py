import psycopg2
import psycopg2.extras
import os

class database():
    def __init__(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        self.con = psycopg2.connect(DATABASE_URL, sslmode='require')
            
    def checkguildInDb(self, guildID):
        #checks if the discord server is in the database and will either return NONE or 1. 
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select 1 from disc_users where guild = %s;",(guildID,))
        checked = cur.fetchone()
        cur.close()
        self.con.close()
        return checked
    
    def checkuserInDb(self, userID):
        #checks if the discord user is in the table
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select 1 from disc_users where discuser_id = %s;",(userID,))
        checked = cur.fetchone()
        cur.close()
        self.con.close()
        return checked

    def getGuildProfile(self,guildID):
        #this returns a dictionary of the row based on the discord server 
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select * from disc_users where guild = %s;",(guildID,))
        userProfile = cur.fetchone()
        cur.close()
        self.con.close()
        return userProfile 

    def getGuildProfile2 (self, userID):
        #this returns a dictionary of the row based on the discord user id
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select * from disc_users where discuser_id = %s;",(userID,))
        userProfile = cur.fetchone()
        cur.close()
        self.con.close()
        return userProfile

    def addGuildID(self, newguildID, discid):
        #adds a new row to the table with the server id and discord user id
        cur = self.con.cursor()
        cur.execute("insert into disc_users (guild,init,discuser_id) values(%s,%s,%s)", (newguildID,False,discid,))
        self.con.commit()
        cur.close()          
        self.con.close()    

    def addFinalSecretAndKey(self, newKey, newSecret, guildID):
        #adds the sercret and key to the row where the message's discord server id is from
        cur = self.con.cursor()
        cur.execute("update disc_users set secret = %s, key = %s, init = %s where guild = %s", (newSecret, newKey, True,guildID,))
        self.con.commit()
        cur.close()
        self.con.close()

    def addClasscode(self, newClasscode, guildID):
        #adds the class code to the row, can be run again to replace the class code if the user chooses another class
        cur = self.con.cursor() 
        cur.execute("update disc_users set class_code = %s, init = %s where guild = %s", (newClasscode, True,guildID,))         
        self.con.commit()
        cur.close()
        self.con.close()

    def addUsercode_id(self, usercode, guildID):
        #adds the discord user's schoology usercode to the row
        cur = self.con.cursor()
        cur.execute("update disc_users set user_code = %s, init = %s where guild = %s", (usercode,True,guildID,))         
        self.con.commit()
        cur.close()
        self.con.close()

    def deleteRow(self, guildID):
        #deletes the whole row from the dictionary based off of the discord server id
        cur = self.con.cursor()
        cur.execute("delete from disc_users where guild = %s", (guildID,))
        self.con.commit()
        cur.close()
        self.con.close()
    
    def checkUserinAGuild(self, userID):
        #checks if a discord user exists in the table
        cur = self.con.cursor(cursor_factory= psycopg2.extras.DictCursor)
        cur.execute("select 1 from disc_users where discuser_id = %s;",(userID,))
        checked = cur.fetchone()
        cur.close()
        self.con.close()
        return checked
    
    def addSecret(self, newSecret, userID):
        #adds the secret to the row
        cur = self.con.cursor()
        cur.execute("update disc_users set secret = %s where discuser_id = %s", (newSecret,userID,))
        self.con.commit()
        cur.close()
        self.con.close()
    
    def addKey(self, newKey, userID):
        #adds the key to the row
        cur = self.con.cursor()
        cur.execute("update disc_users set key = %s where discuser_id = %s", (newKey,userID,))
        self.con.commit()
        cur.close()
        self.con.close()
    
    def createTable(self):
        #creates the table in the databse with all the necessary collumns and the guild(discord server id) as the primary key
        cur = self.con.cursor()
        cur.execute("create table disc_users (guild bigint , secret text, key text, init boolean, class_code bigint, user_code bigint, discuser_id bigint)")
        self.con.commit()
        cur.close()
        self.con.close()