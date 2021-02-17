import traceback
import modules.common_functions as cf
import discord as discord
import languages.selector as language
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

    @staticmethod
    def start_bot(database, logger, token):
        economy_bot = EconomyBot(database=database, logger=logger)

        @economy_bot.event
        async def on_ready():
            await economy_bot.change_presence(status=discord.Status.idle,
                                              activity=discord.Game("Ready to roll!"))
            logger.info(f"{economy_bot.user} connected on Discord!")

        @economy_bot.event
        async def on_guild_join(guild):
            logger.info(f"Economy Bot was added into guild {guild.name}")
            logger.debug(f"Creating a configuration for guild {guild.name} - {guild.id}")
            database.create_configuration(guild=guild)

        @economy_bot.event
        async def on_guild_remove(guild):
            logger.info(f"Economy Bot was removed from {guild.name}")
            logger.info(f"Deleting configuration for guild {guild.name} - {guild.id}")
            database.remove_configuration(guild_id=guild.id)

        @economy_bot.command()
        async def info(ctx, **args):
            logger.debug(args)
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            lang = language.select(configuration.language)
            embed = cf.get_embed(title=lang["info_description"]["title"],
                                 description=lang["info_description"]["description"],
                                 color=discord.Colour.dark_green())
            embed.add_field(name=f"{economy_bot.command_prefix}info",
                            value=lang["info_description"]["info"],
                            inline=False)
            embed.add_field(name=f"{economy_bot.command_prefix}config",
                            value=lang["info_description"]["config"],
                            inline=False)
            embed.add_field(name=f"{economy_bot.command_prefix}config <{lang['prefix']}> <{lang['value']}>",
                            value=lang["info_description"]["config_update"],
                            inline=False)
            embed.add_field(name=lang["info_description"]["legend"],
                            value=lang["info_description"]["legend_description"],
                            inline=False)
            await ctx.channel.send(embed=embed)

        economy_bot.run(token)
