import asyncio
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
        async def info(ctx):
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            embed = cf.get_info_embed(command_prefix=economy_bot.command_prefix,
                                      language=language.select(configuration.language))
            await ctx.channel.send(embed=embed)

        @economy_bot.command()
        async def config(ctx, *args):
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            language_dictionary = language.select(configuration.language)
            embed = None
            if not args:
                embed = cf.get_configuration_embed(command_prefix=economy_bot.command_prefix,
                                                   configuration=configuration,
                                                   language=language_dictionary)

            elif len(args) >= 2:
                prefix = args[0]
                if prefix == "language":
                    value = args[1]
                    if value not in language.get_languages():
                        embed = cf.get_error_embed(language=language_dictionary, key="language_not_present")
                    else:
                        embed = update_value(guild_id=ctx.guild.id, item=prefix, value=value,
                                             language_dictionary=language_dictionary)
                elif prefix == "role":
                    value = args[1]
                    if value == "disable":
                        embed = update_value(guild_id=ctx.guild.id, item=prefix, value=None,
                                             language_dictionary=language_dictionary)
                    elif not discord.utils.get(ctx.guild.roles, id=int(cf.clean_role_id(role_id=value))):
                        embed = cf.get_error_embed(language=language_dictionary, key="role_not_present")
                    else:
                        embed = update_value(guild_id=ctx.guild.id, item=prefix, value=value,
                                             language_dictionary=language_dictionary)

                elif prefix == "command_channel":
                    value = args[1]
                    if value == "disable":
                        embed = update_value(guild_id=ctx.guild.id, item=prefix, value=None,
                                             language_dictionary=language_dictionary)
                    elif not discord.utils.get(ctx.guild.channels, id=int(cf.clean_channel_id(channel_id=value))):
                        embed = cf.get_error_embed(language=language_dictionary, key="channel_not_present")
                    else:
                        embed = update_value(guild_id=ctx.guild.id, item=prefix, value=value,
                                             language_dictionary=language_dictionary)

                elif prefix == "listening_channels":
                    value = args[1:]
                    if args[1] == "disable":
                        embed = update_value(guild_id=ctx.guild.id, item=prefix, value=None,
                                             language_dictionary=language_dictionary)
                    # TODO add a check for every channel listed
                    # elif not discord.utils.get(ctx.guild.channels, id=int(cf.clean_channel_id(channel_id=value))):
                    #     embed = cf.get_error_embed(language=language_dictionary, key="channel_not_present")
                    # else:
                    logger.debug(value)
                    embed = update_value(guild_id=ctx.guild.id, item=prefix, value=value,
                                         language_dictionary=language_dictionary)

                elif prefix == "currency_name":
                    value = args[1]
                    embed = update_value(guild_id=ctx.guild.id, item=prefix, value=value,
                                         language_dictionary=language_dictionary)

                elif prefix == "currency_icon":
                    value = args[1]
                    embed = update_value(guild_id=ctx.guild.id, item=prefix, value=value,
                                         language_dictionary=language_dictionary)

                elif prefix == "check_maximum_messages":
                    value = args[1]
                    if not value.isnumeric():
                        embed = cf.get_error_embed(language=language_dictionary, key="value_not_numeric")
                    elif not int(value) > 0:
                        embed = cf.get_error_embed(language=language_dictionary, key="value_greater_zero")
                    else:
                        embed = update_value(guild_id=ctx.guild.id, item=prefix, value=int(value),
                                             language_dictionary=language_dictionary)

                elif prefix == "check_minimum_messages":
                    value = args[1]
                    if not value.isnumeric():
                        embed = cf.get_error_embed(language=language_dictionary, key="value_not_numeric")
                    elif not int(value) > 0:
                        embed = cf.get_error_embed(language=language_dictionary, key="value_greater_zero")
                    else:
                        embed = update_value(guild_id=ctx.guild.id, item=prefix, value=int(value),
                                             language_dictionary=language_dictionary)

                elif prefix == "check_maximum_currency":
                    value = args[1]
                    if not value.isnumeric():
                        embed = cf.get_error_embed(language=language_dictionary, key="value_not_numeric")
                    elif not int(value) > 0:
                        embed = cf.get_error_embed(language=language_dictionary, key="value_greater_zero")
                    else:
                        embed = update_value(guild_id=ctx.guild.id, item=prefix, value=int(value),
                                             language_dictionary=language_dictionary)

                elif prefix == "check_timer":
                    value = args[1]
                    if not value.isnumeric():
                        embed = cf.get_error_embed(language=language_dictionary, key="value_not_numeric")
                    elif not int(value) > 0:
                        embed = cf.get_error_embed(language=language_dictionary, key="value_greater_zero")
                    else:
                        embed = update_value(guild_id=ctx.guild.id, item=prefix, value=int(value),
                                             language_dictionary=language_dictionary)

                elif prefix == "payment_confirmation":
                    value = args[1]
                    if value.lower() not in ["true", "false"]:
                        embed = cf.get_error_embed(language=language_dictionary, key="incorrect_value")
                    else:
                        embed = update_value(guild_id=ctx.guild.id, item=prefix, value=value,
                                             language_dictionary=language_dictionary)
            else:
                embed = cf.get_error_embed(language=language_dictionary, key="configuration_arguments")

            await ctx.channel.send(embed=embed)

        @economy_bot.command()
        async def register(ctx):
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            language_dictionary = language.select(configuration.language)
            confirmation_message = await cf.send_confirmation(context=ctx,
                                                              title=language_dictionary["registration"]["title"],
                                                              description=language_dictionary["registration"][
                                                                  "description"])

            def check_confirmation(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "✅"

            try:
                reaction, user = await economy_bot.wait_for("reaction_add", timeout=15.0, check=check_confirmation)
            except asyncio.TimeoutError:
                embed = cf.get_error_embed(language=language_dictionary, key="timeout")
                await confirmation_message.edit(embed=embed)
                await confirmation_message.clear_reactions()
            else:
                if database.create_wallet(user_id=ctx.author.id, guild_id=ctx.guild.id):
                    embed = cf.get_done_embed(language=language_dictionary)
                else:
                    embed = cf.get_error_embed(language=language_dictionary, key="wallet_already_registered")
                await confirmation_message.edit(embed=embed)
                await confirmation_message.clear_reactions()

        def update_value(guild_id, item, value, language_dictionary):
            if database.update_configuration(guild_id=guild_id,
                                             item=item,
                                             value=value):
                return cf.get_done_embed(language=language_dictionary)
            else:
                return cf.get_error_embed(language=language_dictionary, key="cannot_update")

        economy_bot.run(token)
