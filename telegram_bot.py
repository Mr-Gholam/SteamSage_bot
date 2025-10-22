
import os
from dotenv import load_dotenv
import telebot
from telebot import types
import asyncio

from Scripts import send_dota2_stat, delete_img,lyrics,create_tts,delete_tts,Database

db = Database("Database/users.db")
db.create_database()


load_dotenv()
TELEGRAM_API = os.getenv("TELEGRAM_API")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
if TELEGRAM_API is None:
    raise ValueError("TELEGRAM_API environment variable is not set.")
bot = telebot.TeleBot(TELEGRAM_API)


@bot.message_handler(commands=["start"])
def send_welcome(msg):
    username= msg.chat.username
    # 0 = English
    # 1 = French
    lang = 0 
    db.create_user(username,lang)
    tts = types.InlineKeyboardButton('text to speech', callback_data='TTS')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(tts)
    bot.reply_to(msg, "Hi! I’m GameBot. Ask me for game recommendations!",reply_markup=keyboard)


@bot.message_handler(commands=["Dota2_stat"])
def send_dota_stat(msg):
    result = send_dota2_stat(msg.text)

    if result[1]:
        try:
            with open(result[1], "rb") as photo:
                bot.send_photo(msg.chat.id, photo, caption=result[0])
                delete_img(result[1])
        except FileNotFoundError:
            bot.reply_to(
                msg.chat.id,
                "Sorry, the image file was not found at the specified path.",
            )
        except Exception as e:
            bot.reply_to(msg.chat.id, f"An error occurred while sending the photo: {e}")
    else:
        bot.send_message(msg.chat.id, result[0])


@bot.message_handler(commands=["music"])
def send_music(msg):
    try:
        with open("music/soad.jpg", "rb") as photo:
            cover = bot.send_photo(msg.chat.id, photo, caption=lyrics)
        with open("music/soad- Vicinity Of Obscenity.mp3", "rb") as music:
            bot.send_audio(
                msg.chat.id,
                music,
                caption="System Of A Down - Vicinity Of Obscenity",
                reply_to_message_id=cover.message_id,
            )
    except FileNotFoundError:
        bot.send_message(
            msg.chat.id,
            "Sorry, the music file was not found at the specified path.",
        )
    except Exception as e:
        bot.send_message(msg.chat.id, f"An error occurred while sending the music: {e}")

@bot.message_handler(commands=["change_language"])
def change_lang(msg):
    try:
        newLang = db.change_user_lang(msg.chat.username)
        response=""
        if newLang ==1 :
            response = f"Language has been changed from English to french"
        else:
           response = "Language has been changed from French to English"
        bot.send_message(msg.chat.id,response)
    except Exception as e:
        bot.send_message(msg.chat.id, f"An error occurred while changing Language: {e}")

@bot.message_handler(commands=["admin"])
def talk_to_admin(msg):
    bot.send_message(msg.chat.id, f"You are sending a message to admin",reply_markup= types.ForceReply(selective=False))





@bot.message_handler(func=lambda message: message.reply_to_message is not None and message.reply_to_message.text == "You are sending a message to admin")
def handle_message(msg):
    if ADMIN_CHAT_ID is None:
        bot.reply_to(msg, "Admin chat id is not configured.")
        return
    bot.send_message(ADMIN_CHAT_ID, f"User:@{msg.chat.username}\nMessage:{msg.text}")
    bot.reply_to(msg,"Admin received your message")



# @bot.message_handler(func=lambda m: True)
# def handle_message(msg):
#     lang = db.get_user_lang(msg.chat.username)
#     tts = types.InlineKeyboardButton('text to speech', callback_data='TTS')
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(tts)
#     reply = chat_with_langchain(msg.text)
#     if lang == 1 :
#         reply = asyncio.run(translator_function(reply))
#         bot.reply_to(
#             msg, reply if reply is not None else "Sorry, I couldn't generate a response.",
#             reply_markup=keyboard
#         )
#     else:
#         bot.reply_to(
#             msg, reply if reply is not None else "Sorry, I couldn't generate a response.",
#             reply_markup=keyboard
#         )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "TTS":
        text = call.message.text
        username = call.from_user.username
        messageId= call.message.message_id
        chat_id = str(call.message.chat.id)
        lang = db.get_user_lang(username)
        fileAddress = create_tts(text,username,messageId,lang)
        try:
            with open(fileAddress, "rb") as tts:
             bot.send_voice(
                chat_id,
                tts,
                reply_to_message_id=messageId,
            )
            delete_tts(fileAddress)
        except FileNotFoundError:
                bot.send_message(
                chat_id,
                "Sorry, the text to speech file was not found at the specified path.",
            )
        except Exception as e:
            bot.send_message(chat_id, f"An error occurred while sending the music: {e}")
            # bot.send_audio(chat_id,fileAddress)
            # bot.send_message(call.message.chat.id, "Recommend a Game")
        
    elif call.data == "bar":
        bot.answer_callback_query(call.id, "Answer is bar")



print("app is running ")
bot.infinity_polling()
