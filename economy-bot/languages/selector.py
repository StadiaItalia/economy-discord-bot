languages = {
    "en": {
        "prefix": "prefix",
        "value": "value",
        "info_description": {
            "title": "Command list",
            "description": "Command list for Economy Bot",
            "info": "Show this message",
            "config": "Show the actual configuration for your server",
            "config_update": "Update the selected prefix configuration",
            "legend": "Legend",
            "legend_description": "< > = mandatory parameter"
        }
    },

    "it": {
        "prefix": "prefisso",
        "value": "valore",
        "info_description": {
            "title": "Lista comandi",
            "description": "Lista comandi per Economy Bot",
            "info": "Mostra questo messaggio",
            "config": "Mostra la configurazione attuale per il tuo server",
            "config_update": "Aggiorna la configurazione del prefisso indicato",
            "legend": "Legenda",
            "legend_description": "< > = parametro obbligatorio"
        }
    }
}


def select(key):
    language = languages[key]
    return language
