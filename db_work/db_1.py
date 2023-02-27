import redis
import redis_connection as r

# DB for updating last tweets.
db_number = 1
pool = redis.ConnectionPool(host=r.host, port=r.port, db=db_number)
redis = redis.Redis(connection_pool=pool)


def get_map_of_updated_tweets_by_chat_id(chat_id):
    res = redis.hkeys(chat_id)
    return res
    # return [i.decode("utf-8") for i in res]


def update_tweet_in_db(twitter_user, new_tweet_id, chat_id):
    res = redis.hset(chat_id, twitter_user, new_tweet_id)
    return True if res == 1 else False


def remove_twitter_user(twitter_user, chat_id):
    res = redis.hdel(chat_id, twitter_user)
    return True if res == 1 else False


def remove_chat_id(chat_id):
    res = redis.getdel(chat_id)
    return True if res == 1 else False