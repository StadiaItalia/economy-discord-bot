import os

from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv("ECONOMY_DISCORD_TOKEN")

logging_level = os.getenv("ECONOMY_LOGGING_LEVEL")

database_user = os.getenv("ECONOMY_DATABASE_USER")
database_password = os.getenv("ECONOMY_DATABASE_PASSWORD")
database__name = os.getenv("ECONOMY_DATABASE")
database_host = os.getenv("ECONOMY_DATABASE_HOST")
database_configuration_collection = os.getenv("ECONOMY_DATABASE_CONFIGURATION_COLLECTION")
