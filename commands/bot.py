from threading import Thread

import tweepy

import config
import twitter_responses
from bot_init import tele_bot
from commands.sub import subscribe, subscribe_by_id
from commands.unsub import unsubscribe, unsubscribe_by_id, unsubscribe_from_all
from write_messages import send_start_message, send_about_message, show_messages, get_list, show_meta

twitter_auth = tweepy.OAuthHandler(config.twitter_consumer_key, config.twitter_consumer_secret)
twitter_auth.set_access_token(config.twitter_access_key, config.twitter_access_secret)
twitter_api = tweepy.API(twitter_auth, wait_on_rate_limit=True)

dtformat = '%Y-%m-%dT%H:%M:%SZ'
flag_for_zero = 0
photo_number = 0
is_bot_started = False


def get_messages_of_user(message):
    message_text_array = message.text.split(' ')
    username = None
    response = None

    if len(message_text_array) == 2:
        username = message_text_array[1]
        response = twitter_responses.response_user_by_username(username)
        user_id = response["data"][0]["id"]
        response = twitter_responses.response_twitter_last_tweets_of_the_user(user_id, 5)
    elif len(message_text_array) == 3:
        number_of_msg = message_text_array[1]
        username = message_text_array[2]
        response = twitter_responses.response_user_by_username(username)
        user_id = response["data"][0]["id"]
        response = twitter_responses.response_twitter_last_tweets_of_the_user(user_id, number_of_msg)

    if "data" not in response:
        show_meta(message, username)
    else:
        tweets = response["data"]
        show_messages(message, tweets)


def show_list(message):
    get_list(message)


def handle():
    @tele_bot.message_handler(commands=['start'])  # handle the command "Start"
    def start_welcome(message):
        send_start_message(message)

    @tele_bot.message_handler(commands=['about'])  # handle with "about" command
    def about_reply(message):
        send_about_message(message)

    @tele_bot.message_handler(commands=['list'])  # handle with "about" command
    def list_reply(message):
        show_list(message)

    @tele_bot.message_handler(content_types=['text'])  # handle with text
    def handle_text(message):
        message_text_array = message.text.split(' ')

        match message_text_array[0]:
            case "sub":
                subscribe(message)
            case "sub_id":
                subscribe_by_id(message)
            case "list":
                show_list(message)
            case "about":
                send_about_message(message)
            case "get":
                get_messages_of_user(message)
            case "unsub":
                unsubscribe(message)
            case "unsub_id":
                unsubscribe_by_id(message)
            case "wipe":
                unsubscribe_from_all(message)
            case _:
                "ЗАГЛУШКА"


thread1 = Thread(target=handle)
thread1.start()
tele_bot.polling(non_stop=True)

