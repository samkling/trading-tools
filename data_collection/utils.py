from datetime import datetime
from PolygonTickerData import PolygonTickerData
import os
import pytz
from Properties import properties as p
import requests
import time

MARKET_OPEN = " 09:30:00"
MARKET_CLOSE = " 16:00:00"
DATE_TIME_FORMAT = "%m/%d/%Y %H:%M:%S"
DATE_FORMAT = "%m/%d/%Y"

def get_start_end_milliseconds_from_day(day):
    eastern = pytz.timezone("US/Eastern")
    start_time = int(eastern.localize(datetime.strptime(day+MARKET_OPEN, DATE_TIME_FORMAT)).timestamp() * 1000)
    end_time = int(eastern.localize(datetime.strptime(day+MARKET_CLOSE, DATE_TIME_FORMAT)).timestamp() * 1000)
    return [start_time, end_time]

def build_minute_bars_request_url(date, ticker):
    start_time, end_time = get_start_end_milliseconds_from_day(date)
    url = (f"https://api.polygon.io/v2/aggs/ticker/{ticker.upper()}/range/1/minute/{start_time}/{end_time}?adjusted"
           f"=true&sort=asc&apiKey={p.API_KEY}")
    return url

def get_minute_bar_data_from_api(date, ticker):
    url = build_minute_bars_request_url(date, ticker)
    response = requests.get(url)
    data = None
    if response.status_code == 200:
        data = response.json()
    else:
        print(url)
        print("Request failed with status code:", response.status_code)
    return data

def data_file_exists(file_name):
    file_path = "TickerData/" + file_name + ".txt"
    return os.path.exists(file_path)

def write_data_to_file(file_name, date, ticker, post_high_low):
    with open(file_name, "a") as file:
        file.write(f"{date}\t {ticker}\t {post_high_low}\n")
    print(f"{ticker}\t{post_high_low}")

def ticker_data_exists(file_path, search_string):
    if data_file_exists(file_path):
        with open(file_path, 'r') as file:
            # Iterate through each line in the file
            for line in file:
                if search_string in line:
                    return True  # String found
    return False

def create_file_name(date, ticker):
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
        file_name = create_file_name(date, ticker)
        if not ticker_data_exists(file_name, ticker):
            data = get_minute_bar_data_from_api(date, ticker)
            if data == None:
                print("no data")
                return
            ticker_data = PolygonTickerData(data)
            post_high_low = ticker_data.find_post_high_low()
            write_data_to_file(file_name, date, ticker, post_high_low)
        c += 1

def print_time_completed():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%I:%M:%S %p")
    print("\n*** Time Completed: ", formatted_time)
