from boilerplate.mongodatabase import MongoDatabase
from classes.bot_configuration import BotConfiguration
from classes.wallet import Wallet
from pymongo import MongoClient


class BotDatabase(MongoDatabase):
    def __init__(self, host, user, password, database, configuration_repository, wallet_repository, logger):
        self.logger = logger
        self.init_database(host=host, user=user, password=password, db_name=database)
        self.configuration_repository = self.get_collection(configuration_repository)
        self.wallet_repository = self.get_collection(wallet_repository)

    def init_database(self, host, user, password, db_name):
        self.database = MongoClient(
            host.replace("<username>", user).replace("<password>", password).replace("<dbname>", db_name))[db_name]
        self.logger.debug(f"Connected to {self.database}")

    def read_configuration(self, guild_id):
        configuration = self.configuration_repository.find_one({"guild_id": guild_id})
        if configuration:
            self.logger.debug(f"Configuration found: {str(configuration)}")
            return BotConfiguration.from_dict(configuration)
        else:
            self.logger.debug(f"Couldn't find any configuration for guild {guild_id}")
            return None

    def remove_configuration(self, guild_id):
        deleted = self.configuration_repository.delete_many({"guild_id": guild_id}).deleted_count
        if deleted.deleted_count > 0:
            self.logger.info(f"Deleted {deleted} configurations for guild {guild_id}")
            return True
        else:
            self.logger.info(f"Couldn't delete any configuration for guild {guild_id}")
            return False

    def update_configuration(self, guild_id, item, value):
        updated = self.configuration_repository.update_many({"guild_id": guild_id}, {"$set": {item: value}})
        if updated.modified_count > 0:
            self.logger.info(f"Updated configuration for guild {guild_id}")
            self.logger.debug(f"==> updated item {item} with value {value}")
            return True
        else:
            self.logger.info(f"Couldn't update configuration for guild {guild_id}")
            self.logger.debug(f"==> tried updating item {item} with value {value}")
            return False

    def create_configuration(self, guild):
        previous_configuration = self.read_configuration(guild_id=guild.id)
        if previous_configuration:
            self.logger.info(f"Configuration for guild {guild.id} already existing")
            self.logger.debug(f"==> {str(previous_configuration)}")
            return previous_configuration
        else:
            bot_configuration = BotConfiguration(guild_id=guild.id, guild_name=guild.name)
            self.logger.info(f"Creating configuration for guild {guild.id}")
            self.configuration_repository.insert_one(bot_configuration.to_dict())
            return bot_configuration

    def read_registered_users(self, guild_id):
        registered_users = map(lambda x: Wallet.from_dict(x), self.wallet_repository.find({"guild_id": guild_id}))
        return registered_users

    def read_wallet(self, user_id, guild_id):
        wallet = self.wallet_repository.find_one({"guild_id": guild_id, "user_id": user_id})
        if wallet:
            self.logger.debug(f"Wallet found: {str(wallet)}")
            return Wallet.from_dict(wallet)
        else:
            self.logger.debug(f"Couldn't find any wallet for user {user_id} in guild {guild_id}")
            return None

    def create_wallet(self, user_id, guild_id):
        wallet = self.read_wallet(user_id=user_id, guild_id=guild_id)
        if wallet:
            self.logger.info(f"Registration for user {user_id} in guild {guild_id} already existing")
            self.logger.debug(f"==> {str(wallet)}")
            return False
        else:
            wallet = Wallet(guild_id=guild_id, user_id=user_id)
            self.logger.info(f"Creating registration for user {user_id} in guild {guild_id}")
            self.wallet_repository.insert_one(wallet.to_dict())
            return True

    # Operation is a string type. It can be "Adding" or "Subtracting". 
    # You can perform better the operation like increase the money or exchange it
    async def automatic_operation(self, user_id, guild_id, amount, operation):
        wallet = self.read_wallet(user_id=user_id, guild_id=guild_id)
        if wallet:
            self.logger.info(f"{operation}  {amount} for user {user_id} in guild {guild_id}")
            mathFunction = {"Adding":sum([wallet.amount,amount]), "Subtract":sum([wallet.amount,-amount])}
            total_amount = mathFunction[operation]
            self.logger.debug(f"Total amount: {total_amount}")
            self.wallet_repository.update_one({"guild_id": guild_id, "user_id": user_id},
                                              {"$set": {"amount": total_amount}})
