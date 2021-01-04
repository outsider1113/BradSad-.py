import time, discord, requests
import oauth2 as oauth, urllib
import requests_oauthlib
import json
import pytz
from datetime import datetime
from getschoologystuff import schoology as schoology

path = "https://api.schoology.com/v1"
key = "6c457bdf6661e60b42292540a754394e05faf105c"
secret = "7595214e6c1a35452960e2fbfe0bafe9"
userscode = "55633162"
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if (message.content == "+today"):
            print(message.author,":", message.content)
            assignmentDict = sortAssignments(schoology(key,secret))
            #valueList = list(assignmentDict.values())
            try:
                cdate = getCurrentDate(False)
                temp = assignmentDict[cdate]
                await message.channel.send(embed = sendEmbed(discord,temp[0],temp[3],cdate,temp[4], temp[2], temp[1]))
            except KeyError:
                await message.channel.send(message.author.mention + " There are no assignments due today")
        elif (message.content == "+nextday"):
            print(message.author,":", message.content)
            assignmentDict = sortAssignments(schoology(key,secret))
            try:
                nextDate = getCurrentDate(True)
                temp = assignmentDict[nextDate] #replace brackets with nextDate
                await message.channel.send(embed = sendEmbed(discord,temp[0],temp[3],nextDate,temp[4], temp[2], temp[1]))
            except KeyError:
                await message.channel.send(message.author.mention +  " There are no assignments due Tomorrow")

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
scgetallcourses = sc.getuserinfo(userscode)
print(scgetallcourses)

def sortAssignments(school):
    sc = school
    starter = 0
    limiter = 20
    assignmentCounter = 0
    scgetcourses = sc.getcourses(starter, limiter)
    scgetassignments = scgetcourses['assignment']
    tempDict = {}
    for i in scgetassignments:
        #loops through all assignments and assigns the tite and date to a dictionary where the keys are the dates and the values are the titles
        assignmentDueDateandTime = i['due'].split()
        assignmentDueDateandTime[1] = convertTime(assignmentDueDateandTime)
        tempDict[assignmentDueDateandTime[0]] = [i['title'], assignmentDueDateandTime[1],i['max_points'],i['description'],i['type']]
        assignmentCounter += 1
        if(assignmentCounter == 20):
            #resets the limit and calls the getcourses module again to get all assignments
            assignmentCounter = 0
            starter += 20
            limiter += 20
            scgetcourses = sc.getcourses(starter, limiter)
            for x in scgetcourses['assignment']:
                #gets the next set of assignments 
                scgetassignments.append(x)
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
client = MyClient()
client.run("Nzk0ODA5MzYzOTczMjc1NjQ4.X_AN5w.cZvphqU4FLUrG4Kl4H7p-29l1uE")
