import time, discord, requests
import oauth2 as oauth, urllib
import requests_oauthlib
import json

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

path = "https://api.schoology.com/v1"
key = "6c457bdf6661e60b42292540a754394e05faf105c"
secret = "7595214e6c1a35452960e2fbfe0bafe9"
#schoololooooogy = requests.get("https://api.schoology.com/v1")
#print(schoololooooogy)
starter = 0
limiter = 20
assignmentCounter = int(0)
"""
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print(message.author,":", message.content)
        print(message.author.id)
        if (message.author.id == 343403664175792128):
            await message.channel.send("{0.author.mention} stop being sad, brad".format(message))

client = MyClient()
client.run("Nzk0ODA5MzYzOTczMjc1NjQ4.X_AN5w.cZvphqU4FLUrG4Kl4H7p-29l1uE")

print("Sad Brad")
sadbrad = True 
if (sadbrad):
    print("brad is sad")
else:
    print("brad is glad")
"""
class schoology:
    def __init__(self, consumer_key, consumer_secret, domain='https://www.schoology.com', three_legged=False,
                    request_token=None, request_token_secret=None, access_token=None, access_token_secret=None):
            self.API_ROOT = 'https://api.schoology.com/v1'
            self.DOMAIN_ROOT = domain

            self.consumer_key = consumer_key
            self.consumer_secret = consumer_secret

            self.request_token = request_token
            self.request_token_secret = request_token_secret

            self.access_token = access_token
            self.access_token_secret = access_token_secret

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
            getlink = "https://api.schoology.com/v1/sections/2535704616/assignments"+"?start="+str(starter)+"&limit="+str(limiter)
            courses = self.oauth.get(getlink)
            return courses.json()
        except JSONDecodeError:
            return{}

sc = schoology(key,secret)
scgetuserinfo = sc.getuserinfo()
scgetcourses = sc.getcourses(starter, limiter)
scgetassignments = scgetcourses['assignment']
assignmentTitles = []
print(scgetcourses['total'])
print(scgetuserinfo['name_display'])
for i in scgetassignments:
    assignmentTitles.append(i['title'])
    assignmentCounter += 1
    if(assignmentCounter == 20):
        assignmentCounter = 0
        starter += 21
        limiter += 21
        scgetcourses = sc.getcourses(starter, limiter)
        for x in scgetcourses['assignment']:
            scgetassignments.append(x)

print(assignmentTitles)
#print(scgetassignments)