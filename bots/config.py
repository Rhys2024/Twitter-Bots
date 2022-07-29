# tweepy-bots/bots/config.py
import tweepy
import logging
import os

logger = logging.getLogger()

def create_connections():
    #global auth
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAJLzbAEAAAAAxypUCF8cE6XLi1vFt6sjo3BqzHQ%3DXsckmuHJbjYM0zLYbJxnw0ojahbHBQpJISKyrsTj0i9L2q3W28"
    consumer_key = "Ot5FjgEUNOZoiUZQDWeHoFRtB"
    consumer_secret = "4FgYFlbc7rgv862hhaYq3qu4EtYa7Hut11ozWbvHucvlqdB7do"
    access_token = "1512071827689857031-7KPWVREXJgWqLrcltMjpUz0k9FUtHd"
    access_token_secret = "Whi1mjIHDmQ0Bnf8cbYnCHDxJCH47XA6zUmDNeneYbmQi"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    client = tweepy.Client(bearer_token,api.auth.consumer_key, api.auth.consumer_secret, 
                        api.auth.access_token, api.auth.access_token_secret)
    
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    
    return {"Client" : client, "API" : api, "Bearer" : bearer_token}