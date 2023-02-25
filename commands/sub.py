import twitter_responses
from write_messages import subscribe_msg_if_no_users, subscribe_msg


def subscribe_by_id(message):
    message_text_array = message.text.split(' ')
    user_ids_to_subscribe = message_text_array[1:]

    if user_ids_to_subscribe:
        subscribe_users_by_id(user_ids_to_subscribe, message)
    else:
        subscribe_msg_if_no_users(message)


def subscribe(message):
    message_text_array = message.text.split(' ')
    usernames_to_subscribe = message_text_array[1:]

    if usernames_to_subscribe:
        subscribe_users_by_username(usernames_to_subscribe, message)
    else:
        subscribe_msg_if_no_users(message)


def subscribe_users_by_username(usernames_to_subscribe, message):
    response = twitter_responses.response_user_by_username(usernames_to_subscribe)
    subscribe_msg(response, message)


def subscribe_users_by_id(ids_to_subscribe, message):
    response = twitter_responses.response_users_by_id(ids_to_subscribe)
    subscribe_msg(response, message)
