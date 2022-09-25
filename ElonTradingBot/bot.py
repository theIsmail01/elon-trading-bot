import tweepy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


from datetime import date
import time


from config import api_key, api_secret_key, access_key, access_key_secret, binance_api_key, binance_secret_key


from binance.client import Client
from binance.enums import *


import re


BALANCE = 10000
TRADESYMBOL = "DOGEUSD"
keywords = set(['Bitcoin', 'bitcoin', 'BITCOIN', 'btc', 'BTC', 'Dogecoin', 'DOGECOIN',
                'dogecoin', 'doge', 'crypto', 'Crypto', 'CRYPTO', 'cryptocurreny', 'DOGEUSD', 'Dogeusd', 'dogeusd'])
LEVERAGE = 50


auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_key, access_key_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


client = Client(binance_api_key, binance_secret_key)


def get_new_tweets():
    latest_tweet = tweepy.Cursor(api.user_timeline, id="44196397",
                                 since=date.today(), tweet_mode='extended').items(1)

    # remove all invalid characters and pictures or anything other than text
    text_of_latest_tweet = re.sub('[^A-Za-z0-9]+', ' ', latest_tweet.full_text)

    # Check if this tweet mentions crypto/doge anywhere
    for word in nltk.word_tokenize(text_of_latest_tweet):
        if word in keywords:
            return text_of_latest_tweet

    return ""


def analyze_elon_latest_tweet(tweet):
    if tweet == "":
        return False

    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(tweet)

    if score['pos'] > score['neg']:
        return True
    return False


def send_trade(score):
    doge_price = client.get_symbol_ticker(symbol="DOGEUSDT")
    doge_price = doge_price['price']
    # Update leverage to 50 before sending a buy order
    client.futures_change_leverage(leverage=LEVERAGE)
    client.create_order(
        symbol=TRADESYMBOL,
        side='BUY',
        type='MARKET',
        timeInForce='GTC',
        quoteOrderQty=BALANCE,
        tp=doge_price * 1.1
    )


def order_in_place():
    orders = client.get_all_orders()
    if orders:
        return True
    return False


def position_in_place():
    positions = client.futures_account()['position']
    if positions:
        return True
    return False


def main():

    while True:

        # Check if a buy order or position is already being placed or active
        if not order_in_place() and not position_in_place():

            # Get the latest tweet made by Elon Musk if it containes any reference to Dogecoin
            tweet = get_new_tweets()

            # Analyze the tweet using nltk library,
            # if the sentiment is positive, then it return True which is a buy signal
            if analyze_elon_latest_tweet(tweet):

                # Hence, if the sentiment is positive, send order to buy dogecoin
                send_trade()

        # Sleep for a minute to avoid spamming
        time.sleep(5)


if __name__ == "__main__":
    main()
