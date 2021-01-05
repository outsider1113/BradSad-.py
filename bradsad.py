import time, discord, requests
import oauth2 as oauth, urllib
import requests_oauthlib
import json
import pytz
from datetime import datetime
from getschoologystuff import schoology as schoology

#else:
    #await message.channel.send(message.author.mention + " Please Finish initalization first with command:\n+init")
path = "https://api.schoology.com/v1"
key = "6c457bdf6661e60b42292540a754394e05faf105c"
secret = "7595214e6c1a35452960e2fbfe0bafe9"
userscode = "55633162"
classcode = "2535704616"
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

    async def on_message(self, message):
        global keyentered, secretentered, tempuserkey, tempusersecret, tempusercode, initializing
        if(message.author.id != self.user.id):
            if(message.guild != None):
                if(message.content == "+today" and keyentered and secretentered):
                    print(message.author,":", message.content)
                    assignmentDict = sortAssignments(schoology(key, secret), classcode)#replace with tempuser key/secret
                    #valueList = list(assignmentDict.values())
                    try:
                        cdate = getCurrentDate(False)
                        temp = assignmentDict[cdate]
                        await message.channel.send(embed = sendEmbed(discord,temp[0],temp[3],cdate,temp[4], temp[2], temp[1], message.author.display_name, message.author.avatar_url))
                    except KeyError:
                        await message.channel.send(message.author.mention + " There are no assignments due today")
                elif (message.content == "+nextday" and keyentered and secretentered):
                    print(message.author,":", message.content)
                    assignmentDict = sortAssignments(schoology(key,secret), classcode)
                    try:
                        nextDate = getCurrentDate(True)
                        temp = assignmentDict[nextDate] #replace brackets with nextDate
                        await message.channel.send(embed = sendEmbed(discord,temp[0],temp[3],nextDate,temp[4], temp[2], temp[1], message.author.display_name, message.author.avatar_url))
                    except KeyError:
                        await message.channel.send(message.author.mention +  " There are no assignments due Tomorrow")
                elif (message.content == "+init"):
                    userGuild = message.guild
                    print(userGuild)
                    await message.author.send("Hello\nPlease Enter key and Secret\n\nEnter Key Below: ")
                elif ((message.content == "+today" or message.content == "+nextday") and not keyentered and not secretentered):
                    await message.channel.send(message.author.mention + " Please Finish initalization first with command:\n+init")
                elif (message.content == "+classes"):
                    #gets all classes from user, it will need the usercode (new or not), so you can move this elif around to where the user has already intialized
                    classesDict = sortClasses(schoology(key, secret), tempusercode)
                    classesList = classesDict.keys()
                    await message.channel.send(embed = sendClassEmbed(discord, message.author.display_name, message.author.avatar_url, classesList[0], classesList[1], classesList[2], classesList[3], classesList[4], classesList[5])) 
                    #after the embed message the user should choose a number which corresponds to the course, which will be linked to a classcode.
                    #then the function sortChosenClass will be called which will take their input and return the class code (make sure to int() their input)
            elif(message.guild == None and (not keyentered and not secretentered)): #I NEED IT TO NOT READ MESSAGES UNLESS INIT COMMMAND HAS BEEN CALLED
                if(not keyentered):
                    tempuserkey = message.content #store  
                    keyentered = True
                    await message.author.send("Key Recieved!\nPlease enter secret: ")
                elif(not secretentered):
                    tempusersecret = message.content #store in a limited dict 
                    secretentered = True
                    await message.author.send("Secret Recieved\nChecking if correct Momentarily")
                    try:
                        tempschool = schoology(tempuserkey,tempusersecret)
                        tempuser = tempschool.getusercode()
                        if(tempuser == None):
                            secretentered = False
                            keyentered = False
                            await message.author.send("Invalid Secret or Key\nPlease initalize once again(Keys and Secrets must be Exact do not leave empty space)")
                        else:
                            userList = sortUser(schoology(tempuserkey,tempusersecret)) 
                            tempusercode = userList[0] #sets the new usercode 
                            await message.author.send("Succesful you can now use the commands in your server")
                    except:
                        secretentered = False
                        keyentered = False
                        await message.author.send("Invalid Secret or Key\nPlease initalize once again(Keys and Secrets must be Exact do not leave empty space)")

def sendEmbed(disc, title, desc, date, typeof, points, time, author, authorurl):
    #Creates embed and returns it 
    embedVar = disc.Embed(title= title, description= desc, color=0x42f5f5)
    embedVar.set_author(name= author, icon_url= authorurl) #shows the user name and their avator at the top of the embed for aesthetic purposes 
    embedVar.set_thumbnail(url = "https://p11cdn4static.sharpschool.com/UserFiles/Servers/Server_141067/Image/sgy%20logo%20resized.png") #shows the schoology logo for aesthetic purposes
    embedVar.add_field(name="Assignment Type", value=typeof, inline=False)
    embedVar.add_field(name="Points Worth", value= points, inline=False)    
    embedVar.add_field(name="Time Due", value= time, inline=False)
    return embedVar

def sendClassEmbed(disc, author, authorurl, class1, class2, class3, class4, class5, class6):
    #creates the embed to show the selected user's classes
    #should be followed by bot seeing which class it chose in classesList and set the class code accordingly
    embed= disc.Embed(title="Your Classes", description="Please choose which class you would like to view", color=0x5119d4)
    embed.set_author(name= author, icon_url= authorurl)
    embed.set_thumbnail(url="https://p11cdn4static.sharpschool.com/UserFiles/Servers/Server_141067/Image/sgy%20logo%20resized.png")
    embed.add_field(name="1. " + class1, value="", inline=False)
    embed.add_field(name="2. " + class2, value="", inline=False)
    embed.add_field(name="3. " + class3, value="", inline=False)
    embed.add_field(name="4. " + class4, value="", inline=False)
    embed.add_field(name="5. " + class5, value="", inline=False)
    embed.add_field(name="6. " + class6, value="", inline=False)
    embed.set_footer(text="Please select a number 1-6")
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
    sc = school 
    scgetuserinfo = sc.getusercourses(userscode)
    scgetallcourses = scgetuserinfo['section']
    tempDict = {}
    for i in scgetallcourses:
        tempDict[i['course_title']] = i['id']
    return tempDict

def sortUser(school):
    sc = school 
    scgetusercode = sc.getusercode()
    tempList = [""]
    tempList[0] = scgetusercode['uid']
    return tempList

def sortChosenClass(num):
    #takes the input of the user which is a number 1-6 and and matches the class to the class code
    classesDict = sortClasses(schoology(key, secret), userscode)
    classesList = list(classesDict.keys())
    print(classesDict)
    print(classesList)
    classchoiceName = ''
    classchoiceCode = ''
    """
    Bro what if i told you input is a python function and this probably gonna break sooner or later if not changed 
    """
    if (num == 1):
        classchoiceName = classesList[0]
        classchoiceCode = classesDict[classchoiceName]
    elif (num == 2):
        classchoiceName = classesList[1]
        classchoiceCode = classesDict[classchoiceName]
    elif (num == 3):
        classchoiceName = classesList[2]
        classchoiceCode = classesDict[classchoiceName]
    elif (num == 4):
        classchoiceName = classesList[3]
        classchoiceCode = classesDict[classchoiceName]
    elif (num == 5):
        classchoiceName = classesList[4]
        classchoiceCode = classesDict[classchoiceName]
    elif (num == 6):
        classchoiceName = classesList[5]
        classchoiceCode = classesDict[classchoiceName]
    return classchoiceCode

userList = sortUser(schoology(key,secret))
classchoice = sortChosenClass(2)
print(classchoice)
#print(userList)
client = MyClient()
client.run("Nzk0ODA5MzYzOTczMjc1NjQ4.X_AN5w.cZvphqU4FLUrG4Kl4H7p-29l1uE")
