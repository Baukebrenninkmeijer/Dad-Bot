# Henry Bot
HenryBot is a fun interactive bot for groupchats in telegram. The bot will respond to any triggers that are added, with the given responses. His triggers can be seen by issuing the `/triggers` command, while commands can be added with the `/add` command. 

Henry's triggers are global, meaning that you can see the triggers of other chats and the other way around. One might argue this has its drawbacks, but I would argue that it creates some hilarious situations. HenryBot supports all unicode characters, among which are emojis, greek letters and different fonts. 

This bot can be found on [telegram](https://t.me/HenryBot).

The repo is build up like this:
I develop the bot in bot.ipynb, because I think it is quite handy. Using the notebook2script.py (credits to Jeremy Howard from fast.ai) this notebook is converted to bot.py. To get a clear overview of all the components, I advise you to look at bot.py. Lib.py contains some useful additional functions like database access.

If you would like to run this project, you should have a config.ini containing two things:

RDS
- url
- db
- username
- password

telegram
- api_token

You can put any database information in RDS, its just called that cause that's what I use. Make sure to have a `triggers` table in your database and you should be ready to go. 
