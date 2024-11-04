from datetime import datetime
from TickerData import TickerData
import os
import pytz
import properties as p
import requests
import time

MARKET_OPEN = " 09:30:00"
MARKET_CLOSE = " 16:00:00"
DATE_TIME_FORMAT = "%m/%d/%Y %H:%M:%S"
DATE_FORMAT = "%m/%d/%Y"

def getStartEndMillisecondsFromDay(day):
    eastern = pytz.timezone("US/Eastern")
    start_time = int(eastern.localize(datetime.strptime(day+MARKET_OPEN, DATE_TIME_FORMAT)).timestamp() * 1000)
    end_time = int(eastern.localize(datetime.strptime(day+MARKET_CLOSE, DATE_TIME_FORMAT)).timestamp() * 1000)
    return [start_time, end_time]

def buildMinuteBarsRequestUrl(date,ticker):
    start_time, end_time = getStartEndMillisecondsFromDay(date)
    url = (f"https://api.polygon.io/v2/aggs/ticker/{ticker.upper()}/range/1/minute/{start_time}/{end_time}?adjusted"
           f"=true&sort=asc&apiKey={p.API_KEY}")
    return url

def getMinuteBarDataFromApi(date, ticker):
    url = buildMinuteBarsRequestUrl(date, ticker)
    response = requests.get(url)
    data = None
    if response.status_code == 200:
        data = response.json()
    else:
        print("Request failed with status code:", response.status_code)
    return data

def dataFileExists(file_name):
    file_path = "TickerData/" + file_name + ".txt"
    return os.path.exists(file_path)

def writeDataToFile(file_name, date, ticker, post_high_low):
    with open(file_name, "a") as file:
        file.write(f"{date}    {ticker}    {post_high_low}\n")
    print(f"{ticker} {post_high_low}")

def tickerDataExists(file_path, search_string):
    if dataFileExists(file_path):
        with open(file_path, 'r') as file:
            # Iterate through each line in the file
            for line in file:
                if search_string in line:
                    return True  # String found
    return False

def createFileName(date, ticker):
    return "TickerData/" + date.replace("/", "-")+ ".txt"

def timeout_api_calls():
    print("API Call Limit Timeout")
    time.sleep(60)
    print("Resumed")

def gather_data(date, tickers):
    c = 0
    for ticker in tickers:
        if (c % 5 == 0) and (c != 0):
            timeout_api_calls()
        ticker = ticker.upper()
        file_name = createFileName(date, ticker)
        if not tickerDataExists(file_name, ticker):
            data = getMinuteBarDataFromApi(date, ticker)
            ticker_data = TickerData(data)
            post_high_low = ticker_data.findPostHighLow()
            writeDataToFile(file_name, date, ticker, post_high_low)
        c += 1

def print_time_completed():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%I:%M:%S %p")

    print("\n*** Time Completed: ", formatted_time)