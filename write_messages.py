import iso8601

import twitter_responses
from bot_init import tele_bot
from db_work.db_1 import update_tweet_in_db, remove_twitter_user, \
    get_list_of_user_ids
from twitter_user import twitter_user


def send_start_message(message):
    msg = "Hi, " + message.from_user.first_name + "!\n" + \
          "I'm a bot named " + tele_bot.get_me().first_name + ".\n" + \
          "U can send me next commands\n" + \
          "1) /about, to know some information\n" + \
          "2) sub, to subscribe Twitter user by username\n" + \
          "3) sub_id, to subscribe Twitter user by id\n" + \
          "4) unsub, to unsubscribe Twitter user by username\n" + \
          "5) unsub_id, to unsubscribe Twitter user by id\n" + \
          "6) /list, to show list of subscriptions\n" + \
          "7) /get, to get last tweets\n"
    send_msg(message.chat.id, msg)


def send_about_message(chat_id):
    msg = "It was created by [Dmitry](tg://user?id={416544613}).\n" \
          "[VK](vk.com/id46566190)\n" \
          "[Instagram](instagram.com/dmitrygurylev/)"
    send_msg(chat_id, msg)


def show_messages(chat_id, tweets, username):
    for tweet in tweets:
        text = tweet["text"]
        created_at = tweet["created_at"]
        date = iso8601.parse_date(created_at).strftime('%d-%m-%Y %H:%M:%S')
        send_msg(chat_id, text + "\n\n" + username + "\n" + date)


def show_meta(message, username):
    send_msg(message.chat.id, "there is no user '" + username + "'")


def get_list_of_username_ids(chat_id):
    id_list = get_list_of_user_ids(chat_id)
    if not id_list:
        send_msg(chat_id, "you are not following anyone")
    else:
        response = twitter_responses.response_users_by_id(id_list)
        followed_users = ""
        for user in response["data"]:
            user = twitter_user(user["id"], user["username"], None)
            followed_users = followed_users + "id:" + user.id + ", username: " + user.username + "\n\n"
        send_msg(chat_id, "you are following:\n\n" + followed_users)


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


def sub_unsub_msg(response, chat_id, is_sub):
    msg = __subscribe_msg(response, chat_id) if is_sub else __unsubscribe_msg(response, chat_id)
    send_msg(chat_id, msg)


def subscribe_msg_if_no_users(chat_id):
    send_msg(chat_id, "you didn't choose any user to subscribe")


def unsubscribe_msg_if_no_users(chat_id):
    send_msg(chat_id, "you didn't choose any user to unsubscribe")


def __sub_msg_if_no_errors(user_id, chat_id):
    if add_user_to_storage(user_id, chat_id):
        return "Successfully subscribed on user\n"
    else:
        return "Already subscribed on user\n"


def __unsub_msg_if_no_errors(user_id, chat_id):
    if remove_user_from_storage(user_id, chat_id):
        return "Successfully unsubscribed on user\n"
    else:
        return "You are not subscribed on user\n"


def sub_unsub_if_no_errors(resp, chat_id, is_sub):
    msg = ''
    for user_ok in resp["data"]:
        user = twitter_user(user_ok["id"], user_ok["username"], user_ok["name"])
        users_to_sub_unsub = ''
        if is_sub:
            users_to_sub_unsub = __sub_msg_if_no_errors(user.id, chat_id)
        else:
            users_to_sub_unsub = __unsub_msg_if_no_errors(user.id, chat_id)
        msg += users_to_sub_unsub + \
            "id: " + user.id + ",\n" + \
            "username: " + user.username + ",\n" + \
            "name: " + user.name + "\n\n"
    send_msg(chat_id, msg)


def __sub_unsub_if_errors(rest_error, is_sub):
    sub_unsub_text = "subscribe" if is_sub else "unsubscribe"
    errors = ""
    for user_error in rest_error:
        errors = errors + "Can't " + sub_unsub_text + \
                 " on user\nname: " + user_error["value"] + \
                 "\nreason: " + user_error["detail"] + "\n\n"
    return errors


def add_user_to_storage(user_id, chat_id):
    response = twitter_responses.get_last_tweet_of_user(user_id)
    latest_tweet_id = -1 \
        if response["meta"]["result_count"] == 0 \
        else response["meta"]["newest_id"]
    return update_tweet_in_db(user_id, latest_tweet_id, chat_id)


def remove_user_from_storage(user_id, chat_id):
    return remove_twitter_user(user_id, chat_id)


def send_msg(chat_id, msg):
    tele_bot.send_message(chat_id, msg)
