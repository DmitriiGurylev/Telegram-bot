# twitter

twitter_users_tweets_url = 'https://api.twitter.com/2/users/:id/tweets'
twitter_users_by_id_url = 'https://api.twitter.com/2/users?ids='
twitter_users_by_username_url = 'https://api.twitter.com/2/users/by?usernames='
twitter_user_timeline_url = 'https://api.twitter.com/2/users/:id/tweets'

twitter_users_tweets = {
    'id': None,
    'exclude': None,
    'expansions': None,
    'max_results': None,
    'media.fields': None,
    'pagination_token': None,
    'place.fields': None,
    'poll.fields': None,
    'since_id': None,
    'start_time': None,
    'end_time': None,
    'tweet.fields': None,
    'until_id': None,
    'user.fields': None
}

twitter_tweets_url = 'https://api.twitter.com/2/tweets'
twitter_tweets = {
    'ids': None,
    'tweet.fields': 'created_at',
    'expansions': 'author_id',
    'user.fields': 'created_at'
}

twitter_user_timeline = {
    'user_id': None,
    'screen_name': None,
    'since_id': None,
    'count': None,
    'max_id': None,
    'trim_user': None,
    'exclude_replies': None,
    'include_rts': None,
}
