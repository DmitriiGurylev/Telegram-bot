import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)


def get_list_by_chat_id(chat_id):
    res = redis.smembers(chat_id)
    return res


def add_user_to_storage_subscription(id_to_add, chat_id):
    res = redis.sadd(chat_id, id_to_add)
    return True if res == 1 else False


def unsubscribe_user_from_storage_subscription(id_to_unsubscribe, chat_id):
    res = redis.srem(chat_id, id_to_unsubscribe)
    return True if res == 1 else False
