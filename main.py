import requests
import datetime
from privates import *

#Find previous active trading day
TODAY = datetime.date.today()

def prev_business_day(query_day):
    query_day -= datetime.timedelta(days=1)
    while query_day.weekday() > 4:  # Mon-Fri are 0-4
        query_day -= datetime.timedelta(days=1)
    return query_day

YESTERDAY = prev_business_day(TODAY)

NEWS_API = NEWS_API

STOCK_API = STOCK_API
STOCK = STOCK
COMPANY_NAME = COMPANY_NAME

STOCK_ENDPOINT = STOCK_ENDPOINT
NEWS_ENDPOINT = NEWS_ENDPOINT

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "outputsize": "compact",
    "apikey": STOCK_API,
    "symbol": STOCK,
}

news_params = {
    "apiKey": NEWS_API,
    "qInTitle": COMPANY_NAME,
    "from": YESTERDAY,
    "sortBy": "publishedAt",
}

news_response = requests.get(url=NEWS_ENDPOINT,params=news_params)
news_response.raise_for_status()
news_data = news_response.json()
#print(news_data["articles"][0:1])

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()

previous_previous_close = float(stock_data["Time Series (Daily)"][str(prev_business_day(YESTERDAY))]["1. open"])
previous_close = float(stock_data["Time Series (Daily)"][str(prev_business_day(TODAY))]["4. close"])



if previous_close > previous_previous_close:
    percent_diff = 100 - (previous_previous_close / previous_close * 100)
    direction = "up"
elif previous_close < previous_previous_close:
    percent_diff = 100 - (previous_close / previous_previous_close * 100)
    direction = "down"

percent_diff = float("{:.2f}".format(percent_diff))
print(f"At previous close, {STOCK} was {percent_diff}% {direction} compared to close on {str(prev_business_day(YESTERDAY))}\n")

if percent_diff > 5:
    print("Greater than 5")
    print("Get News")

#print(news_data)
for i in range(0,3):
    print(news_data["articles"][i]["title"])
    print(news_data["articles"][i]["description"])
    print("\n")

## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number.
#HINT 1: Consider using a List Comprehension.


