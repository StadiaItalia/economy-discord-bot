import discord


def get_embed(title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    return embed


def get_error_embed(language, key):
    title = language["error"]
    description = language["error_messages"][key]
    embed = get_embed(title=title, description=description, color=discord.Color.red())
    return embed


def get_done_embed(language):
    title = language["done"]
    embed = get_embed(title=title, description=language["done_description"], color=discord.Color.dark_green())
    return embed


def get_info_embed(command_prefix, language):
    embed = get_embed(title=language["info_description"]["title"],
                      description=language["info_description"]["description"],
                      color=discord.Colour.dark_green())
    embed.add_field(name=f"{command_prefix}info",
                    value=language["info_description"]["info"],
                    inline=False)
    embed.add_field(name=f"{command_prefix}config",
                    value=language["info_description"]["config"],
                    inline=False)
    embed.add_field(name=f"{command_prefix}config <{language['prefix']}> <{language['value']}>",
                    value=language["info_description"]["config_update"],
                    inline=False)
    embed.add_field(name=language["info_description"]["legend"],
                    value=language["info_description"]["legend_description"],
                    inline=False)
    return embed


def get_configuration_embed(command_prefix, configuration, language):
    embed = get_embed(title=language["configuration_description"]["title"],
                      description=language["configuration_description"]["description"],
                      color=discord.Color.dark_gold())

    embed.add_field(name=f"{command_prefix}config language <it|en>",
                    value=f"{language['current'].format(configuration.language)}\n"
                          f"{language['configuration_description']['language']}",
                    inline=False)

    embed.add_field(name=f"{command_prefix}config role <@role|disable>",
                    value=f"{language['current'].format(configuration.role if configuration.role else 'unset')}\n"
                          f"{language['configuration_description']['role']}",
                    inline=False)

    embed.add_field(name=f"{command_prefix}config command_channel <#channel|disable>",
                    value=f"{language['current'].format(configuration.command_channel if configuration.command_channel else 'unset')}\n"
                          f"{language['configuration_description']['command_channel']}",
                    inline=False)

    embed.add_field(name=f"{command_prefix}config listening_channels <#channel[]|disable>",
                    value=f"{language['current'].format(configuration.listening_channels if configuration.listening_channels else 'unset')}\n"
                          f"{language['configuration_description']['listening_channels']}",
                    inline=False)

    embed.add_field(name=f"{command_prefix}config currency_name <name>",
                    value=f"{language['current'].format(configuration.currency_name)}\n"
                          f"{language['configuration_description']['currency_name']}",
                    inline=False)

    embed.add_field(name=f"{command_prefix}config currency_icon <emoji>",
                    value=f"{language['current'].format(configuration.currency_icon)}\n"
                          f"{language['configuration_description']['currency_icon']}",
                    inline=False)

    embed.add_field(name=f"{command_prefix}config payment_confirmation <on|off>",
                    value=f"{language['current'].format(configuration.payment_confirmation)}\n"
                          f"{language['configuration_description']['payment_confirmation']}",
                    inline=False)

    embed.add_field(name=f"{command_prefix}config check_maximum_messages <value>",
                    value=f"{language['current'].format(configuration.check_maximum_messages)}\n"
                          f"{language['configuration_description']['check_maximum_messages']}",
                    inline=False)

    embed.add_field(name=f"{command_prefix}config check_minimum_messages <value>",
                    value=f"{language['current'].format(configuration.check_minimum_messages)}\n"
                          f"{language['configuration_description']['check_minimum_messages']}",
                    inline=False)

    embed.add_field(name=f"{command_prefix}config check_maximum_currency <value>",
                    value=f"{language['current'].format(configuration.check_maximum_currency)}\n"
                          f"{language['configuration_description']['check_maximum_currency']}",
                    inline=False)

    embed.add_field(name=f"{command_prefix}config check_timer <value>",
                    value=f"{language['current'].format(configuration.check_timer)}\n"
                          f"{language['configuration_description']['check_timer']}",
                    inline=False)
    return embed


def clean_channel_id(channel_id):
    return channel_id.replace("<#", "").replace(">", "")


def clean_role_id(role_id):
    return role_id.replace("<@&", "").replace(">", "")


def clean_user_id(user_id):
    return user_id.replace("<@!", "").replace(">", "")
