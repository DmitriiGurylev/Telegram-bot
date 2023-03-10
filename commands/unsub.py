import twitter_responses
from write_messages import unsubscribe_msg_if_no_users, get_list_of_user_ids, sub_unsub_if_no_errors


def unsubscribe_by_id(message):
    message_text_array = message.text.split(' ')
    user_ids_to_unsubscribe = message_text_array[1:]

    if user_ids_to_unsubscribe:
        unsubscribe_users_by_id(user_ids_to_unsubscribe, message.chat.id)
    else:
        unsubscribe_msg_if_no_users(message.chat.id)


def unsubscribe(message):
    message_text_array = message.text.split(' ')
    usernames_to_unsubscribe = message_text_array[1:]

    if usernames_to_unsubscribe:
        unsubscribe_users_by_username(usernames_to_unsubscribe, message.chat.id)
    else:
        unsubscribe_msg_if_no_users(message.chat.id)


def unsubscribe_users_by_username(usernames_to_unsubscribe, chat_id):
    response = twitter_responses.response_user_by_username(usernames_to_unsubscribe)
    sub_unsub_if_no_errors(response, chat_id, False)


def unsubscribe_users_by_id(ids_to_unsubscribe, chat_id):
    response = twitter_responses.response_users_by_id(ids_to_unsubscribe)
    sub_unsub_if_no_errors(response, chat_id, False)


def unsubscribe_from_all(chat_id):
    id_list = get_list_of_user_ids(chat_id)
    unsubscribe_users_by_id(id_list, chat_id)
