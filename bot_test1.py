import telebot
import tweepy
from telebot import types
import random
import requests
import json
import config
import twitterApi

twitter_auth = tweepy.OAuthHandler(config.twitter_consumer_key, config.twitter_consumer_secret)
twitter_auth.set_access_token(config.twitter_access_key, config.twitter_access_secret)
twitter_api = tweepy.API(twitter_auth, wait_on_rate_limit=True)

photo_number = 0
random_digit = 0

bot = telebot.TeleBot(config.bot_token)
twitter_user_id = set()
twitter_user_id.add("donaldtrump")


def response_bank(api):  # function which read data  and deserialize them from API
    response = requests.get(api)
    deserial = json.loads(response.text)
    return deserial


def response_stasuses_user_timeline(user_id):  # function which read data  and deserialize them from API

    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token

    my_params = twitterApi.twitter_stasuses_user_timeline
    my_params['user_id'] = user_id

    response = requests.get(
        twitterApi.twitter_stasuses_user_timelineUrl,
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


def response_twitter_tweets(messages_id):  # function which read data  and deserialize them from API

    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token

    my_params = twitterApi.twitter_tweets
    my_params['ids'] = messages_id

    response = requests.get(
        twitterApi.twitter_tweetsUrl,
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


def exchange_valute(value, from_first, to_second):  # function which converts valute
    first_value = data["Valute"][from_first]["Value"] / data["Valute"][from_first]["Nominal"]
    second_value = data["Valute"][to_second]["Value"] / data["Valute"][to_second]["Nominal"]
    if second_value != 0:
        return float(value) * float(first_value) / float(second_value)


data = response_bank(config.bank_api_currency)  # variable representing data acquired from bank api
tweets = response_twitter_tweets(twitter_user_id)
twitter_user = response_stasuses_user_timeline(twitter_user_id)


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
    global random_digit
    random_digit = str(random.randint(1, 3))  # random value from 1 to 3. Why we use it? Look below
    image1 = open('static/start.jpg', 'rb')  # start image
    bot.send_photo(message.chat.id, image1)  # send the photo to a user
    keyboard_in1 = types.InlineKeyboardMarkup(row_width=3)  # create an inline keyboard with 3 values
    unit_1 = types.InlineKeyboardButton("1", callback_data="1")
    unit_2 = types.InlineKeyboardButton("2", callback_data="2")
    unit_3 = types.InlineKeyboardButton("3", callback_data="3")
    keyboard_in1.add(unit_1, unit_2, unit_3)

    bot.send_message(message.chat.id,  # start message by bot
                     "Hi, {}!\n"
                     "I'm a bot named {}.\n"
                     "U can send me next comands \n"
                     "1) /exchange, "
                     "to check the currency today "
                     "according to central bank of RUSSIA FEDERUSSIA \n"
                     "2) /about, to know some information \n"
                     "3) /tweetInfo, to get tex of tweet"
                     .format(message.from_user.first_name, bot.get_me().first_name))

    bot.send_message(message.chat.id,  # second message following the first one
                     "U can send me a digit between 1 and 3 "
                     "to get a random 05 picture",
                     reply_markup=keyboard_in1)


@bot.message_handler(commands=['exchange'])  # handle with "exchange" command
def exchange(message):  # just a description of the command
    bot.send_message(message.chat.id, "U can choose currency exchange "
                                      "of these currencies:\n" +
                     str(data["Valute"].keys()) +
                     "\n"
                     "To get result write down an expression according to a next way: \n"
                     "11 USD EUR")


@bot.message_handler(commands=['about'])  # handle with "about" command
def about_reply(message):
    image2 = open('static/about.jpg', 'rb')  # another pic
    bot.send_photo(message.chat.id, image2)
    bot.send_message(message.chat.id,
                     "It was created by [Dmitry](tg://user?id={416544613}).\n"  # Telegram link
                     "[VK](vk.com/id46566190)\n"  # VK link
                     "[Instagram](instagram.com/dmitrygurylev/)",  # Instagram link
                     parse_mode="Markdown")


    @bot.message_handler(commands=['tweetInfo'])  # handle with text (ONLY FOR TWEETINFO COMMAND)
    def qwerty(message):
        bot.send_message(message.chat.id, "Write needed tweets down in a next way:\n "
                                          "tweet=<tweetId> or"
                                          "tweets=<tweetId1>,<tweetId2>... without spaces")


@bot.message_handler(content_types=['text'])  # handle with text (ONLY FOR "EXCHANGE" COMMAND)
def qwerty(message):
    if (message.text.find("tweet=") or message.text.find("tweets=")):
        if "tweet=" in message.text:
            messages_number = 1
        else:
            messages_number = len(message.text.replace("tweets=", "").split(","))
        response = response_twitter_tweets(message.text.replace(" ", "").split("=")[1])

        if messages_number == 1:
            if "data" in response:
                bot.send_message(
                    message.chat.id,
                    "text:\n" + response["data"][0]["text"] + "\n" +
                    "author_id: " + response["data"][0]["author_id"] + "\n\n" +
                    "created_at: " + response["data"][0]["created_at"])
            elif "errors" in response:
                bot.send_message(
                    message.chat.id,
                    "Error:\n{}".format(response["errors"][0]["detail"]))
        else:
            if "data" in response:
                for dataItem in response["data"]:
                    bot.send_message(
                        message.chat.id,
                        "text:\n" + dataItem["text"] + "\n\n" +
                        "author_id: " + dataItem["author_id"] + "\n" +
                        "created_at: " + dataItem["created_at"])
            elif "errors" in response:
                bot.send_message(
                    message.chat.id,
                    "Error:\n{}".format(response["errors"][0]["message"]))

    else:
        user_text = message.text.split()
        if len(user_text) == 3 and user_text[0].isdigit() and len(user_text[1]) == 3 and len(user_text[2]) == 3:
            user_text[1] = user_text[1].upper()  # transform letters to uppercase
            user_text[2] = user_text[2].upper()
            if user_text[1] in data["Valute"].keys() and user_text[2] in data["Valute"].keys():
                ex_v = exchange_valute(user_text[0], user_text[1], user_text[2])
            elif user_text[1] == "RUR" and user_text[2] in data["Valute"].keys():
                ex_v = float(user_text[0]) / data["Valute"][user_text[2]]["Value"] * data["Valute"][user_text[2]]["Nominal"]
            elif user_text[1] in data["Valute"].keys() and user_text[2] == "RUR":
                ex_v = float(user_text[0]) * data["Valute"][user_text[1]]["Value"] / data["Valute"][user_text[1]]["Nominal"]
            else:
                bot.send_message(
                    message.chat.id,
                    "Try to write data in a correct way.")
                return
        else:
            bot.send_message(message.chat.id, "I can't work with this text. It's not correct to handle.")
            return

        bot.send_message(
            message.chat.id,  # bot send a result of the operations
            "{} {} --> {} = {}".format(user_text[0], user_text[1], user_text[2], ex_v))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):  # handle with inline digits 1, 2 and 3
    global photo_number  # variable which count attempts
    try:
        if call.message:
            if str(
                    call.data) == random_digit:  # if inline digit equals the random value we defined in "start_welcome" function
                image2 = open('static/dag.jpg', 'rb')
                bot.send_photo(call.message.chat.id, image2)  # send a picture of a brave Dagestan's sitizen
                bot.send_message(call.message.chat.id, "Salam aleykum")
                bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                              # inline keyboard must be removed if you guessed the digit
                                              message_id=call.message.message_id,
                                              reply_markup="")
                photo_number = 0
            elif call.data != random_digit and call.data in ("1", "2", "3"):
                photo_number += 1  # increment the variable
                if photo_number == 1:
                    bot.send_message(call.message.chat.id, "Did not guess the needed digit")
                elif photo_number == 2:
                    bot.send_message(call.message.chat.id, "Well, the last attempt must be correct")
                else:
                    bot.send_message(call.message.chat.id, "You pushed this button already...")
    except Exception:
        print(repr(Exception))


bot.polling(none_stop=True, interval=0)
