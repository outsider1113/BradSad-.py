import time, discord, requests, random
import oauth2 as oauth, urllib
import requests_oauthlib
import json
import pytz
from datetime import datetime
from getschoologystuff import schoology as schoology
from db import database as database
#else:
    #await message.channel.send(message.author.mention + " Please Finish initalization first with command:\n+init")
path = "https://api.schoology.com/v1"
key = "6c457bdf6661e60b42292540a754394e05faf105c"
secret = "7595214e6c1a35452960e2fbfe0bafe9"
userscode = "55633162"
classcode = "2535704616"
discordid = "343403664175792128"
userChannels = {}
userGuild = ""
keyentered = False
secretentered = False
tempuserkey = " "
tempusersecret = " "
tempusercode = ""
initializing = False
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed = welcomeEmbed(discord))
            break
    
    async def on_message(self, message):
        if(message.author.id == self.user.id):
            return
        args = message.content.split()
        print(args)
        if (args[0]== "+help"):
            await message.channel.send(embed = helpEmbed(discord))
            #await message.author.send(embed = initEmbed(discord))
        elif(args[0] == "+init"):
            db = database()
            if(db.checkguildInDb(message.guild.id) == None):
                db = database()
                db.addGuildID(message.guild.id, message.author.id)
                #await message.author.send("Hello!\nLets Get Started With The Setup\n```css\nFor the following steps please vist your own Schoology page(The one you use everyday)\nThen In the Browser URL after the '.com' type '/api'\nIt should look something like this: 'www.schoology.com/api'\n(Note Schoology.com is probably different for you specific to your school which doesnt matter)\nThen the page it leads to will have your secret and key\nFor the Next part use the command '+key' in this direct message, in order to input your key from the webisite```")
                await message.author.send(embed = initEmbed(discord))
                print()
            else:
                await message.channel.send(message.author.mention + "Someone has Already Called This Command")
                print()
        elif(args[0] == "+secret"):
            if(message.guild == None):
                userdb = database().checkuserInDb(message.author.id)
                #profile = database().getGuildProfile2(message.author.id)
                if(userdb == None and database().getGuildProfile2(message.author.id)['key'] != None):
                    await message.channel.send("You Have Not used '+init' yet")
                elif(userdb != None and database().getGuildProfile2(message.author.id)['init'] == True and database().getGuildProfile2(message.author.id)['key'] != None):
                    await message.channel.send("Your Secret and Key is already being used in another server. Please Have Someone else With the same class/classes set up the Bot\nIf You Believe this is a mistake and your key is being used without your permission use '+help' for more info on how to reset your key and secret")
                    database().deleteRow(database().getGuildProfile2(message.author.id)['guild'])  
                elif(userdb != None and database().getGuildProfile2(message.author.id)['init'] == False and database().getGuildProfile2(message.author.id)['secret'] == None and database().getGuildProfile2(message.author.id)['key'] != None):
                    try:
                        database().addSecret(args[1], message.author.id)
                        try:
                            userkey = database().getGuildProfile2(message.author.id)['key']
                            userSecret = database().getGuildProfile2(message.author.id)['secret']
                            userGuildID = database().getGuildProfile2(message.author.id)['guild']
                            tempschool = schoology(userkey,userSecret)
                            tempuser = tempschool.getusercode()
                            if(tempuser == None):
                                database().deleteRow(database().getGuildProfile2(message.author.id)['guild'])
                                await message.channel.send("Invalid Secret or Key: Please use the command '+init' in your server again")
                            else:
                                userList = sortUser(schoology(userkey,userSecret)) 
                                tempusercode = userList #sets the new usercode
                                database().addUsercode_id(tempusercode, userGuildID)
                                await message.author.send("Succesful you can now use the commands in your server")
                        except:
                            database().deleteRow(database().getGuildProfile2(message.author.id)['guild'])
                            await message.channel.send("Invalid Secret or Key: Please use the command '+init' in your server again")
                            print()
                    except:
                        await message.channel.send("invalid secret entry")
                elif(userdb != None and database().getGuildProfile2(message.author.id)['init'] == False and database().getGuildProfile2(message.author.id)['secret'] != None and database().getGuildProfile2(message.author.id)['key'] != None):
                    await message.channel.send("Already entered a Secret")
                elif(database().getGuildProfile2(message.author.id)['key'] == None):
                    await message.channel.send("Need to enter Key First with '+key'")       
            else:
                await message.channel.send("Please only use this command in direct messages" )
        elif(args[0] == "+key"):
            if(message.guild == None):
                userdb = database().checkuserInDb(message.author.id)
                #database().getGuildProfile2(message.author.id)
                if(userdb == None):
                    await message.channel.send("You Have Not used '+init' yet")
                elif(userdb != None and database().getGuildProfile2(message.author.id)['init'] == True):
                    await message.channel.send("Your Secret or Key is already being used in another server. Please Have Someone else With the same class/classes set up the Bot\nIf You Believe this is a mistake and your key is being used without your permission use '+help' for more info on how to reset your key and secret")
                    database().deleteRow(database().getGuildProfile2(message.author.id)['guild'])  
                elif(userdb != None and database().getGuildProfile2(message.author.id)['init'] == False and database().getGuildProfile2(message.author.id)['key'] == None):
                    try:
                        database().addKey(args[1], message.author.id)
                        await message.channel.send("Succesful Key add\n\nPlease use the command '+secret (enter secret here)' to add your Secret'")
                    except:
                        await message.channel.send("invalid key entry")
                elif(userdb != None and database().getGuildProfile2(message.author.id)['init'] == False and database().getGuildProfile2(message.author.id)['key'] != None):
                    await message.channel.send("Already entered a Key")       
            else:
                await message.channel.send("Please only use this command in direct messages" )
        elif(args[0] == "+reset"):
            if(message.guild != None):
                if(database().checkguildInDb(message.guild.id) == None):
                    await message.channel.send("Bot has not been initialized in this server yet")
                else:
                    database().deleteRow(message.guild.id)
                    await message.channel.send("Completed Rest run '+init' again")
        elif(args[0] == "+today"):
            if(message.guild != None):
                userDb = database().checkguildInDb(message.guild.id)
                if(userDb == None):
                    await message.channel.send("Pleas use '+init' command first and finish setup")
                elif(userDb != None and database().getGuildProfile(message.guild.id)['init'] == False):
                    await message.channel.send("Please finsih setup with '+init' command")
                else:
                    profile = database().getGuildProfile(message.guild.id)
                    userkey = profile['key']
                    usersecret = profile['secret']
                    classcode = profile['class_code']
                    #assignmentDict = sortAssignments(schoology(userkey,usersecret),classcode )
                    
                    try:
                        assignmentDict = sortAssignments(schoology(userkey,usersecret),classcode )
                        cdate = getCurrentDate(False)
                        temp = assignmentDict[cdate]
                        await message.channel.send(embed = sendEmbed(discord,temp[0],temp[3],cdate,temp[4], temp[2], temp[1], message.author.display_name, message.author.avatar_url))
                    except KeyError:
                        await message.channel.send(message.author.mention + " There are no assignments due today")
            else:
                await message.channel.send("Please use this command in your Server")
        elif(args[0] == "+nextday"):
            if(message.guild != None):
                userDb = database().checkguildInDb(message.guild.id)
                if(userDb == None):
                    await message.channel.send("Pleas use '+init' command first and finish setup")
                elif(userDb != None and database().getGuildProfile(message.guild.id)['init'] == False):
                    await message.channel.send("Please finsih setup with '+init' command")
                else:
                    profile = database().getGuildProfile(message.guild.id)
                    userkey = profile['key']
                    usersecret = profile['secret']
                    classcode = profile['class_code']
                    #assignmentDict = sortAssignments(schoology(userkey,usersecret),classcode )
                    
                    try:
                        assignmentDict = sortAssignments(schoology(userkey,usersecret),classcode )
                        cdate = getCurrentDate(True)#for next date this just has to be true
                        temp = assignmentDict[cdate]
                        await message.channel.send(embed = sendEmbed(discord,temp[0],temp[3],cdate,temp[4], temp[2], temp[1], message.author.display_name, message.author.avatar_url))
                    except KeyError:
                        await message.channel.send(message.author.mention + " There are no assignments due today")
            else:
                await message.channel.send("Please use this command in your Server")
        elif(args[0] == "+classes"):
            """
            classesDict = sortClasses(schoology(key, secret), userscode)
            classesList = list(classesDict.keys())
            await message.channel.send(embed = sendClassEmbed(discord, message.author.display_name, message.author.avatar_url, classesList[0], classesList[1], classesList[2], classesList[3], classesList[4], classesList[5], classesList[6]))
            """
            if(message.guild != None):
                userDb = database().checkguildInDb(message.guild.id)
                if(userDb == None):
                    await message.channel.send("Pleas use '+init' command first and finish setup")
                elif(userDb != None and database().getGuildProfile(message.guild.id)['init'] == False):
                    await message.channel.send("Please finsih setup with '+init' command")
                else:
                    profile = database().getGuildProfile(message.guild.id)
                    userkey = profile['key']
                    usersecret = profile['secret']
                    usercode = str(profile['user_code'])
                    classesDict = sortClasses(schoology(userkey, usersecret), usercode)
                    classesList = list(classesDict.keys())
                    print(classesList)
                    await message.channel.send(embed = sendClassEmbed(discord, message.author.display_name, message.author.avatar_url, classesList[0], classesList[1], classesList[2], classesList[3], classesList[4], classesList[5], classesList[6]))
            else:
                await message.channel.send("Please use this command in your Server")
        elif(args[0] == "+c"):
            if(message.guild != None):
                userDb = database().checkguildInDb(message.guild.id)
                if(userDb == None):
                    await message.channel.send("Pleas use '+init' command first and finish setup")
                elif(userDb != None and database().getGuildProfile(message.guild.id)['init'] == False):
                    await message.channel.send("Please finsih setup with '+init' command")
                else:
                    profile = database().getGuildProfile(message.guild.id)
                    userkey = profile['key']
                    usersecret = profile['secret']
                    usercode = str(profile['user_code'])
                    classChosenList = sortChosenClass(args[1],userkey,usersecret,usercode)
                    if classChosenList == None:
                        await message.channel.send("your dumb af")
                    else:
                        #usercode = classChosenList[0]
                        #classcode = classChosenList[1]
                        await message.channel.send("You have selected **"+classChosenList[1]+"**, if this is not the class you want to view please resend the command.")
        else:
            return

def sendEmbed(disc, title, desc, date, typeof, points, time, author, authorurl):
    #Creates embed and returns it 
    embedVar = disc.Embed(title= title, description= desc, color=0x42f5f5)
    embedVar.set_author(name= author, icon_url= authorurl) #shows the user name and their avator at the top of the embed for aesthetic purposes 
    embedVar.set_thumbnail(url = "https://p11cdn4static.sharpschool.com/UserFiles/Servers/Server_141067/Image/sgy%20logo%20resized.png") #shows the schoology logo for aesthetic purposes
    embedVar.add_field(name="Assignment Type", value=typeof, inline=False)
    embedVar.add_field(name="Points Worth", value= points, inline=False)    
    embedVar.add_field(name="Time Due", value= time, inline=False)
    return embedVar

def sendClassEmbed(disc, author, authorurl, class1, class2, class3, class4, class5, class6, class7):
    #creates the embed to show the selected user's classes
    #should be followed by bot seeing which class it chose in classesList and set the class code accordingly
    embed= disc.Embed(title="Your Classes", description="Please choose which class you would like to view", color=0x5119d4)
    embed.set_author(name= author, icon_url= authorurl)
    embed.set_thumbnail(url="https://p11cdn4static.sharpschool.com/UserFiles/Servers/Server_141067/Image/sgy%20logo%20resized.png")
    embed.add_field(name="1. " , value=class1, inline=False)
    embed.add_field(name="2. " , value=class2, inline=False)
    embed.add_field(name="3. " , value=class3, inline=False)
    embed.add_field(name="4. " , value=class4, inline=False)
    embed.add_field(name="5. " , value=class5, inline=False)
    embed.add_field(name="6. " , value=class6, inline=False)
    embed.add_field(name="7. " , value=class7, inline=False)
    embed.set_footer(text="Please select a number 1-7")
    return embed

def helpEmbed(disc):
    #embeded message for the +help command, shows all the commands along with descriptions
    embed= disc.Embed(title = "HELP", description = ":arrow_down: :arrow_down: :arrow_down: :arrow_down: :arrow_down: :arrow_down:" , color=0xdc6f09)
    embed.set_thumbnail(url = "https://p11cdn4static.sharpschool.com/UserFiles/Servers/Server_141067/Image/sgy%20logo%20resized.png")
    embed.add_field(name="Setup Commands:", value=":tools:", inline=False)
    embed.add_field(name="+init", value="Initialization of the bot (Should be ran first).", inline=False)
    embed.add_field(name="+key ", value="Only used in direct messages with bot.", inline=True)
    embed.add_field(name="+secret", value="Only used in direct messages with bot.", inline=False)
    embed.add_field(name="+classes", value="Displays the list of classes you can see updates for.\n------------------------------------------------------------", inline=False)
    embed.add_field(name="General Commands:", value = ":gem:", inline=False)
    #embed.set_image(url="https://cdn.discordapp.com/attachments/461448421320949764/512005978108067850/image0.gif", inline =True)
    embed.add_field(name="+classchoose (#1-7)", value="Choose the number that corresponds with the class you would like to view", inline=False)
    embed.add_field(name="+today", value="Shows all assignments due today for the class you have selected.", inline=False)
    embed.add_field(name="+nextday", value="Shows all assignments due tomorrow for the class you have selected.", inline=False)
    embed.add_field(name="+reset", value="Deletes your info from the bot's database. +init should be called again.\n----------------------------------------------------------- ", inline=True)
    embed.set_footer(text="If you have any further questions or suggestions contact BrandoWithTheLambo#3469")
    return embed

def welcomeEmbed(disc):
    #embeded message which should be sent when the bot joins the server
    embed = disc.Embed(title = "Thank you for adding me! :pray:", description = "My prefix is +", color=0x000000)
    embed.set_thumbnail(url = "https://p11cdn4static.sharpschool.com/UserFiles/Servers/Server_141067/Image/sgy%20logo%20resized.png")
    embed.add_field(name="See a list of commands by typing +help", value=":tools:", inline=True)
    embed.add_field(name = "Start up the bot by typing +init", value = ":magic_wand:", inline=True)
    embed.set_footer(text="If you have any further questions or suggestions contact BrandoWithTheLambo#3469")
    embed.set_image(url="https://cdn.discordapp.com/attachments/461448421320949764/512005978108067850/image0.gif")
    return embed

def initEmbed(disc):
    #embeded message that should be sent to the user in dm's 
    embed = disc.Embed(title = "For the following steps please vist your own Schoology page :computer:", description = 'The one you use everyday', color = 0xc738e0)
    embed.set_thumbnail(url = "https://p11cdn4static.sharpschool.com/UserFiles/Servers/Server_141067/Image/sgy%20logo%20resized.png")
    embed.add_field(name = "Then in the browser URL after the .com type /api :globe_with_meridians:", value = "The url should look like lms.lausd.net/api or schoology.com/api", inline = False)
    embed.add_field(name = "Next type +key (your key from the site) :key: ", value = "Your message should look like '+key sdlfk332j22' ", inline = True)
    embed.add_field(name = "After the successful key add, type +secret (your secret from the api site) :lock:", value = "Your message should look like '+secret bvnxm321r'", inline = True)
    embed.set_footer(text="If you have any further questions or suggestions contact BrandoWithTheLambo#3469")
    return embed
    
def getCurrentDate(tomorrow):
    #gets the current date
    pst = pytz.timezone('America/Los_Angeles')
    tempDate = datetime.now(pst)
    tempLeapyear = tempDate.year % 4
    if tomorrow:
        if (tempDate.day == 31 and (tempDate.month == 1 or tempDate.month == 3 or tempDate.month == 5 or tempDate.month == 7 or tempDate.month == 8 or tempDate.month == 10 or tempDate.month == 12)):
            tempDate = tempDate.replace(month = tempDate.month + 1)
            tempDate = tempDate.replace(day = 1)
        elif (tempDate.day == 30 and (tempDate.month == 4 or tempDate.month == 6 or tempDate.month == 9 or tempDate.month == 11)):
            tempDate = tempDate.replace(month = tempDate.month + 1)
            tempDate = tempDate.replace(day = 1)
        elif (tempDate.day == 28 and tempDate.month == 2 and tempLeapyear != 0):
            tempDate = tempDate.replace(month = tempDate.month + 1)
            tempDate = tempDate.replace(day = 1)
        elif (tempDate.day == 29 and tempDate.month == 2 and tempLeapyear == 0):
            tempDate = tempDate.replace(month = tempDate.month + 1)
            tempDate = tempDate.replace(day = 1)
        else: 
            tempDate = tempDate.replace(day = tempDate.day + 1)
    dateAndTime = str(tempDate).split()
    currentDate = dateAndTime[0]
    print("The current date is:", currentDate)
    print("Sad Brad")
    return currentDate

def convertTime(milTime):
    #function that changes the time from military to standard so it is legible
    temptime = milTime[1].split(':')
    temptime[0] = int(temptime[0]) 
    if (temptime[0] > 12):
        temptime[0] -= 12
        temptime[2] = "PM"
    else:
        temptime[2] = "AM"
    standardTime = str(temptime[0]) + ':' + temptime[1] + ' '+ temptime[2]
    return standardTime

def sortAssignments(school, classcode):
    sc = school
    starter = 0
    limiter = 20
    assignmentCounter = 0
    scgetcourses = sc.getassignments(starter, limiter, classcode)
    scgetassignments = scgetcourses['assignment']
    tempDict = {}
    for i in scgetassignments:
        #loops through all assignments and assigns the tite and date to a dictionary where the keys are the dates and the values are the titles
        assignmentDueDateandTime = i['due'].split()
        assignmentDueDateandTime[1] = convertTime(assignmentDueDateandTime)
        tempDict[assignmentDueDateandTime[0]] = [i['title'], assignmentDueDateandTime[1],i['max_points'],i['description'],i['type']]
        assignmentCounter += 1
        if(assignmentCounter == 20):
            #resets the limit and calls the getassignments module again to get all assignments
            assignmentCounter = 0
            starter += 20
            limiter += 20
            scgetcourses = sc.getassignments(starter, limiter, classcode)
            for x in scgetcourses['assignment']:
                #gets the next set of assignments 
                scgetassignments.append(x)
    return tempDict

def sortClasses(school, userscode):
    #sorts through the user's courses and places them in a dictionary with the course name and the class id
    sc = school 
    scgetuserinfo = sc.getusercourses(userscode)
    scgetallcourses = scgetuserinfo['section']
    tempDict = {}
    tempListNames = []
    tempListIds = []
    for i in scgetallcourses:
        print(i)
        #This would append to the two lists
        tempListNames.append(i['course_title'])
        tempListIds.append(i['id'])

        tempDict[i['course_title']] = i['id']
    return tempDict

def sortUser(school):
    #sorts through the user's information and gets the user's id
    sc = school 
    scgetusercode = sc.getusercode()
    tempList = [""]
    tempList[0] = scgetusercode['uid']
    return tempList[0]

def sortChosenClass(num,key,secret,usercode):
    #takes the input of the user which is a number 1-7 and and matches the class to the class code
    classesDict = sortClasses(schoology(key, secret), usercode)
    classesList = list(classesDict.keys())
    print(classesDict)
    print(classesList)
    classchoiceName = ''
    classchoiceCode = ''
    if (num == '1'):
        classchoiceName = classesList[0]
        classchoiceCode = classesDict[classchoiceName]
    elif (num == '2'):
        classchoiceName = classesList[1]
        classchoiceCode = classesDict[classchoiceName]
    elif (num == '3'):
        classchoiceName = classesList[2]
        classchoiceCode = classesDict[classchoiceName]
    elif (num == '4'):
        classchoiceName = classesList[3]
        classchoiceCode = classesDict[classchoiceName]
    elif (num == '5'):
        classchoiceName = classesList[4]
        classchoiceCode = classesDict[classchoiceName]
    elif (num == '6'):
        classchoiceName = classesList[5]
        classchoiceCode = classesDict[classchoiceName]
    elif (num == '7'):
        classchoiceName = classesList[6]
        classchoiceCode = classesDict[classchoiceName]
    else:
        return None
    return [classchoiceCode, classchoiceName]

#userList = sortUser(schoology(key,secret))
#classchoice = sortChosenClass(2)
#print(classchoice)
#print(userList)
client = MyClient()
client.run("Nzk0ODA5MzYzOTczMjc1NjQ4.X_AN5w.cZvphqU4FLUrG4Kl4H7p-29l1uE")



"""
-I realized a dictioanry cant have values with the same KEY so this means that if someone has the same titled class or if 
their is an assignment with the same due date we need to make an exception for it
- so we have to make it a list and loop through the list in order to find matching things.

optimal? No, but fuck you

other than that were basically done we just need to push to heroku 
"""
