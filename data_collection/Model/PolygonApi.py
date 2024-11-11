from Resource import utils as u

from datetime import datetime
import time
import requests

"""
    Free tier of Polygon API has a maximum of 5 calls per minute. 
    This class will keep track of number of calls and sleep when appropriate
"""
class PolygonApi:
    def __init__(self):
        self.call_count = 0

    def make_api_call(self):
        if (self.call_count % 5 == 0) and (self.call_count != 0):
            print(f"API Call Limit Timeout - {datetime.now().strftime('%I:%M:%S %p')}")
            time.sleep(60)
            print(f"Resumed - {datetime.now().strftime('%I:%M:%S %p')}")
        self.call_count += 1

    def get_minute_bars(self, date, ticker):
        self.make_api_call()
        url = u.build_minute_bars_request_url(date, ticker)

        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = response.json()
        else:
            print(url)
            print("Minute Bar request failed with status code:", response.status_code)
        return data

    def get_daily_bar_data(self, date, ticker):
        self.make_api_call()
        url = u.build_daily_bar_request_url(date, ticker)

        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = response.json()
        else:
            print(url)
            print("Daily Bar request failed with status code:", response.status_code)
        return data

    def get_ticker_details_data(self, date, ticker):
        self.make_api_call()
        url = u.build_ticker_details_request_url(date,ticker)

        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = response.json()
        else:
            print(url)
            print("Ticker Details request failed with status code:", response.status_code)
        return data
