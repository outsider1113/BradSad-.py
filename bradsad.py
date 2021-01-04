import time, discord, requests
import oauth2 as oauth, urllib
import requests_oauthlib
import json
import pytz
from datetime import datetime
from getschoologystuff import schoology as schoology


#else:
#   await message.channel.send(message.author.mention + " Please Finish initalization first with command:\n+init")
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
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        global keyentered, secretentered, tempuserkey, tempusersecret
        if(message.author.id != self.user.id):
            if(message.guild != None):
                if(message.content == "+today" and keyentered and secretentered):
                    print(message.author,":", message.content)
                    assignmentDict = sortAssignments(schoology(key, secret), classcode)#replace with tempuser key/secret
                    #valueList = list(assignmentDict.values())
                    try:
                        cdate = getCurrentDate(False)
                        temp = assignmentDict[cdate]
                        await message.channel.send(embed = sendEmbed(discord,temp[0],temp[3],cdate,temp[4], temp[2], temp[1]))
                    except KeyError:
                        await message.channel.send(message.author.mention + " There are no assignments due today")
                elif (message.content == "+nextday" and keyentered and secretentered):
                    print(message.author,":", message.content)
                    assignmentDict = sortAssignments(schoology(key,secret), classcode)
                    try:
                        nextDate = getCurrentDate(True)
                        temp = assignmentDict[nextDate] #replace brackets with nextDate
                        await message.channel.send(embed = sendEmbed(discord,temp[0],temp[3],nextDate,temp[4], temp[2], temp[1]))
                    except KeyError:
                        await message.channel.send(message.author.mention +  " There are no assignments due Tomorrow")
                elif (message.content == "+init"):
                    userGuild = message.guild
                    print(userGuild)
                    await message.author.send("Hello\nPlease Enter key and Secret\n\nEnter Key Below: ")
                elif((message.content == "+today" or message.content == "+nextday") and not keyentered and not secretentered):
                    await message.channel.send(message.author.mention + " Please Finish initalization first with command:\n+init")
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
                            await message.author.send("Succesful you can now use the commands in your server")
                    except:
                        secretentered = False
                        keyentered = False
                        await message.author.send("Invalid Secret or Key\nPlease initalize once again(Keys and Secrets must be Exact do not leave empty space)")


def sendEmbed(disc, title, desc, date, typeof, points, time):
    #Creates embed and returns it 
    embedVar = disc.Embed(title= title, description= desc, color=0x42f5f5)
    embedVar.add_field(name="Assignment Type", value=typeof, inline=False)
    embedVar.add_field(name="Points Worth", value= points, inline=False)    
    embedVar.add_field(name="Time Due", value= time, inline=False)
    return embedVar

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

sc = schoology(key,secret)
scgetallcourses = sc.getusercourses(userscode)
#print(scgetallcourses)

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

def sortClasses(school):
    sc = school 
    scgetuserinfo = sc.getusercourses(userscode)
    scgetallcourses = scgetuserinfo['section']
    tempDict = {}
    for i in scgetallcourses:
        tempDict[i['course_title']] = i['id']
    return tempDict
    
"""
assignmentDict = sortAssignments(schoology(key,secret))
valueList = list(assignmentDict.values())
print(assignmentDict)

try:
    banana = assignmentDict[currentDate]
    print(banana)
except KeyError:
    print("There are no assignments due today")
"""
classesDict = sortClasses(schoology(key, secret))
print(classesDict)
client = MyClient()
client.run("Nzk0ODA5MzYzOTczMjc1NjQ4.X_AN5w.cZvphqU4FLUrG4Kl4H7p-29l1uE")
