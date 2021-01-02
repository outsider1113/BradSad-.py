import pyautogui, time, discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run(process.token.user)

print("Sad Brad")
sadbrad = True 
if (sadbrad):
    print("brad is sad")
else:
    print("brad is glad")