import time
from datetime import datetime, timedelta
from threading import Thread

import tweepy

import config
import twitter_responses
from bot_init import t_bot
from write_messages import subscribe_msg, subscribe_msg_if_no_users, unsubscribe_msg_if_no_users, \
    unsubscribe_users_by_id, send_start_message, send_about_message, unsubscribe_msg, show_messages, get_list

twitter_auth = tweepy.OAuthHandler(config.twitter_consumer_key, config.twitter_consumer_secret)
twitter_auth.set_access_token(config.twitter_access_key, config.twitter_access_secret)
twitter_api = tweepy.API(twitter_auth, wait_on_rate_limit=True)

dtformat = '%Y-%m-%dT%H:%M:%SZ'
flag_for_zero = 0
photo_number = 0
is_bot_started = False


def get_messages_of_user(message):
    message_text_array = message.text.split(' ')
    if len(message_text_array) == 2:
        username = message_text_array[1]
        response = twitter_responses.response_user_by_username(username)
        id = response["data"][0]["id"]
        response = twitter_responses.response_twitter_last_tweets_of_the_user(id, 5)
        tweets = response["data"]
        show_messages(message, tweets)
    elif len(message_text_array) == 3:
        number_of_msg = message_text_array[1]
        username = message_text_array[2]
        response = twitter_responses.response_user_by_username(username)
        id = response["data"][0]["id"]
        response = twitter_responses.response_twitter_last_tweets_of_the_user(id, number_of_msg)
        tweets = response["data"]
        show_messages(message, tweets)


def subscribe_users_by_username(user_names_to_subscribe, message):
    response = twitter_responses.response_users_by_username(user_names_to_subscribe)
    subscribe_msg(response, message)


def unsubscribe_users_by_username(usernames_to_unsubscribe, message):
    response = twitter_responses.response_users_by_username(usernames_to_unsubscribe)
    unsubscribe_msg(response, message)


def subscribe_users_by_id(ids_to_subscribe, message):
    response = twitter_responses.response_users_by_id(ids_to_subscribe)
    subscribe_msg(response, message)


def subscribe(message):
    message_text_array = message.text.split(' ')
    users_to_subscribe = message_text_array[1:]
    if users_to_subscribe:
        subscribe_users_by_username(users_to_subscribe, message)
    else:
        subscribe_msg_if_no_users(message)


def unsubscribe(message):
    message_text_array = message.text.split(' ')
    usernames_to_unsubscribe = message_text_array[1:]
    if usernames_to_unsubscribe:
        unsubscribe_users_by_username(usernames_to_unsubscribe, message)
    else:
        unsubscribe_msg_if_no_users(message)


def subscribe_by_id(message):
    message_text_array = message.text.split(' ')
    user_ids_to_subscribe = message_text_array[1:]
    if user_ids_to_subscribe:
        subscribe_users_by_id(user_ids_to_subscribe, message)
    else:
        subscribe_msg_if_no_users(message)


def unsubscribe_by_id(message):
    message_text_array = message.text.split(' ')
    user_ids_to_unsubscribe = message_text_array[1:]
    if user_ids_to_unsubscribe:
        unsubscribe_users_by_id(user_ids_to_unsubscribe, message)
    else:
        unsubscribe_msg_if_no_users(message)


def show_list(message):
    get_list(message)


def handle():
    @t_bot.message_handler(commands=['start'])  # handle the command "Start"
    def start_welcome(message):
        is_bot_started = True
        send_start_message(message)

    @t_bot.message_handler(commands=['about'])  # handle with "about" command
    def about_reply(message):
        send_about_message(message)

    @t_bot.message_handler(content_types=['text'])  # handle with text
    def handle_text(message):
        message_text_array = message.text.split(' ')

        match message_text_array[0]:
            case "subscribe":
                subscribe(message)
            case "subscribe_by_id":
                subscribe_by_id(message)
            case "list":
                show_list(message)
            case "get":
                get_messages_of_user(message)
            case "unsubscribe":
                unsubscribe(message)
            case "unsubscribe_by_id":
                unsubscribe_by_id(message)
            case _:
                "ЗАГЛУШКА"


thread1 = Thread(target=handle)
# thread2 = Thread(target=check_new_tweets_with_interval)

thread1.start()
# thread2.start()

t_bot.polling(non_stop=True)

# telegram_test_bot.infinity_polling(timeout=10, long_polling_timeout=5)
