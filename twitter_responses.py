import json
import requests
import config
import twitterApi


def response_users_by_username(user_names):
    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token
    my_params = ','.join(user_names)
    response = requests.get(
        twitterApi.twitter_users_by_username_url + my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response

def response_user_by_username(user_name):
    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token
    my_params = user_name
    response = requests.get(
        twitterApi.twitter_users_by_username_url + my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


def response_users_by_id(user_ids):
    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token
    my_params = ','.join(user_ids)
    response = requests.get(
        twitterApi.twitter_users_by_id_url + my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


def response_user_by_id(user_id):
    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token
    my_params = user_id
    response = requests.get(
        twitterApi.twitter_users_by_id_url + my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response

# def responsetweets_by_user():


def response_twitter_last_tweets_of_the_user(user_id, number_of_msg):  # read data of tweet and deserialize them from API

    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token

    my_params = twitterApi.twitter_users_tweets.copy()

    my_params['tweet.fields'] = "created_at"
    my_params['max_results'] = number_of_msg

    response = requests.get(
        twitterApi.twitter_users_tweets_url.replace(":id", user_id),
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


# read data of tweet and deserialize them from API
def response_twitter_user_subscribe_tweets(user_id, start_time, end_time):

    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token

    my_params = twitterApi.twitter_users_tweets.copy()
    my_params['tweet.fields'] = "attachments," \
                                "created_at," \
                                "author_id," \
                                "context_annotations," \
                                "conversation_id," \
                                "entities," \
                                "geo," \
                                "id," \
                                "in_reply_to_user_id," \
                                "lang," \
                                "public_metrics," \
                                "possibly_sensitive," \
                                "referenced_tweets," \
                                "reply_settings," \
                                "source," \
                                "text," \
                                "withheld"
    my_params['start_time'] = start_time
    my_params['end_time'] = end_time

    response = requests.get(
        twitterApi.twitter_users_tweets_url.replace(":id", user_id),
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
        twitterApi.twitter_tweets_url,
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response


def response_statuses_user_timeline(user_id):  # read data and deserialize them from API

    my_headers = {}
    my_headers['Authorization'] = 'Bearer ' + config.twitter_bearer_token

    my_params = twitterApi.twitter_user_timeline.copy()
    my_params['user_id'] = user_id

    response = requests.get(
        twitterApi.twitter_user_timeline_url,
        params=my_params,
        headers=my_headers
    )
    json_response = response.json()
    return json_response
