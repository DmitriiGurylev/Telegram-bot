import json
import requests
import config
import twitter_api


def response_user_by_username(user_names):
    my_headers = {'Authorization': 'Bearer ' + config.twitter_bearer_token}
    my_params = ','.join(user_names)
    response = requests.get(
        twitter_api.twitter_users_by_username_url + my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


def response_users_by_id(user_ids):
    my_headers = {'Authorization': 'Bearer ' + config.twitter_bearer_token}
    my_params = ','.join(user_ids)
    response = requests.get(
        twitter_api.twitter_users_by_id_url + my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


def response_twitter_last_tweets_of_the_user(user_id,
                                             number_of_msg):  # read data of tweet and deserialize them from API
    my_headers = {'Authorization': 'Bearer ' + config.twitter_bearer_token}

    my_params = dict()

    my_params['tweet.fields'] = "created_at"
    my_params['max_results'] = number_of_msg
    response = requests.get(
        twitter_api.twitter_users_tweets_url.replace(":id", user_id),
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


# read data of tweet and deserialize them from API
def response_twitter_user_subscribe_tweets(user_id, since_id):
    my_headers = {'Authorization': 'Bearer ' + config.twitter_bearer_token}

    my_params = dict()
    my_params['tweet.fields'] = "created_at"
    if since_id != '-1':
        my_params['since_id'] = since_id
    response = requests.get(
        twitter_api.twitter_users_tweets_url.replace(":id", user_id),
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


def get_last_tweet_of_user(user_id):
    my_headers = {'Authorization': 'Bearer ' + config.twitter_bearer_token}

    my_params = dict()
    my_params['max_results'] = 5
    response = requests.get(
        twitter_api.twitter_user_timeline_url.replace(":id", user_id),
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response
