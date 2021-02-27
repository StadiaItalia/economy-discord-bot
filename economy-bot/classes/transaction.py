import datetime as datetime


class Transaction:
    def __init__(self, **args):
        self.guild_id = args.get("guild_id")
        self.user_id = args.get("user_id")
        self.target_id = args.get("target_id")
        self.amount = float(args.get("amount", 0))
        self.timestamp = datetime.datetime.now()

    def to_dict(self):
        return {
            "guild_id": self.guild_id,
            "user_id": self.user_id,
            "target_id": self.target_id,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_dict(obj):
        return Transaction(**obj)
