import redis

storage_twitter_subscription = "storage_twitter_subscription.txt"


import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

redis.set('mykey', 'Hello from Python!')
value = redis.get('mykey')
print(value)

redis.zadd('vehicles', {'car' : 0})
redis.zadd('vehicles', {'bike' : 0})
vehicles = redis.zrange('vehicles', 0, -1)
print(vehicles)

def add_to_set_from_file(file):
    id_set = set()
    with open(file, "r") as f:
        ids = f.readlines()
        for id in ids:
            id = id.replace("\n", '')
            id_set.add(id)
    return id_set


def add_user_to_storage_subscription(id_to_add):
    id_set = add_to_set_from_file(storage_twitter_subscription)
    if id_to_add not in id_set:
        with open(storage_twitter_subscription, "a") as f:
            f.write(id_to_add + "\n")
        return True
    else:
        return False


def unsubscribe_user_from_storage_subscription(id_to_unsubscribe):
    id_set = add_to_set_from_file(storage_twitter_subscription)
    if id_to_unsubscribe in id_set:
        id_set.remove(id_to_unsubscribe)
        with open(storage_twitter_subscription, "w") as f:
            for id in id_set:
                f.write(id + "\n")
        return True
    else:
        return False
