import iso8601

import twitter_responses
from bot_init import tele_bot
from db_work.db_0 import get_list_by_chat_id, add_user_to_storage_subscription, \
    unsubscribe_user_from_storage_subscription


def send_start_message(message):
    tele_bot.send_message(message.chat.id,  # start message by bot
                          "Hi, {}!\n"
                          "I'm a bot named {}.\n"
                          "U can send me next commands\n"
                          "1) /about, to know some information\n"
                          "2) sub, to subscribe Twitter user by username\n"
                          "3) sub_id, to subscribe Twitter user by id\n"
                          "4) unsub, to unsubscribe Twitter user by username\n"
                          "5) unsub_id, to unsubscribe Twitter user by id\n"
                          "6) /list, to show list of subscriptions\n"
                          .format(
                              message.from_user.first_name,
                              tele_bot.get_me().first_name)
                          )


def send_about_message(message):
    tele_bot.send_message(message.chat.id,
                          "It was created by [Dmitry](tg://user?id={416544613}).\n"  # Telegram link
                          "[VK](vk.com/id46566190)\n"  # VK link
                          "[Instagram](instagram.com/dmitrygurylev/)",  # Instagram link
                          parse_mode="Markdown")


def show_messages(message, tweets):
    for tweet in tweets:
        text = tweet["text"]
        created_at = tweet["created_at"]
        date = iso8601.parse_date(created_at).strftime('%d-%m-%Y %H:%M:%S')

        tele_bot.send_message(
            message.chat.id,
            text + "\n\n" + date
        )


def show_meta(message, username):
    tele_bot.send_message(
        message.chat.id,
        "there is no user '{}'".format(username)
    )


def get_list(message):
    id_list = get_list_by_chat_id(message.chat.id)

    response = twitter_responses.response_users_by_id(id_list)
    followed_users = ""
    for user in response["data"]:
        user_id = user["id"]
        username = user["username"]
        followed_users = followed_users + "id:" + user_id + ", username:" + username + "\n\n"
    tele_bot.send_message(
        message.chat.id,
        "you are following:\n\n" + followed_users)


def subscribe_msg(response, message):
    msg_error = ""
    msg_ok = ""
    if 'data' in response:
        msg_ok = subscribe_msg_if_no_errors(response["data"], message.chat.id)
    if 'errors' in response:
        msg_error = subscribe_msg_if_errors(response["errors"])
    tele_bot.send_message(
        message.chat.id,
        msg_ok + msg_error
    )


def subscribe_msg_if_no_users(message):
    tele_bot.send_message(
        message.chat.id,
        "you didn't choose any user to subscribe"
    )


def unsubscribe_msg(response, message):
    msg_error = ""
    msg_ok = ""
    if 'data' in response:
        msg_ok = unsubscribe_msg_if_no_errors(response["data"], message.chat.id)
    if 'errors' in response:
        msg_error = unsubscribe_msg_if_errors(response["errors"])
    tele_bot.send_message(
        message.chat.id,
        msg_ok + msg_error
    )


def unsubscribe_msg_if_no_users(message):
    tele_bot.send_message(
        message.chat.id,
        "you didn't choose any user to unsubscribe"
    )


def subscribe_msg_if_no_errors(resp_data, chat_id):
    users_to_subscribe = ""
    for user_ok in resp_data:
        if add_user_to_storage_subscription(user_ok["id"], chat_id):
            users_to_subscribe = users_to_subscribe + \
                                 "Succesfully subscribed on user\n" + \
                                 "id: " + user_ok["id"] + ",\n" + \
                                 "username: " + user_ok["username"] + ",\n" + \
                                 "name: " + user_ok["name"] + "\n\n"
        else:
            users_to_subscribe = users_to_subscribe + \
                                 "Already subscribed on user\n" + \
                                 "id: " + user_ok["id"] + ",\n" + \
                                 "username: " + user_ok["username"] + ",\n" + \
                                 "name: " + user_ok["name"] + "\n\n"
    return users_to_subscribe


def unsubscribe_msg_if_no_errors(resp_data, chat_id):
    users_to_unsubscribe = ""
    for user_ok in resp_data:
        if unsubscribe_user_from_storage_subscription(user_ok["id"], chat_id):
            users_to_unsubscribe = users_to_unsubscribe + \
                                   "Succesfully unsubscribed on user\n" + \
                                   "id: " + user_ok["id"] + ",\n" + \
                                   "username: " + user_ok["username"] + ",\n" + \
                                   "name: " + user_ok["name"] + "\n\n"
        else:
            users_to_unsubscribe = users_to_unsubscribe + \
                                   "Already unsubscribed on user\n" + \
                                   "id: " + user_ok["id"] + ",\n" + \
                                   "username: " + user_ok["username"] + ",\n" + \
                                   "name: " + user_ok["name"] + "\n\n"
    return users_to_unsubscribe


def subscribe_msg_if_errors(rest_error):
    errors = ""
    for user_error in rest_error:
        errors = errors + \
                 "Can't subscribe on user\n" + \
                 "name: " + user_error["value"] + "\n" \
                                                  "reason: " + user_error["detail"] + "\n\n"
    return errors


def unsubscribe_msg_if_errors(rest_error):
    errors = ""
    for user_error in rest_error:
        errors = errors + \
                 "Can't unsubscribe on user\n" + \
                 "name: " + user_error["value"] + "\n" \
                                                  "reason: " + user_error["detail"] + "\n\n"
    return errors
