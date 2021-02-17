class Wallet:
    def __init__(self, **args):
        self.guild_id = args.get("guild_id")
        self.user_id = args.get("user_id")
        self.wallet = args.get("amount", 0)

    def to_dict(self):
        return {
            "guild_id": self.guild_id,
            "user_id": self.user_id,
            "amount": self.wallet
        }

    @staticmethod
    def from_dict(obj):
        return Wallet(**obj)
