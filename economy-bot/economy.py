from boilerplate.logger import Logger

import modules.configuration as configuration
from classes.bot_database import BotDatabase
from classes.bot_economy import EconomyBot

logger = None
database = None

if configuration.logging_level:
    logger = Logger(level=configuration.logging_level)
else:
    raise Exception("Environment variable ECONOMY_LOGGING_LEVEL not found")

if configuration.database_host and configuration.database_user and configuration.database_password and configuration.database_name and configuration.database_configuration_collection:
    try:
        database = BotDatabase(host=configuration.database_host, user=configuration.database_user,
                               database=configuration.database_name, password=configuration.database_password,
                               configuration_repository=configuration.database_configuration_collection,
                               wallet_repository=configuration.database_wallet_collection,
                               transaction_repository=configuration.database_transactions_collection,
                               logger=logger)
    except Exception as ex:
        raise Exception(f"Exception during database startup: {ex}")
else:
    raise Exception("Database environment variables not properly configured, please check documentation")

if configuration.discord_token:
    EconomyBot.start_bot(token=configuration.discord_token, database=database, logger=logger)
else:
    raise Exception("Environment variable ECONOMY_DISCORD_TOKEN not found")
