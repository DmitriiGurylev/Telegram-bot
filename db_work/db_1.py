import redis
from db_work import redis_connection


# DB for updating last tweets.
db_number = 1
pool = redis.ConnectionPool(host=redis_connection.host, port=redis_connection.port, db=db_number)
redis = redis.Redis(connection_pool=pool)


def get_chat_ids():  # get list of chat ids
    res = redis.keys()
    return [i.decode("utf-8") for i in res]


def get_list_of_user_ids(chat_id):  # get list of Twitter user ids
    chat_ids_set = set()
    chat_ids_set.update(get_chat_ids())
    if chat_id not in chat_ids_set:
        return []
    res = redis.hkeys(chat_id)  # get list of Twitter user ids
    return [i.decode("utf-8") for i in res]


def get_list_of_newest_tweets(chat_id, user_id):  # get newest_tweet_id of user
    res = redis.hget(chat_id, user_id)
    return res.decode("utf-8")


def update_tweet_in_db(twitter_user_id, new_tweet_id, chat_id):
    res = redis.hset(chat_id, twitter_user_id, new_tweet_id)
    return True if res == 1 else False


def remove_twitter_user(twitter_user_id, chat_id):
    res = redis.hdel(chat_id, twitter_user_id)
    return True if res == 1 else False


def remove_chat_id(chat_id):
    res = redis.getdel(chat_id)
    return True if res == 1 else False
