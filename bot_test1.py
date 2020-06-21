import telebot
from telebot import types
import random
import requests
import json
import config

photo_number = 0
random_digit = 0

bot = telebot.TeleBot(config.token)
bank_api = config.url_currency


def resp_bank(api):  # function which read data  and deserialize them from bank API
    response = requests.get(api)
    deserial = json.loads(response.text)
    return deserial


data = resp_bank(bank_api)  # variable equals data acquired from bank api


def exchange_valute(value, from_first, to_second):  # function which converts valute
    first_value = data["Valute"][from_first]["Value"] / data["Valute"][from_first]["Nominal"]
    second_value = data["Valute"][to_second]["Value"] / data["Valute"][to_second]["Nominal"]
    return value * int(first_value) / int(second_value)

# неиспользуемые данные для инлайновых сообщений; нужны, чтобы не забыть
# keyboard
# keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
# unit1 = types.KeyboardButton("How is it going bot?")
# unit2 = types.KeyboardButton("Type down: Hello")
# keyboard.add(unit1, unit2)

# #keyboardInline
# keyboard = types.InlineKeyboardMarkup(row_width=1)
# unit_1 = types.InlineKeyboardButton("1", callback_data="1")


@bot.message_handler(commands=['start'])  # handle the command "Start"
def start_welcome(message):
    global random_digit  # variable to initialise a random value
    random_digit = str(random.randint(1, 3))  # random value from 1 to 3. Why we use it? Look below
    image1 = open('static/start.jpg', 'rb')  # start image. Yes, it's anime picture...
    bot.send_photo(message.chat.id, image1)  # send the photo to a user
    keyboardIn1 = types.InlineKeyboardMarkup(row_width=3)  # create an inline keyboard with 3 values
    unit_1 = types.InlineKeyboardButton("1", callback_data="1")
    unit_2 = types.InlineKeyboardButton("2", callback_data="2")
    unit_3 = types.InlineKeyboardButton("3", callback_data="3")
    keyboardIn1.add(unit_1, unit_2, unit_3)

    bot.send_message(message.chat.id,  # start message by bot
                     "Hi, {}!\n"
                     "I'm a bot named {}.\n"
                     "U can send me next comands \n"
                     "1) /exchange, "
                     "to check the currency today "
                     "according to central bank of RUSSIA FEDERUSSIA \n"
                     "2) /about, to know some information"
                     .format(message.from_user.first_name, bot.get_me().first_name))

    bot.send_message(message.chat.id,  # second message following the first one
                     "So u can send me a digit between 1 and 3 "
                     "to get some solar power \n"
                     "(05 region).",
                     reply_markup=keyboardIn1)


@bot.message_handler(commands=['exchange'])  # handle with "exchange" command
def exchange(message):  # just a description of the command
    bot.send_message(message.chat.id, "U can choose currency exchange "
                                      "of these currencies:\n"
                                      "AUD, AZN, GBP, AMD, BYN, BGN, BRL, HUF,"
                                      "HKD, DKK, USD, EUR, INR, KZT, CAD, KGS,"
                                      "CNY, MDL, NOK, PLN, RON, XDR, SGD, TJS,"
                                      "TRY, TMT, UZS, UAH, CZK, SEK, CHF, ZAR, "
                                      "KRW, JPY\n"
                                      "So, write down an expression in a next way: \n"
                                      "11 USD EUR")


@bot.message_handler(commands=['about'])  # handle with "about" command
def about_reply(message):
    image2 = open('static/about.jpg', 'rb')  # another pic
    bot.send_photo(message.chat.id, image2)
    bot.send_message(message.chat.id,
                     "I was created by [Dmitry](tg://user?id={416544613}).\n"  # Telegram link
                     "[VK](vk.com/id46566190)\n"  # VK link (for Russian and C.I.S. people who use it always and everywhere)
                     "[Instagram](instagram.com/dmitrygurylev/)",  # Instagram link
                     parse_mode="Markdown")


@bot.message_handler(content_types=['text'])  # handle with text (ONLY FOR "EXCHANGE" COMMAND)
def qwerty(message):
    user_text = message.text.split()
    if len(user_text) == 3 and user_text[0].isdigit():
        user_text[1] = user_text[1].upper()  # transform letters to uppercase
        user_text[2] = user_text[2].upper()
        if user_text[1] in data["Valute"].keys() and user_text[2] in data["Valute"].keys():
            ex_v = exchange_valute(int(user_text[0]), user_text[1], user_text[2])
        elif user_text[1] == "RUR" and user_text[2] in data["Valute"].keys():
            ex_v = int(user_text[0]) / data["Valute"][user_text[2]]["Value"] * data["Valute"][user_text[2]]["Nominal"]
        elif user_text[2] == "RUR" and user_text[1] in data["Valute"].keys():
            ex_v = int(user_text[0]) * data["Valute"][user_text[1]]["Value"] / data["Valute"][user_text[1]]["Nominal"]
        else:
            bot.send_message(message.chat.id, "Try to write data in a correct way.")
            return

    bot.send_message(message.chat.id,  # bot send a result of the operations
                     "{} {} --> {} = {}"
                     .format(user_text[0], user_text[1], user_text[2], ex_v))


@bot.callback_query_handler(func=lambda call: True)  # dunno what is lambda function
def callback_inline(call):  #  handle with inline digits 1, 2 and 3
    global photo_number  # variable which count attempts
    try:
        if call.message:
            if str(call.data) == random_digit:  # if inline digit equals the random value we defined in "start_welcome" function
                image2 = open('static/dag.jpg', 'rb')
                bot.send_photo(call.message.chat.id, image2)  # send a picture of a brave Dagestan's sitizen
                bot.send_message(call.message.chat.id, "Salam aleykum")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id,  # inline keyboard must be removed if you guessed the digit
                                              message_id=call.message.message_id,
                                              reply_markup="")
                photo_number = 0
            elif call.data != random_digit and call.data in ("1", "2", "3"):
                photo_number += 1  # increment the variable
                if photo_number == 1:
                    bot.send_message(call.message.chat.id, "Did not guess the needed digit")
                elif photo_number == 2:
                    bot.send_message(call.message.chat.id, "well, the last attempt must be correct")
                else:
                    bot.send_message(call.message.chat.id, "you pushed this button already...")
    except Exception:
        print(repr(Exception))


bot.polling(none_stop=True, interval=0)
