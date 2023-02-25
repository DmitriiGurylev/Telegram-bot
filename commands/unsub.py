import twitter_responses
from db_work.db_0 import get_list_by_chat_id
from write_messages import unsubscribe_msg, unsubscribe_msg_if_no_users


def unsubscribe_by_id(message):
    message_text_array = message.text.split(' ')
    user_ids_to_unsubscribe = message_text_array[1:]

    if user_ids_to_unsubscribe:
        unsubscribe_users_by_id(user_ids_to_unsubscribe, message)
    else:
        unsubscribe_msg_if_no_users(message)


def unsubscribe(message):
    message_text_array = message.text.split(' ')
    usernames_to_unsubscribe = message_text_array[1:]

    if usernames_to_unsubscribe:
        unsubscribe_users_by_username(usernames_to_unsubscribe, message)
    else:
        unsubscribe_msg_if_no_users(message)


def unsubscribe_users_by_username(usernames_to_unsubscribe, message):
    response = twitter_responses.response_user_by_username(usernames_to_unsubscribe)
    unsubscribe_msg(response, message)


def unsubscribe_users_by_id(ids_to_unsubscribe, message):
    response = twitter_responses.response_users_by_id(ids_to_unsubscribe)
    unsubscribe_msg(response, message)


def unsubscribe_from_all(message):
    id_list = get_list_by_chat_id(message.chat.id)
    unsubscribe_users_by_id(id_list, message)
