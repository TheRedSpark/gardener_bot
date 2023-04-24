# V4.0 Live 23.06.2022
# credits to https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py
import logging

import mysql.connector
import time
from telegram import __version__ as TG_VER, ReplyKeyboardMarkup  # v20

import variables as v

ort = "home"
database = "Gardener"
live = True
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"Dieses Beispiel ist nicht kompatibel mit deiner PTB version {TG_VER}."
        f"{TG_VER} version von diesem Beispiel, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

B_START, B_FRAGE, B_ANTWORT, B_ENTSCHEIDUNG, B_CLOSEUP = range(5)

giesen_vara = {'Menge': 0,
               'Pflanze': ''}

pflanzen_config = {'Wassermenge': 0,
                   'Lichtzyklus': '8-20Uhr',
                   'isLicht': 'False',
                   'Lüfterzyklus': '30min',
                   'isLüfter': 'False',
                   'Wasserstand': '44%',
                   'Luftfeuchtigkeit': '40%',
                   'Temperatur': '28C°',
                   }


def userlogging(user_id, username, message_chat_id, message_txt, message_id, first_name, last_name, land_code):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    time_sql = time.strftime("%Y-%m-%d %H:%M:%S")

    sql_maske = "INSERT INTO `Gardener`.`Messages` (`Time`,`User_Id`,`Username`,`Chat_Id`,`Message_Text`," \
                "`Message_Id`,`First_Name`,`Last_Name`,`Land_Code`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); "
    data_n = (
        time_sql, user_id, username, message_chat_id, message_txt, message_id, first_name, last_name, land_code)
    my_cursor.execute(sql_maske, data_n)
    mydb.commit()
    my_cursor.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    await update.message.reply_text(
        'Hallo und willkommen bei dem fantastischen alleskönnenden Telegram Bot (FAT Bot) \n'
        'Benutze /help um diese Nachricht anzuzeigen \n'
        'Benutze /wasser oder /w um dir die aktuelle Feuchtigkeit deiner Pflanzen auszugeben. \n'
        'Benutze /licht oder /li um den Pflanzen von der ferne Wasser zu geben \n'
        'Benutze /luft oder /lu um den Pflanzen von der ferne Wasser zu geben \n'
        'Benutze /bewasserung oder /b um den Pflanzen von der ferne Wasser zu geben \n'
        'Benutze /plan oder /p um den Pflanzen von der ferne Wasser zu geben \n'
        'Benutze /qualitat oder /q um die Luftqualität anzuzeigen. \n'
        'Benutze /status oder /s um die Luftqualität anzuzeigen. \n'
        'Benutze /photo oder /p um die Luftqualität anzuzeigen. \n')


async def wasser(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    await context.bot.send_message(update.effective_user.id,
                                   f'Die Pflanze wurde ___ das letzte mal gegossen')  # ToDo letzten gießstand einführen
    await context.bot.send_message(update.effective_user.id,
                                   f'Hier wird dir zukünftig der Wasserstand angezeigt')  # Todo Wasser Sensor auslesen


async def licht(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    await context.bot.send_message(update.effective_user.id,
                                   f'Hier wird dir zukünftig angezeigt ob das Licht an ist oder nicht')  # Todo Licht Sensor auslesen


async def luft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    await context.bot.send_message(update.effective_user.id,
                                   f'Hier wird dir zukünftig angezeigt ob die Lüftüng an ist oder nicht an ist oder nicht')  # Todo Licht Sensor auslesen


async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    await context.bot.send_message(update.effective_user.id,
                                   f'Hier bekommt du eine auswertung was der Plan für die nächsten Aktionen ist')  # Todo Licht Sensor auslesen


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    await context.bot.send_message(update.effective_user.id,
                                   f'Die eingestellte Wassermenge ist :{pflanzen_config["Wassermenge"]} \n'
                                   f'Der eingestellte Lichtzyklus ist: {pflanzen_config["Lichtzyklus"]} \n'
                                   f'Der eingestellte Lüfterzyklus ist: {pflanzen_config["Lüfterzyklus"]} \n'
                                   f'Der eingestellte Lichtzyklus ist: {pflanzen_config["Lüfterzyklus"]} \n')  # Todo Config anpassen

pflanzen_config = {'Wassermenge': 0,
                   'Lichtzyklus': '8-20Uhr',
                   'isLicht': 'False',
                   'Lüfterzyklus': '30min',
                   'isLüfter': 'False',
                   'Wasserstand': '44%',
                   'Luftfeuchtigkeit': '40%',
                   'Temperatur': '28C°',
                   }

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)

    await context.bot.send_photo(update.effective_user.id, 'meme.jpg', 'Das ist eine premium Meme')


async def qualitat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    await context.bot.send_message(update.effective_user.id,
                                   f'Hier bekommt du eine auswertung von den letzten Luftdaten')  # Todo Licht Sensor auslesen


async def b_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    giesen_vara.clear()
    await update.message.reply_text(f"Wie viel ml möchtest du die Pfanze(n) gießen lassen? \n"
                                    f"Du kannt das Menu jederzeit abbrechen indem du /cancel benutzt",
                                    reply_markup=ReplyKeyboardRemove())
    return B_FRAGE


async def b_frage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    antwort = update.message.text.lower()
    try:
        antwort = int(antwort)
    except ValueError:
        await context.bot.send_message(update.effective_user.id,
                                       f'Leider hast du keine ganze Zahl eingegeben bitte versuche es erneut.')
        await context.bot.send_message(update.effective_user.id,
                                       f'Das Menu wurde abgebrochen du kannst es mit /b oder /bewasserung gerne noch einmal versuchen.')
        return ConversationHandler.END

    zu_giesen_in_ml = antwort
    giesen_vara['Menge'] = zu_giesen_in_ml
    await context.bot.send_message(update.effective_user.id,
                                   f'Du wirst {giesen_vara["Menge"]} ml giesen')
    reply_keyboard = [["Pflanze 1", "Pflanze 2", "Pflanze 3", "Pflanze 4"], ["Alle Pflanzen"]]
    await update.message.reply_text(
        "Sub-Menu",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Bitte wähle"
        ),
    )

    return ConversationHandler.END
    # return B_ANTWORT


async def b_antwort(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    antwort = update.message.text.lower()

    return B_FRAGE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Du hast das Menu erfolgreich abgebrochen", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)

    await update.message.reply_text('Kein Befehl erkannt, bitte nutze einen Befehl unter /help')


def main() -> None:
    application = Application.builder().token(v.api_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start, filters=filters.User(v.allown_ids)))
    application.add_handler(CommandHandler(["wasser", "w"], wasser, filters=filters.User(v.allown_ids)))
    application.add_handler(CommandHandler(["licht", "li"], licht, filters=filters.User(v.allown_ids)))
    application.add_handler(CommandHandler(["luft", "lu"], luft, filters=filters.User(v.allown_ids)))
    application.add_handler(CommandHandler(["plan", "p"], plan, filters=filters.User(v.allown_ids)))
    application.add_handler(CommandHandler(["qualitat", "q"], qualitat, filters=filters.User(v.allown_ids)))
    application.add_handler(CommandHandler(["status", "s"], status, filters=filters.User(v.allown_ids)))
    application.add_handler(CommandHandler(["photo", "p"], photo, filters=filters.User(v.allown_ids)))
    # application.add_handler(CommandHandler(["bewässerung", "b"], wasser))
    # application.add_handler(CommandHandler("abstand", abstand))

    conv_handler_bewasserung = ConversationHandler(
        entry_points=[CommandHandler(["bewasserung", "b"], b_start)],
        states={
            B_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_start)],
            B_FRAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_frage)],
            B_ANTWORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_antwort)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler_bewasserung)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
