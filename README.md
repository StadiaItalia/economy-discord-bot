# economy-discord-bot

## Discord bot

Build your own discord guild economy with this bot!

What?! Discord economy?! 

Yeah! Just reward your users for being active or winning events in you community!

## Commands

The bot will answer to these commands:

Command | Description
--------|------------
e>info | Will show a help message that will list the bot commands and some useful informations
e>config | Will show a configuration recap
e>config <prefix> <value> | Will update a configuration to the passed value
e>register | Will register your wallet and start counting your activities reward

## Configuration

So far you can customize these configurations for you discord server:

Prefix | Description
--------|------------
role <@role> | Specify the role the bot will listen to when searching for commands
command_channel <#channel> | Specify the channel the bot will listen to (defaults to every channel the bot role can read)

TODO

## FAQ

**I want to invite this bot to my server**

Easy peasy, just
click [here](https://discord.com/api/oauth2/authorize?client_id=811156112639918080&permissions=1342557264&scope=bot) and
follow the procedure for inviting the bot!

**Do I have to save some environment variables for the bot to function?**

Absolutely, here's the required environment variables (or saved into a `.env` file):

Variable | Description
---------|------------
ECONOMY_DISCORD_TOKEN | Discord token (obtained through Discord Developer Portal)
ECONOMY_LOGGING_LEVEL | Logging level `[WARN, ERROR, INFO, DEBUG]`
ECONOMY_DATABASE_HOST | MongoDB connection string (it should be something like `mongodb://\[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]` )
ECONOMY_DATABASE | MongoDB database name
ECONOMY_DATABASE_USER | Self explanatory
ECONOMY_DATABASE_PASSWORD | Self explanatory
ECONOMY_DATABASE_CONFIGURATION_COLLECTION | Collection where guild configurations will be stored
ECONOMY_DATABASE_WALLET_COLLECTION | Collection where user wallet will be stored