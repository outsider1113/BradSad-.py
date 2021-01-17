#Hello and thank you for taking a look at our discord bot!

The SchoologyRemind Bot is a discord bot that can send reminders for assignments or tests you have coming up. 
The bot itself is ran on heroku as well as the database we use to store the user's info.
Our bot is able to get assignments by asking the user for their 'key' and 'secret' which are api tokens special to each user.
The bot puts the discord user's schoology info into a table in the database.
The bot then takes the info from the table and gets the user's class info in order to get assignments.
Note: There can only be one discord user per row/server, so if another user wants to use the bot in the same server they must reset the bot using the shown commands and send their key and secret again
Note: Throughout the code, discord servers are often refered to as guilds and server id's as guild id's.
This was made by two highschool students who were bored during winter break in quarantine. So please bear this in mind before you make heavy judgements or assumptions on our code. 
Thank you.
