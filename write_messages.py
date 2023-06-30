import iso8601
from psycopg2 import DatabaseError

import twitter_responses
from bot_init import bot

from db_work import pg_connection
from db_work.db import get_list_of_user_ids, remove_twitter_user
from twitteruser import TwitterUser


async def send_start_message(message):
    msg = "Hi!\n" + \
          "U can send me next commands\n" + \
          "1) /about, to know some information\n" + \
          "2) sub, to subscribe Twitter user by username\n" + \
          "3) sub_id, to subscribe Twitter user by id\n" + \
          "4) unsub, to unsubscribe Twitter user by username\n" + \
          "5) unsub_id, to unsubscribe Twitter user by id\n" + \
          "6) /list, to show list of subscriptions\n" + \
          "7) /get, to get last tweets\n"
    await send_msg(message.chat.id, msg)


async def send_about_message(chat_id):
    msg = "It was created by [Dmitry](tg://user?id={416544613}).\n" \
          "[VK](vk.com/id46566190)\n" \
          "[Instagram](instagram.com/dmitrygurylev/)"
    await send_msg(chat_id, msg)


async def show_messages(chat_id, tweets, username):
    for tweet in tweets:
        text = tweet["text"]
        created_at = tweet["created_at"]
        date = iso8601.parse_date(created_at).strftime('%d-%m-%Y %H:%M:%S')
        await send_msg(chat_id, text + "\n\n" + username + "\n" + date)


async def show_meta(message, username):
    await send_msg(message.chat.id, "there is no user '" + username + "'")


async def get_list_of_username_ids(chat_id):
    id_list = get_list_of_user_ids(chat_id)
    if not id_list:
        await send_msg(chat_id, "you are not following anyone")
    else:
        response = twitter_responses.response_users_by_id(id_list)
        followed_users = ""
        for user in response["data"]:
            user = TwitterUser(user["id"], user["username"], None)
            followed_users = followed_users + "id:" + user.id + ", username: " + user.username + "\n\n"
        await send_msg(chat_id, "you are following:\n\n" + followed_users)


def __subscribe_msg(response, chat_id):
    msg_error = ""
    msg_ok = ""
    if 'data' in response:
        msg_ok = __sub_msg_if_no_errors(response["data"], chat_id)
    if 'errors' in response:
        msg_error = __sub_unsub_if_errors(response["errors"], True)
    return msg_ok + msg_error


def __unsubscribe_msg(response, chat_id):
    msg_error = ""
    msg_ok = ""
    if 'data' in response:
        msg_ok = __unsub_msg_if_no_errors(response["data"], chat_id)
    if 'errors' in response:
        msg_error = __sub_unsub_if_errors(response["errors"], False)
    return msg_ok + msg_error


async def sub_unsub_msg(response, chat_id, is_sub):
    msg = __subscribe_msg(response, chat_id) if is_sub else __unsubscribe_msg(response, chat_id)
    await send_msg(chat_id, msg)


async def unsubscribe_msg_if_no_users(chat_id):
    await send_msg(chat_id, "you didn't choose any user to unsubscribe")


def __sub_msg_if_no_errors(user_id, chat_id):
    if add_user_to_db(user_id, chat_id):
        return "Successfully subscribed on user\n"
    else:
        return "Already subscribed on user\n"


def __unsub_msg_if_no_errors(user_id, chat_id):
    if remove_user_from_storage(user_id, chat_id):
        return "Successfully unsubscribed on user\n"
    else:
        return "You are not subscribed on user\n"


async def sub_if_no_errors(resp, chat_id):
    msg = ''
    for user_ok in resp["data"]:
        user = TwitterUser(user_ok["id"], user_ok["username"], user_ok["name"])
        users_to_sub = __sub_msg_if_no_errors(user.id, chat_id)
        msg += users_to_sub + \
               "id: " + user.id + ",\n" + \
               "username: " + user.username + ",\n" + \
               "name: " + user.name + "\n\n"
    return msg


def __sub_unsub_if_errors(rest_error, is_sub):
    sub_unsub_text = "subscribe" if is_sub else "unsubscribe"
    errors = ""
    for user_error in rest_error:
        errors = errors + "Can't " + sub_unsub_text + \
                 " on user\nname: " + user_error["value"] + \
                 "\nreason: " + user_error["detail"] + "\n\n"
    return errors


def add_user_to_db(user_id, chat_id):
    response = twitter_responses.get_last_tweet_of_user(user_id)
    latest_tweet_id = -1 \
        if response["meta"]["result_count"] == 0 \
        else response["meta"]["newest_id"]
    try:
        with pg_connection.conn as conn:
            with conn.cursor() as cursor:
                commands = (
                    f"""
                    INSERT INTO twitter_users(twitter_user_id)
                    VALUES ({user_id})
                    """,
                    f"""
                    INSERT INTO service_users_following(tld_id, twitter_user_id)
                    VALUES ({chat_id}, {user_id})
                    """,
                    f"""
                    INSERT INTO twitter_user_last_msgs(twitter_user_id, msg_id)
                    VALUES ({user_id}, {latest_tweet_id})
                    """
                )
                for c in commands:
                    cursor.execute(c)
    except (Exception, DatabaseError) as error:
        print(error)


async def remove_user_from_storage(user_id, chat_id):
    return await remove_twitter_user(user_id, chat_id)


async def send_msg(chat_id, msg):
    await bot.send_message(chat_id, msg)
