languages = {
    "en": {
        "prefix": "prefix",
        "value": "value",
        "current": "Current: {}",
        "info_description": {
            "title": "Command list",
            "description": "Command list for Economy Bot",
            "info": "Show this message",
            "config": "Show the actual configuration for your server",
            "config_update": "Update the selected prefix configuration",
            "legend": "Legend",
            "legend_description": "< > = mandatory parameter"
        },
        "configuration_description": {
            "title": "Configuration",
            "description": "Configuration summary",
            "language": "Language",
            "role": "Role the bot will listen to for configuration commands",
            "command_channel": "Channel the bot will listen to for configuration commands",
            "listening_channels": "Channels the bot will listen to for checking user activities",
            "currency_name": "Your server currency name",
            "currency_icon": "Your server currency icon",
            "check_maximum_messages": "ADVANCED, see repository through info command",
            "check_minimum_messages": "ADVANCED, see repository through info command",
            "check_maximum_currency": "ADVANCED, see repository through info command",
            "check_timer": "ADVANCED, see repository through info command",
            "payment_confirmation": "Wheter to show a confirmation message for assigning and exchanging currencies"
        }
    },

    "it": {
        "prefix": "prefisso",
        "value": "valore",
        "current": "Corrente: {}",
        "info_description": {
            "title": "Lista comandi",
            "description": "Lista comandi per Economy Bot",
            "info": "Mostra questo messaggio",
            "config": "Mostra la configurazione attuale per il tuo server",
            "config_update": "Aggiorna la configurazione del prefisso indicato",
            "legend": "Legenda",
            "legend_description": "< > = parametro obbligatorio"
        },
        "configuration_description": {
            "title": "Configurazione",
            "description": "Riassunto della configurazione",
            "language": "Lingua",
            "role": "Ruolo che il bot ascoltera per gli aggiornamenti di configurazione",
            "command_channel": "Canale che il bot controllera per gli aggiornamenti di configurazione",
            "listening_channels": "Lista di canali che il bot monitorera per le attivita utente",
            "currency_name": "Nome della valuta",
            "currency_icon": "Icona della valuta",
            "check_maximum_messages": "AVANZATO, controllare il repository presente nel comando info",
            "check_minimum_messages": "AVANZATO, controllare il repository presente nel comando info",
            "check_maximum_currency": "AVANZATO, controllare il repository presente nel comando info",
            "check_timer": "AVANZATO, controllare il repository presente nel comando info",
            "payment_confirmation": "Mostrare o meno una conferma per l'assegnazione e lo scambio di valuta"
        }
    }
}


def select(key):
    language = languages[key]
    return language
