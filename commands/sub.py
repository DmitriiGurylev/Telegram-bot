import twitter_responses
from write_messages import subscribe_msg_if_no_users, sub_unsub_if_no_errors


def subscribe_by_id(message):
    message_text_array = message.text.split(' ')
    user_ids_to_subscribe = message_text_array[1:]

    if user_ids_to_subscribe:
        subscribe_users_by_id(user_ids_to_subscribe, message.chat.id)
    else:
        subscribe_msg_if_no_users(message.chat.id)


def subscribe(message):
    message_text_array = message.text.split(' ')
    usernames_to_subscribe = message_text_array[1:]

    if usernames_to_subscribe:
        subscribe_users_by_username(usernames_to_subscribe, message.chat.id)
    else:
        subscribe_msg_if_no_users(message.chat.id)


def subscribe_users_by_username(usernames_to_subscribe, chat_id):
    response = twitter_responses.response_user_by_username(usernames_to_subscribe)
    sub_unsub_if_no_errors(response, chat_id, True)


def subscribe_users_by_id(ids_to_subscribe, chat_id):
    response = twitter_responses.response_users_by_id(ids_to_subscribe)
    sub_unsub_if_no_errors(response, chat_id, True)
