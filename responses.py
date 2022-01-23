import json

import requests

import config
import twitterApi


def response_bank(api):  # read data  and deserialize them from API
    response = requests.get(api)
    deserial = json.loads(response.text)
    return deserial


def response_twitter_last5tweets_of_the_user(user_id):  # read data of tweet and deserialize them from API

    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token

    my_params = twitterApi.twitter_users_tweets.copy()

    my_params['tweet.fields'] = "created_at"
    my_params['max_results'] = 5

    response = requests.get(
        twitterApi.twitter_users_tweetsUrl.replace(":id", user_id),
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


def response_twitter_userSubscribeTweets(user_id, start_time):  # read data of tweet and deserialize them from API

    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token

    my_params = twitterApi.twitter_users_tweets.copy()
    my_params['tweet.fields'] = "created_at"
    my_params['start_time'] = start_time

    response = requests.get(
        twitterApi.twitter_users_tweetsUrl.replace(":id", user_id),
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


def response_twitter_tweets(messages_id):  # read data of tweet and deserialize them from API

    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token

    my_params = twitterApi.twitter_tweets.copy()
    my_params['ids'] = messages_id

    response = requests.get(
        twitterApi.twitter_tweetsUrl,
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


def response_stasuses_user_timeline(user_id):  # read data and deserialize them from API

    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token

    my_params = twitterApi.twitter_users_tweets.copy()
    my_params['user_id'] = user_id

    response = requests.get(
        twitterApi.twitter_users_tweetsUrl,
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response
