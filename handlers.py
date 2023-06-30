from aiogram import Dispatcher
import twitter_responses
from commands.sub import subscribe
from db_work.db import get_chat_ids, get_list_of_user_ids, get_list_of_newest_tweets, update_tweet_in_db
from write_messages import show_messages, send_msg, show_meta, get_list_of_username_ids, send_start_message, \
    send_about_message
from aiogram import types

async def check_new_tweets_with_interval():
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
                    await show_messages(chat_id, new_tweets, username)


async def get_messages_of_user(message):
    message_text_array = message.text.split(' ')
    if len(message_text_array) == 2:
        number_of_msg = 5
        username = [message_text_array[1]]
    elif len(message_text_array) == 3:
        number_of_msg = message_text_array[1]
        username = [message_text_array[2]]
    else:
        await send_msg(message.chat.id, "You didn't choose Twitter user to get messages")
        return

    response = twitter_responses.response_user_by_username(username)
    user_id = response["data"][0]["id"]
    response = twitter_responses.response_twitter_last_tweets_of_the_user(user_id, number_of_msg)
    if "data" not in response:
        await show_meta(message.chat.id, username)
    else:
        tweets = response["data"]
        await show_messages(message.chat.id, tweets, username)


async def show_list(message):
    await get_list_of_username_ids(message.chat.id)


async def start_welcome(message):
    msg = "Hi!\n" + \
          "I'm a bot named " + "ЗАГЛУШКА" + ".\n" + \
          "U can send me next commands\n" + \
          "1) /about, to know some information\n" + \
          "2) sub, to subscribe Twitter user by username\n" + \
          "3) sub_id, to subscribe Twitter user by id\n" + \
          "4) unsub, to unsubscribe Twitter user by username\n" + \
          "5) unsub_id, to unsubscribe Twitter user by id\n" + \
          "6) /list, to show list of subscriptions\n" + \
          "7) /get, to get last tweets\n"
    await send_msg(message.chat.id, msg)


async def about_reply(message):
    await send_about_message(message.chat.id)


async def get_reply(message: types.Message):
    await get_messages_of_user(message)


async def list_reply(message):
    await show_list(message)


async def handle_text(message: types.Message):
    message_text_array = message.text.split(' ')

    match message_text_array[0]:
        case "sub":
            msg = subscribe(message)
            await message.answer(msg)
        # case "sub_id":
        #     await subscribe_by_id(message)
        # case "list":
        #     await show_list(message)
        # case "about":
        #     await send_about_message(message)
        # case "get":
        #     await get_messages_of_user(message)
        # case "unsub":
        #     await unsubscribe(message)
        # case "unsub_id":
        #     await unsubscribe_by_id(message)
        # case "wipe":
        #     await unsubscribe_from_all(message.chat.id)
        case _:
            "ЗАГЛУШКА"


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_welcome, commands=['start'])
    dp.register_message_handler(about_reply, commands=['about'])
    dp.register_message_handler(get_reply, commands=['get'])
    dp.register_message_handler(list_reply, commands=['list'])
    dp.register_message_handler(handle_text, content_types=['text'])
