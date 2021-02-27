import asyncio
import datetime
import traceback

import discord as discord
from discord.ext.commands import command

import languages.selector as language
import modules.common_functions as cf
from enums.operation import Operation

intents = discord.Intents.default()
intents.members = True


class EconomyBot(discord.ext.commands.Bot):
    def __init__(self, database, logger):
        super(EconomyBot, self).__init__(command_prefix="e>", intents=intents)
        self.database = database
        self.logger = logger
        self.tasks = []

    async def on_error(self, event_method, *args, **kwargs):
        self.logger.error(f"Something went wrong: {event_method}")
        traceback.print_exc()

    @staticmethod
    def start_bot(database, logger, token):
        economy_bot = EconomyBot(database=database, logger=logger)

        @economy_bot.event
        async def on_ready():
            await economy_bot.change_presence(status=discord.Status.idle,
                                              activity=discord.Game("Ready to roll! Use e>info to start!"))
            logger.info(f"{economy_bot.user} connected on Discord!")
            for guild in economy_bot.guilds:
                configuration = database.read_configuration(guild_id=guild.id)
                if configuration.is_running:
                    logger.info(f"Starting loop control for guild {guild.id} {guild.name}")
                    economy_bot.tasks.append(
                        economy_bot.loop.create_task(check_user_activities(guild=guild), name=str(guild.id)))

        @economy_bot.event
        async def on_guild_join(guild):
            logger.info(f"Economy Bot was added into guild {guild.name}")
            logger.debug(f"Creating a configuration for guild {guild.name} - {guild.id}")
            database.create_configuration(guild=guild)

        @economy_bot.event
        async def on_guild_remove(guild):
            logger.info(f"Economy Bot was removed from {guild.name}")
            logger.info(f"Deleting configuration for guild {guild.name} - {guild.id}")
            database.remove_registered_users(guild_id=guild.id)
            database.remove_configuration(guild_id=guild.id)

        @economy_bot.command()
        async def info(ctx):
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            language_dictionary = language.select(configuration.language)
            if configuration.command_channel:
                if ctx.channel.id != int(cf.clean_channel_id(channel_id=configuration.command_channel)):
                    return
            embed = cf.get_info_embed(command_prefix=economy_bot.command_prefix,
                                      language=language_dictionary)
            if configuration.role:
                role = discord.utils.get(ctx.guild.roles, id=int(cf.clean_role_id(role_id=configuration.role)))
                if role in ctx.author.roles:
                    embed = cf.get_private_info_embed(command_prefix=economy_bot.command_prefix,
                                                      language=language_dictionary, embed=embed)
            embed.add_field(name=language_dictionary["info_description"]["legend"],
                            value=language_dictionary["info_description"]["legend_description"],
                            inline=False)
            await ctx.channel.send(embed=embed)

        @economy_bot.command()
        async def config(ctx, *args):
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            if configuration.role:
                role = discord.utils.get(ctx.guild.roles, id=int(cf.clean_role_id(role_id=configuration.role)))
                if role not in ctx.author.roles:
                    return

            language_dictionary = language.select(configuration.language)
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
                    else:
                        for channel in value:
                            channel_id = cf.clean_channel_id(channel_id=channel)
                            if not channel_id.isnumeric() or not discord.utils.get(ctx.guild.channels,
                                                                                   id=int(channel_id)):
                                embed = cf.get_error_embed(language=language_dictionary, key="configuration_parameter")
                                await ctx.channel.send(embed=embed)
                                return
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
                        embed = update_value(guild_id=ctx.guild.id, item=prefix,
                                             value=True if value.lower == "true" else False,
                                             language_dictionary=language_dictionary)
                else:
                    embed = cf.get_error_embed(language=language_dictionary, key="configuration_parameter")
            else:
                embed = cf.get_error_embed(language=language_dictionary, key="configuration_arguments")

            await ctx.channel.send(embed=embed)

        @economy_bot.command()
        async def start(ctx):
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            if configuration.role:
                role = discord.utils.get(ctx.guild.roles, id=int(cf.clean_role_id(role_id=configuration.role)))
                if role not in ctx.author.roles:
                    return

            language_dictionary = language.select(configuration.language)
            logger.info(f"Starting loop control for guild {ctx.guild.id} {ctx.guild.name}")
            running_task = [x for x in economy_bot.tasks if x.get_name() == str(ctx.guild.id)]
            if len(running_task) == 0:
                try:
                    economy_bot.tasks.append(
                        economy_bot.loop.create_task(check_user_activities(guild=ctx.guild), name=str(ctx.guild.id)))
                    embed = cf.get_done_embed(language=language_dictionary)
                    update_value(guild_id=ctx.guild.id, item="is_running",
                                 value=True, language_dictionary=language_dictionary)

                except RuntimeError:
                    embed = cf.get_error_embed(language=language_dictionary, key="cannot_start")
            else:
                embed = cf.get_error_embed(language=language_dictionary, key="already_running")
            await ctx.send(embed=embed)

        @economy_bot.command()
        async def stop(ctx):
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            if configuration.role:
                role = discord.utils.get(ctx.guild.roles, id=int(cf.clean_role_id(role_id=configuration.role)))
                if role not in ctx.author.roles:
                    return

            language_dictionary = language.select(configuration.language)
            logger.info(f"Stopping loop control for guild {ctx.guild.id} {ctx.guild.name}")

            running_task = [x for x in economy_bot.tasks if x.get_name() == str(ctx.guild.id)]
            if len(running_task) > 0:
                try:
                    running_task[0].cancel()
                    embed = cf.get_done_embed(language=language_dictionary)
                    update_value(guild_id=ctx.guild.id, item="is_running",
                                 value=False, language_dictionary=language_dictionary)

                except RuntimeError:
                    embed = cf.get_error_embed(language=language_dictionary, key="cannot_stop")
            else:
                embed = cf.get_error_embed(language=language_dictionary, key="already_stopped")
            await ctx.send(embed=embed)

        @economy_bot.command()
        async def register(ctx):
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            if configuration.command_channel:
                if ctx.channel.id != int(cf.clean_channel_id(channel_id=configuration.command_channel)):
                    return
            language_dictionary = language.select(configuration.language)
            confirmation_message = await cf.send_private_confirmation(user=ctx.author,
                                                                      title=language_dictionary["registration"][
                                                                          "title"],
                                                                      description=language_dictionary["registration"][
                                                                          "description"])

            def check_confirmation(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "✅"

            try:
                reaction, user = await economy_bot.wait_for("reaction_add", timeout=30.0, check=check_confirmation)
            except asyncio.TimeoutError:
                embed = cf.get_error_embed(language=language_dictionary, key="timeout")
                await confirmation_message.delete()
            else:
                if database.create_wallet(user_id=ctx.author.id, guild_id=ctx.guild.id):
                    embed = cf.get_done_embed(language=language_dictionary)
                else:
                    embed = cf.get_error_embed(language=language_dictionary, key="wallet_already_registered")
                await confirmation_message.delete()
                await ctx.channel.send(embed=embed)

        @economy_bot.command()
        async def wallet(ctx):
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            if configuration.command_channel:
                if ctx.channel.id != int(cf.clean_channel_id(channel_id=configuration.command_channel)):
                    return
            language_dictionary = language.select(configuration.language)
            wallet = database.read_wallet(guild_id=ctx.guild.id, user_id=ctx.author.id)
            if wallet:
                embed = cf.get_embed(title=language_dictionary["wallet"]["title"],
                                     description=language_dictionary["wallet"]["description"].format(
                                         round(wallet.amount, 2),
                                         configuration.currency_icon,
                                         configuration.currency_name),
                                     color=discord.Color.blurple())
            else:
                embed = cf.get_error_embed(language=language_dictionary, key="wallet_retrieval")
            await ctx.channel.send(embed=embed)

        def update_value(guild_id, item, value, language_dictionary):
            if database.update_configuration(guild_id=guild_id,
                                             item=item,
                                             value=value):
                return cf.get_done_embed(language=language_dictionary)
            else:
                return cf.get_error_embed(language=language_dictionary, key="cannot_update")

        async def check_user_activities(guild):
            while True:
                configuration = database.read_configuration(guild_id=guild.id)
                await asyncio.sleep(int(configuration.check_timer) * 60)
                logger.info(f"Checking {guild.id} {guild.name} activities")
                registered_users = list(database.read_registered_users(guild_id=guild.id))
                logger.debug(f"Found these registered users for guild {guild.id} {guild.name}")
                logger.debug(f"{str(registered_users)}")
                for registered_user in registered_users:
                    messages = 0
                    channels = list(map(lambda x: int(cf.clean_channel_id(x)), configuration.listening_channels))
                    for channel_id in channels:
                        start_check = datetime.datetime.utcnow() - datetime.timedelta(
                            minutes=int(configuration.check_timer))
                        channel = [x for x in guild.channels if x.id == channel_id][0]
                        logger.debug(
                            f"Searching user {registered_user.user_id} messages in channel {channel.id} for server {guild.id}")

                        async for message in channel.history(limit=500, oldest_first=False):
                            if message.author.id == int(registered_user.user_id):
                                if message.created_at < start_check:
                                    logger.debug(
                                        f"Found messages older than {start_check}, stopping iteration for channel {channel.id}")
                                    break
                                else:
                                    messages += 1

                        if messages >= int(configuration.check_maximum_messages):
                            messages = int(configuration.check_maximum_messages)
                            break

                    logger.info(
                        f"User {registered_user.user_id} wrote {messages} message in the last {configuration.check_timer} minutes")
                    if messages >= int(configuration.check_minimum_messages):
                        rate = messages / int(configuration.check_maximum_messages)
                        reward = float(rate * int(configuration.check_maximum_currency))
                        await database.wallet_operation(user_id=registered_user.user_id, guild_id=guild.id,
                                                        amount=reward, operation=Operation.ADDING)

        @economy_bot.command()
        async def pay(ctx, target_user, amount):
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            language_dictionary = language.select(configuration.language)

            configuration = database.read_configuration(guild_id=ctx.guild.id)
            if configuration.command_channel:
                if ctx.channel.id != int(cf.clean_channel_id(channel_id=configuration.command_channel)):
                    return

            try:
                amount = float(amount)
            except ValueError:
                embed = cf.get_error_embed(language=language_dictionary, key="value_not_numeric")
                await ctx.send(embed=embed)
                return

            if amount < 0:
                embed = cf.get_error_embed(language=language_dictionary, key="negative_value")
                await ctx.send(embed=embed)
                return

            registered_wallets = database.read_registered_users(guild_id=ctx.guild.id)
            registered_users_id = list(map(lambda x: int(x.user_id), registered_wallets))
            target_id = cf.clean_user_id(user_id=target_user)
            if target_id.isnumeric():
                target = await ctx.guild.fetch_member(member_id=int(cf.clean_user_id(user_id=target_user)))
            else:
                target = None
            if not target_user or not amount:
                embed = cf.get_error_embed(language=language_dictionary, key="configuration_arguments")
            elif ctx.author.id not in registered_users_id:
                embed = cf.get_error_embed(language=language_dictionary, key="wallet_retrieval")
            elif target is None or target.id not in registered_users_id:
                embed = cf.get_error_embed(language=language_dictionary, key="target_retrieval")
            else:
                user_wallet = database.read_wallet(user_id=ctx.author.id, guild_id=ctx.guild.id)

                if amount > float(user_wallet.amount):
                    embed = cf.get_error_embed(language=language_dictionary, key="insufficient_funds")
                else:
                    if configuration.payment_confirmation:
                        confirmation_message = await cf.send_private_confirmation(user=ctx.author,
                                                                                  title=language_dictionary["payment"][
                                                                                      "title"],
                                                                                  description=
                                                                                  language_dictionary["payment"][
                                                                                      "description"].format(amount,
                                                                                                            configuration.currency_icon,
                                                                                                            configuration.currency_name,
                                                                                                            target.name))

                        def check_confirmation(reaction, user):
                            return user == ctx.author and str(reaction.emoji) == "✅"

                        try:
                            reaction, user = await economy_bot.wait_for("reaction_add", timeout=30.0,
                                                                        check=check_confirmation)
                        except asyncio.TimeoutError:
                            await confirmation_message.delete()
                            embed = cf.get_error_embed(language=language_dictionary, key="timeout")
                        else:
                            await confirmation_message.delete()
                            await database.wallet_operation(user_id=ctx.author.id, guild_id=ctx.guild.id,
                                                            amount=float(amount),
                                                            operation=Operation.SUBTRACTING)
                            await database.wallet_operation(user_id=target.id, guild_id=ctx.guild.id,
                                                            amount=float(amount),
                                                            operation=Operation.ADDING)
                            embed = cf.get_payment_done_embed(language=language_dictionary, amount=amount,
                                                              user=ctx.author.id, target=target.id,
                                                              configuration=configuration)
                    else:
                        await database.wallet_operation(user_id=ctx.author.id, guild_id=ctx.guild.id,
                                                        amount=float(amount),
                                                        operation=Operation.SUBTRACTING)
                        await database.wallet_operation(user_id=target.id, guild_id=ctx.guild.id, amount=float(amount),
                                                        operation=Operation.ADDING)
                        embed = cf.get_payment_done_embed(language=language_dictionary, amount=amount,
                                                          user=ctx.author.id, target=target.id,
                                                          configuration=configuration)

            await ctx.send(embed=embed)

        @economy_bot.command()
        async def manage(ctx, target_user, amount):
            configuration = database.read_configuration(guild_id=ctx.guild.id)
            language_dictionary = language.select(configuration.language)
            if configuration.role:
                role = discord.utils.get(ctx.guild.roles, id=int(cf.clean_role_id(role_id=configuration.role)))
                if role not in ctx.author.roles:
                    return

            try:
                amount = float(amount)
            except ValueError:
                embed = cf.get_error_embed(language=language_dictionary, key="value_not_numeric")
                await ctx.send(embed=embed)
                return

            registered_wallets = database.read_registered_users(guild_id=ctx.guild.id)
            registered_users_id = list(map(lambda x: int(x.user_id), registered_wallets))
            target_id = cf.clean_user_id(user_id=target_user)
            if target_id.isnumeric():
                target = await ctx.guild.fetch_member(member_id=int(cf.clean_user_id(user_id=target_user)))
            else:
                target = None
            if not target_user or not amount:
                embed = cf.get_error_embed(language=language_dictionary, key="configuration_arguments")
            elif ctx.author.id not in registered_users_id:
                embed = cf.get_error_embed(language=language_dictionary, key="wallet_retrieval")
            elif target is None or target.id not in registered_users_id:
                embed = cf.get_error_embed(language=language_dictionary, key="target_retrieval")
            else:
                target_wallet = database.read_wallet(user_id=target.id, guild_id=ctx.guild.id)

                if 0 > amount and abs(amount) > float(target_wallet.amount):
                    amount = float(-target_wallet.amount)
                if amount > 0:
                    await database.wallet_operation(user_id=target.id, guild_id=ctx.guild.id,
                                                    amount=abs(amount),
                                                    operation=Operation.ADDING)
                else:
                    await database.wallet_operation(user_id=target.id, guild_id=ctx.guild.id,
                                                    amount=abs(amount),
                                                    operation=Operation.SUBTRACTING)

                embed = cf.get_done_embed(language=language_dictionary)

            await ctx.send(embed=embed)

        economy_bot.run(token)
