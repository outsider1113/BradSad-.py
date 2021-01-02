import pyautogui, time, discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print(self)

client = MyClient()
client.run("Nzk0ODA5MzYzOTczMjc1NjQ4.X_AN5w.cZvphqU4FLUrG4Kl4H7p-29l1uE")

print("Sad Brad")
sadbrad = True 
if (sadbrad):
    print("brad is sad")
else:
    print("brad is glad")