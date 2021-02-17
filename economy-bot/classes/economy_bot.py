import traceback

import discord as discord
from discord.ext.commands import command

intents = discord.Intents.default()
intents.members = True


class EconomyBot(discord.ext.commands.Bot):
    def __init__(self, database, logger):
        super(EconomyBot, self).__init__(command_prefix="e>", intents=intents)
        self.database = database
        self.logger = logger

    async def on_error(self, event_method, *args, **kwargs):
        self.logger.error(f"Something went wrong: {event_method}")
        traceback.print_exc()

    async def on_ready(self):
        await self.change_presence(status=discord.Status.idle,
                                   activity=discord.Game("Ready to roll!"))
        self.logger.info(f"{self.user} connected on Discord!")

    async def on_guild_join(self, guild):
        self.logger.info(f"Economy Bot was added into guild {guild.name}")
        self.logger.debug(f"Creating a configuration for guild {guild.name} - {guild.id}")
        self.database.create_configuration(guild_id=guild.id)

    async def on_guild_remove(self, guild):
        self.logger.info(f"Economy Bot was removed from {guild.name}")
        self.logger.info(f"Deleting configuration for guild {guild.name} - {guild.id}")
        self.database.remove_configuration(guild_id=guild.id)

