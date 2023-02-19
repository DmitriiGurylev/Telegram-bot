import json
import random
import time
from threading import Thread
import telebot
import tweepy
from telebot import types
import config
import twitter_responses
from datetime import datetime, timedelta

twitter_auth = tweepy.OAuthHandler(config.twitter_consumer_key, config.twitter_consumer_secret)
twitter_auth.set_access_token(config.twitter_access_key, config.twitter_access_secret)
twitter_api = tweepy.API(twitter_auth, wait_on_rate_limit=True)

dtformat = '%Y-%m-%dT%H:%M:%SZ'
flag_for_zero = 0
photo_number = 0
telegram_test_bot = telebot.TeleBot(config.bot_token)
is_bot_started = False

storage_twitter_subscription = "storage_twitter_subscription.txt"


def add_to_storage_subscription(id_to_add):
    id_set = set()

    with open(storage_twitter_subscription, "r") as f:
        ids = f.readlines()
        for id in ids:
            id = id.replace("\n", '')
            id_set.add(id)

    if id_to_add not in id_set:
        with open(storage_twitter_subscription, "a") as f:
            f.write(id_to_add + "\n")

def handle():
    @telegram_test_bot.message_handler(commands=['start'])  # handle the command "Start"
    def start_welcome(message):
        is_bot_started = True
        telegram_test_bot.send_message(message.chat.id,  # start message by bot
                                       "Hi, {}!\n"
                                       "I'm a bot named {}.\n"
                                       "U can send me next commands\n"
                                       "1) /about, to know some information\n"
                                       "2) /subscribe, to subscribe Twitter user by name\n"
                                       "3) /unsubscribe, to unsubscribe Twitter user by name\n"
                                       "4) /list, to list subscribed Twitter users\n"
                                       # "1) /subscribe, to subscribe Twitter user\n"
                                       .format(
                                           message.from_user.first_name,
                                           telegram_test_bot.get_me().first_name)
                                       )

    @telegram_test_bot.message_handler(commands=['about'])  # handle with "about" command
    def about_reply(message):
        telegram_test_bot.send_message(message.chat.id,
                                       "It was created by [Dmitry](tg://user?id={416544613}).\n"  # Telegram link
                                       "[VK](vk.com/id46566190)\n"  # VK link
                                       "[Instagram](instagram.com/dmitrygurylev/)",  # Instagram link
                                       parse_mode="Markdown")

        # https: // api.twitter.com / 2 / users / by?usernames = twitterdev, twitterapi, adsapi

    @telegram_test_bot.message_handler(content_types=['text'])  # handle with text
    def handle_text(message):
        message_text_array = message.text.split(' ')

        if message_text_array[0] == "subscribe":
            subscribe(message)
        elif message_text_array[0] == "list":
            get_list(message)

    def msg_if_no_users_to_subscribe(message):
        telegram_test_bot.send_message(
            message.chat.id,
            "you didn't choose any user to subscribe"
        )

    def msg_users_if_no_errors(resp_data):
        users_to_subscribe = ""
        for user_ok in resp_data:
            add_to_storage_subscription(user_ok["id"])
            users_to_subscribe = users_to_subscribe + \
                                 "Succesfully subscribed on user\n" + \
                                 "id: " + user_ok["id"] + ",\n" + \
                                 "name: " + user_ok["name"] + "\n\n"
        return users_to_subscribe


    def msg_users_if_errors(rest_error):
        errors = ""
        for user_error in rest_error:
            errors = errors + \
                     "Can't subscribe on user\n" + \
                     "name: " + user_error["value"] + "\n" \
                                                      "reason: " + user_error["detail"] + "\n\n"
        return errors


    def msg_subscribe(users_to_subscribe, message):
        response = twitter_responses.response_users(users_to_subscribe)
        msg_error=""
        msg_ok=""
        if 'data' in response:
            msg_ok = msg_users_if_no_errors(response["data"])
        if 'errors' in response:
            msg_error = msg_users_if_errors(response["errors"])
        telegram_test_bot.send_message(
            message.chat.id,
            msg_ok + msg_error
        )


    def subscribe(message):
        message_text_array = message.text.split(' ')

        users_to_subscribe = message_text_array[1:]
        if not users_to_subscribe:
            msg_if_no_users_to_subscribe(message)
        else:
            msg_subscribe(users_to_subscribe, message)

    def get_list(message):
        id_list = []

        with open(storage_twitter_subscription, "r") as f:
            ids = f.readlines()
            for id in ids:
                id = id.replace("\n", '')
                id_list.append(id)
        telegram_test_bot.send_message(
            message.chat.id,
            id_list)


    @telegram_test_bot.message_handler(content_types=['text'])  # handle with text
    def handle_text(message):
        global data
        if "tweet=" in message.text or "tweets=" in message.text:
            if "tweet=" in message.text:
                messages_number = 1
            else:
                messages_number = len(message.text.replace("tweets=", "").split(","))
            response = twitter_responses.response_twitter_tweets(message.text.replace(" ", "").split("=")[1])
            if messages_number == 1:
                if "data" in response:
                    telegram_test_bot.send_message(
                        message.chat.id,
                        "text:\n" + response["data"][0]["text"] + "\n" +
                        "author_id: " + response["data"][0]["author_id"] + "\n\n" +
                        "created_at: " + response["data"][0]["created_at"])
                elif "errors" in response:
                    telegram_test_bot.send_message(
                        message.chat.id,
                        "Error:\n{}".format(response["errors"][0]["detail"]))
            else:
                if "data" in response:
                    for dataItem in response["data"]:
                        telegram_test_bot.send_message(
                            message.chat.id,
                            "text:\n" + dataItem["text"] + "\n\n" +
                            "author_id: " + dataItem["author_id"] + "\n" +
                            "created_at: " + dataItem["created_at"])
                elif "errors" in response:
                    telegram_test_bot.send_message(
                        message.chat.id,
                        "Error:\n{}".format(response["errors"][0]["message"]))
        elif "twitterAuthorId=" in message.text:
            response = twitter_responses.response_twitter_last5tweets_of_the_user(message.text.replace(" ", "").split("=")[1])
            if "data" in response:
                for dataItem in response["data"]:
                    telegram_test_bot.send_message(
                        message.chat.id,
                        "messageId:\n" + dataItem["id"] + "\n\n" +
                        "createdAt:\n" + dataItem["created_at"] + "\n\n" +
                        "text:\n" + dataItem["text"] + "\n\n")
            elif "errors" in response:
                telegram_test_bot.send_message(
                    message.chat.id,
                    "Error:\n{}".format(response["errors"][0]["message"]))
    telegram_test_bot.polling(none_stop=True, interval=0)


def check_new_tweets_with_interval():
    global flag_for_zero, until, since
    while True:
        if is_bot_started:
            time.sleep(1)
            while flag_for_zero == 0:
                now_time_in_utc = datetime.utcnow()
                since = now_time_in_utc - timedelta(seconds=16)
                until = now_time_in_utc - timedelta(seconds=15)
                flag_for_zero = flag_for_zero + 1


thread1 = Thread(target=handle)
thread2 = Thread(target=check_new_tweets_with_interval)

thread1.start()
thread2.start()

# telegram_test_bot.infinity_polling(timeout=10, long_polling_timeout=5)