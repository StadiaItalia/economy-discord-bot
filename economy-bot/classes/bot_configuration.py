class BotConfiguration:
    def __init__(self, **args):
        self.guild_id = args.get("guild_id")
        self.guild_name = args.get("guild_name")
        self.language = args.get("language", "en")
        self.role = args.get("role", None)
        self.command_channel = args.get("command_channel", None)
        self.listening_channels = args.get("listening_channels", None)
        self.currency_name = args.get("currency_name", "DiscordCoin")
        self.currency_icon = args.get("currency_icon", "🪙")
        self.check_maximum_messages = args.get("check_maximum_messages", 10)
        self.check_minimum_messages = args.get("check_minimum_messages", 5)
        self.check_maximum_currency = args.get("check_maximum_currency", 5)
        self.check_timer = args.get("check_timer", 5)
        self.payment_confirmation = args.get("payment_confirmation", True)

    def to_dict(self):
        return {
            "guild_id": self.guild_id,
            "guild_name": self.guild_name,
            "language": self.language,
            "role": self.role,
            "command_channel": self.command_channel,
            "listening_channels": self.listening_channels,
            "currency_name": self.currency_name,
            "currency_icon": self.currency_icon,
            "check_maximum_messages": self.check_maximum_messages,
            "check_minimum_messages": self.check_minimum_messages,
            "check_maximum_currency": self.check_maximum_currency,
            "check_timer": self.check_timer,
            "payment_confirmation": self.payment_confirmation
        }

    @staticmethod
    def from_dict(obj):
        return BotConfiguration(**obj)
