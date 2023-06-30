import twitter_responses
from write_messages import sub_if_no_errors


def subscribe(message):
    message_text_array = message.text.split(' ')
    usernames_to_subscribe = message_text_array[1:]

    if usernames_to_subscribe:
        subscribe_users_by_username(usernames_to_subscribe, message.chat.id)
    else:
        return "you didn't choose any user to subscribe"


def subscribe_users_by_username(usernames_to_subscribe, chat_id):
    response = twitter_responses.response_user_by_username(usernames_to_subscribe)
    sub_if_no_errors(response, True)


def subscribe_users_by_id(ids_to_subscribe, chat_id):
    response = twitter_responses.response_users_by_id(ids_to_subscribe)
    sub_if_no_errors(response, chat_id, True)
