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
        },
        "registration": {
            "title": "Wallet registration",
            "description": "Do you wanna create your personal wallet and start gaining the server currency?"
        },
        "wallet": {
            "title": "Personal wallet",
            "description": "You have {} {} {} in your wallet"
        },
        "payment": {
            "title": "Payment",
            "description": "You're about to pay {} {} {} to {}",
            "payment_from": "Paymento from {}",
            "payment_to": "Payment to {}"
        },
        "done": "Done",
        "done_description": "Command executed",
        "error": "Error",
        "error_messages": {
            "configuration_parameter": "Configuration parameter not recognized",
            "configuration_arguments": "Number of arguments passed incorrect",
            "language_not_present": "Your chosen language is not yet loaded, please use another",
            "cannot_update": "Cannot update the configuration right now, try later",
            "role_not_present": "The selected role is not defined in the server",
            "channel_not_present": "The selected channel is not present in the server",
            "value_not_numeric": "The passed value is not numeric",
            "value_greater_zero": "The passed value must be greater than 0",
            "incorrect_value": "Passed value comprehension impossibile, please check",
            "timeout": "Timeout",
            "wallet_already_registered": "Wallet already registered",
            "wallet_retrieval": "Cannot retrieve wallet, make sure to register beforehand",
            "target_retrieval": "Cannot retrieve target wallet, make sure the user is registered",
            "insufficient_funds": "Insufficient funds"
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
        },
        "registration": {
            "title": "Registrazione wallet",
            "description": "Vuoi creare il tuo wallet e cominciare ad accumulare la valuta del server?"
        },
        "wallet": {
            "title": "Wallet personale",
            "description": "Hai {} {} {} nel tuo wallet"
        },
        "payment": {
            "title": "Pagamento",
            "description": "Stai per pagare {} {} {} a {}",
            "payment_from": "Pagamento da {}",
            "payment_to": "Pagamento a {}"
        },
        "done": "Eseguito",
        "done_description": "Comando eseguito",
        "error": "Errore",
        "error_messages": {
            "configuration_parameter": "Parametro di configurazione non riconosciuto",
            "configuration_arguments": "Numero di argomenti passati insufficiente",
            "language_not_present": "Hai scelto un linguaggio non ancora presente, prova con un altro",
            "cannot_update": "Non e stato possibile aggiornare la configurazione, riprovare piu tardi",
            "role_not_present": "Il ruolo selezionato non e presente all'interno del server",
            "channel_not_present": "Il canale selezionato e presente all'interno del server",
            "value_not_numeric": "Il valore passato non e numerico",
            "value_greater_zero": "Il valore passato deve essere maggiore di 0",
            "incorrect_value": "Impossibile comprendere il valore passato, verificare",
            "timeout": "Timeout",
            "wallet_already_registered": "Wallet gia esistente",
            "wallet_retrieval": "Impossibile recuperare il wallet, accertarsi di essersi registrati prima",
            "target_retrieval": "Impossibile recuperare il wallet di destinazione, accertarsi che l'utente sia registrato",
            "insufficient_funds": "Fondi insufficienti"
        }
    }
}


def select(key):
    language = languages[key]
    return language


def get_languages():
    return languages.keys()
