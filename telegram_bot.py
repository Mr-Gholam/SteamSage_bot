# import telebot
# from dotenv import load_dotenv
# from telebot import types
# import requests
# import os

# load_dotenv()

# TELEGRAM_KEY = os.getenv("TELEGRAM_API")
# RAWG_KEY = os.getenv("RAWG_APIKEY")

# # Replace 'YOUR_API_TOKEN' with your actual bot token
# bot = telebot.TeleBot(TELEGRAM_KEY)

# @bot.message_handler(commands=['start'])
# def start(message):
#     button_recommender = types.InlineKeyboardButton('Recommend a Game', callback_data='recommend')
#     button_Contact = types.InlineKeyboardButton('Contact Admin', callback_data='contact')
#     button_About = types.InlineKeyboardButton('About Me', callback_data='about')
#     button_Info = types.InlineKeyboardButton('Game Info', callback_data='gameInfo')

#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(button_recommender)
#     keyboard.add(button_Contact)
#     keyboard.add(button_About)
#     keyboard.add(button_Info)

#     bot.send_message(message.chat.id, "Welcome to Game Recommendation Bot \n How can i help you ?  ", reply_markup=keyboard)

# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     if call.data == "recommend":
#         bot.send_message(call.message.chat.id, "Recommend a Game")
#         bot.delete_message(call.message.chat.id, call.message.id)
#     if call.data == "contact":
#         bot.send_message(call.message.chat.id, "Contact Admin")
#         bot.delete_message(call.message.chat.id, call.message.id)
#     if call.data == "about":
#         bot.send_message(call.message.chat.id, "About Me")
#         bot.delete_message(call.message.chat.id, call.message.id)
#     if call.data == "gameInfo":
#         markup = types.ForceReply(selective=False)
#         bot.send_message(call.message.chat.id, "What is the name of the game?",reply_markup=markup)
#     elif call.data == "bar":
#         bot.answer_callback_query(call.id, "Answer is bar")


# #Bottom 1
# @bot.message_handler(func=lambda message: message.text == "Bottom 1")
# def button1(message):
#     bot.send_message(message.chat.id, "U select bottom 1")

# #Bottom 2
# @bot.message_handler(func=lambda message: message.text == "Bottom 2")
# def button2(message):
#     bot.send_message(message.chat.id, "U select bottom 2")


# @bot.message_handler(commands=['info'])
# def send_info(message):
#     bot.reply_to(message, "This is a simple Telegram bot implemented in Python.")

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     if (
#         message.reply_to_message is not None and
#         message.reply_to_message.text == "What is the name of the game?"
#     ):
#         r = requests.get(f"https://api.rawg.io/api/games?key={RAWG_KEY}&search={message.text}")
#         data = r.json()
#         bot.send_photo(message.chat.id, data["results"][0]["background_image"], caption="test")
#     else:
#         bot.reply_to(message, message.text)

# bot.polling()


import os
from dotenv import load_dotenv
import telebot
# from Scripts.langchain_bot import chat_with_langchain

load_dotenv()
telegram_api = os.getenv("TELEGRAM_API")
if telegram_api is None:
    raise ValueError("TELEGRAM_API environment variable is not set.")
bot = telebot.TeleBot(telegram_api)


@bot.message_handler(commands=["start"])
def send_welcome(msg):
    bot.reply_to(msg, "👋 Hi! I’m GameBot. Ask me for game recommendations!")


@bot.message_handler(commands=["Dota2_stat"])
def send_info(msg):
    print(msg.text)
    bot.reply_to(msg, "👋this is information :)")


# @bot.message_handler(func=lambda m: True)
# def handle_message(msg):
#     reply = chat_with_langchain(msg.text)
#     bot.reply_to(
#         msg, reply if reply is not None else "Sorry, I couldn't generate a response."
#     )


print("app is running ")
bot.infinity_polling()
