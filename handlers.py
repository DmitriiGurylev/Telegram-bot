from aiogram import Dispatcher
import twitter_responses
from commands.sub import subscribe, subscribe_by_id
from commands.unsub import unsubscribe, unsubscribe_by_id, unsubscribe_from_all
from db_work.db_1 import get_chat_ids, update_tweet_in_db, get_list_of_newest_tweets
from write_messages import send_start_message, send_about_message, show_messages, get_list_of_username_ids, \
    get_list_of_user_ids, show_meta, send_msg


def check_new_tweets_with_interval():
    while True:
        chat_ids = get_chat_ids()
        map_of_user_id_and_chat_ids = {}
        for chat_id in chat_ids:
            for user_id in get_list_of_user_ids(chat_id):
                map_of_user_id_and_chat_ids[user_id] = map_of_user_id_and_chat_ids[user_id] + chat_id \
                    if user_id in map_of_user_id_and_chat_ids.keys() \
                    else [chat_id]

        for user_id, chat_ids in map_of_user_id_and_chat_ids.items():
            newest_tweet_in_db = get_list_of_newest_tweets(chat_ids[0], user_id)
            resp_tweet = twitter_responses.response_twitter_user_subscribe_tweets(
                user_id,
                since_id=newest_tweet_in_db
            )
            resp_user = twitter_responses.response_users_by_id([user_id])
            if 'status' in resp_user and resp_user['status'] == 429:
                return
            username = resp_user["data"][0]["username"]

            if resp_tweet["meta"]["result_count"] > 0:
                new_tweets = resp_tweet["data"]
                tweet_ids_list = [tweet["id"] for tweet in new_tweets]
                newest_tweet_id = max(tweet_ids_list)

                for chat_id in chat_ids:
                    res = update_tweet_in_db(user_id, newest_tweet_id, chat_id)
                    show_messages(chat_id, new_tweets, username)


def get_messages_of_user(message):
    message_text_array = message.text.split(' ')
    if len(message_text_array) == 2:
        number_of_msg = 5
        username = [message_text_array[1]]
    elif len(message_text_array) == 3:
        number_of_msg = message_text_array[1]
        username = [message_text_array[2]]
    else:
        send_msg(message.chat.id, "You didn't choose Twitter user to get messages")
        return

    response = twitter_responses.response_user_by_username(username)
    user_id = response["data"][0]["id"]
    response = twitter_responses.response_twitter_last_tweets_of_the_user(user_id, number_of_msg)
    if "data" not in response:
        show_meta(message.chat.id, username)
    else:
        tweets = response["data"]
        show_messages(message.chat.id, tweets, username)


def show_list(message):
    get_list_of_username_ids(message.chat.id)


def start_welcome(message):
    send_start_message(message)


def about_reply(message):
    send_about_message(message.chat.id)


def get_reply(message):
    get_messages_of_user(message)


def list_reply(message):
    show_list(message)


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
            unsubscribe_from_all(message.chat.id)
        case _:
            "ЗАГЛУШКА"


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_welcome, commands=['start'])
    dp.register_message_handler(about_reply, commands=['about'])
    dp.register_message_handler(get_reply, commands=['get'])
    dp.register_message_handler(list_reply, commands=['list'])
    dp.register_message_handler(handle_text, content_types=['text'])
