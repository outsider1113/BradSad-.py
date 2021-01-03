import time, discord, requests
import oauth2 as oauth, urllib
import requests_oauthlib
import json
import pytz
from datetime import datetime

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

path = "https://api.schoology.com/v1"
key = "6c457bdf6661e60b42292540a754394e05faf105c"
secret = "7595214e6c1a35452960e2fbfe0bafe9"

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if (message.content == "+Remind"):
            print(message.author,":", message.content)
            assignmentDict = sortAssignments(schoology(key,secret))
            #valueList = list(assignmentDict.values())
            try:
                cdate = getCurrentDate()
                temp = assignmentDict["2020-08-31"]
                await message.channel.send(embed = sendEmbed(discord,temp[0],temp[3],cdate,temp[4], temp[2], temp[1]))
            except KeyError:
                await message.channel.send("There are no assignments due today")    

def sendEmbed(disc, title, desc, date, typeof, points, time):
    embedVar = disc.Embed(title= title, description= desc, color=0x00ff00)
    embedVar.add_field(name="Assignment Type", value=typeof, inline=False)
    embedVar.add_field(name="Points Worth", value= points, inline=False)    
    embedVar.add_field(name="Time Due", value= time, inline=False)
    return embedVar

def getCurrentDate():
    pst = pytz.timezone('America/Los_Angeles')
    dateAndTime = str(datetime.now(pst)).split()
    currentDate = dateAndTime[0]
    print("The current date is:", currentDate)
    print("Sad Brad")
    return currentDate

def convertTime(milTime):
    temptime = milTime[1].split(':')
    temptime[0] = int(temptime[0]) 
    if (temptime[0] > 12):
            #if statement changes the time from military to standard so it is elligble
        temptime[0] -= 12
        temptime[2] = "PM"
    else:
        temptime[2] = "AM"
    standardTime = str(temptime[0]) + ':' + temptime[1] + ' '+ temptime[2]
    return standardTime

class schoology:
    def __init__(self, consumer_key, consumer_secret, domain='https://www.schoology.com', three_legged=False,
                    request_token=None, request_token_secret=None, access_token=None, access_token_secret=None):
            #establishes the root and domain which we already know 
            self.API_ROOT = 'https://api.schoology.com/v1'
            self.DOMAIN_ROOT = domain
            
            #allows to establish the key and secret we give it     
            self.consumer_key = consumer_key
            self.consumer_secret = consumer_secret
            
            #tokens for 3 legged oauth
            self.request_token = request_token
            self.request_token_secret = request_token_secret
            self.access_token = access_token
            self.access_token_secret = access_token_secret

            #requests self user with oauth using given secret and key 
            self.oauth = requests_oauthlib.OAuth1Session(self.consumer_key, self.consumer_secret)
            self.three_legged = three_legged

    def getuserinfo(self):
        try:
            user = self.oauth.get("https://api.schoology.com/v1/users/55633162")
            return user.json()
        except JSONDecodeError:
            return{}

    def getcourses(self, start, limit):
        try:
            getlink = "https://api.schoology.com/v1/sections/2535704616/assignments"+"?start="+str(start)+"&limit="+str(limit)
            courses = self.oauth.get(getlink)
            return courses.json()
        except JSONDecodeError:
            return{}

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
