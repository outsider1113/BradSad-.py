import time, discord, requests
import oauth2 as oauth, urllib

path = "https://api.schoology.com/v1"
key = "6c457bdf6661e60b42292540a754394e05faf105c"
secret = "7595214e6c1a35452960e2fbfe0bafe9"
#schoololooooogy = requests.get("https://api.schoology.com/v1")

#print(schoololooooogy)

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


def oauth_req(url, key, secret, http_method="POST", post_body=None, http_headers=None):
    CONSUMER_KEY = key
    CONSUMER_SECRET = secret
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    content = client.request(
        url,
        method=http_method,
        body= urllib.urlencode({'status': post_body}),
        headers=http_headers,
        force_auth_header=True,
    )
    return content

print(oauth_req(path, key, secret))