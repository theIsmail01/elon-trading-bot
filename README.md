# elon-trading-bot

## DESCRIPTION

This bot is designed to buy dogecoin every time Elon musk tweets about dogecoin with the following parameters:
  1) The tweet mentions dogecoin.
  2) The overall sentiment of the tweet is positive.
  3) No current order or position is in place.

The bot will open a buy position with 50x leverage on dogecoin every time the above 3 conditions are being met.
Take profit is set to when the price rises by 10%.

The bot uses the Tweepy API and a Twitter developer account that you will need access to, as well as Binance account.

Natural Language ToolKit (NLKT) python library is being used to evaluate the sentiment of the tweet.

## IMPORTANT NOTE:
This particular project is mainly built for fun and the novelty of it. it has not been tested on a live account and there isn't any details analysis to suggest this might work.

If you do test this, please share the results!
