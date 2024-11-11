from Model.PolygonApi import PolygonApi
from Model.PolygonDailyTickerData import PolygonDailyTickerData
from Model.PolygonMinuteTickerData import PolygonMinuteTickerData
from Model.PolygonTickerDetailsData import PolygonTickerDetailsData

from datetime import datetime
import os
import pytz
from Resource import properties as p

MARKET_OPEN = " 09:30:00"
MARKET_CLOSE = " 16:00:00"
DATE_TIME_FORMAT = "%m/%d/%Y %H:%M:%S"
DATE_FORMAT = "%m/%d/%Y"

def get_start_end_milliseconds_from_day(day):
    eastern = pytz.timezone("US/Eastern")
    start_time = int(eastern.localize(datetime.strptime(day+MARKET_OPEN, DATE_TIME_FORMAT)).timestamp() * 1000)
    end_time = int(eastern.localize(datetime.strptime(day+MARKET_CLOSE, DATE_TIME_FORMAT)).timestamp() * 1000)
    return [start_time, end_time]

def format_polygon_date(date):
    date_parts = date.split("/")
    return f"{date_parts[2]}-{date_parts[0]}-{date_parts[1]}"

def build_minute_bars_request_url(date, ticker):
    start_time, end_time = get_start_end_milliseconds_from_day(date)
    url = (f"https://api.polygon.io/v2/aggs/ticker/{ticker.upper()}/range/1/minute/{start_time}/{end_time}?adjusted"
           f"=true&sort=asc&apiKey={p.API_KEY}")
    return url

def build_daily_bar_request_url(date, ticker):
    return f"https://api.polygon.io/v1/open-close/{ticker.upper()}/{format_polygon_date(date)}?adjusted=true&apiKey={p.API_KEY}"

def build_ticker_details_request_url(date, ticker):
    return f"https://api.polygon.io/v3/reference/tickers/{ticker.upper()}?date={format_polygon_date(date)}&apiKey={p.API_KEY}"

def data_file_exists(file_name):
    file_path = f"TickerData/{file_name}.txt"
    return os.path.exists(file_path)

def write_data_to_file(file_name, data_string):
    with open(file_name, "a") as file:
        file.write(f"{data_string}\n")
    print(f"{data_string}")

def create_file_name(date, ticker):
    return "TickerData/" + date.replace("/", "-")+ ".txt"

def build_data_file_string(date, ticker, minute_data, daily_data, previous_daily_data, ticker_details_data):
    mkt_cap = None
    if ticker_details_data.market_cap < 0:
        mkt_cap = ticker_details_data.shares_outstanding * daily_data.close
    else:
        mkt_cap = ticker_details_data.market_cap
    return (f"{date}\t {ticker.upper()}\t {daily_data.get_tabbed_ohlc()}\t "
            f"{minute_data.post_high_low}\t {previous_daily_data.close}\t "
            f"{mkt_cap}\t {daily_data.volume}")

def process_data(date, previous_date, tickers):
    polygon = PolygonApi()
    for ticker in tickers:
        ticker = ticker.upper()
        file_name = create_file_name(date, ticker)

        minute_bar_data = polygon.get_minute_bars(date, ticker)
        daily_bar_data = polygon.get_daily_bar_data(date, ticker)
        previous_daily_bar_data = polygon.get_daily_bar_data(previous_date, ticker)
        ticker_details_response_data = polygon.get_ticker_details_data(date,ticker)

        data_list = [minute_bar_data, daily_bar_data, previous_daily_bar_data, ticker_details_response_data]
        if None in data_list:
            print(data_list)
            print("no data")
            return

        minute_ticker_data = PolygonMinuteTickerData(minute_bar_data)
        daily_ticker_data = PolygonDailyTickerData(daily_bar_data)
        previous_daily_ticker_data = PolygonDailyTickerData(previous_daily_bar_data)
        ticker_details_data = PolygonTickerDetailsData(ticker_details_response_data)

        data_file_string = build_data_file_string(date, ticker, minute_ticker_data, daily_ticker_data, previous_daily_ticker_data, ticker_details_data)
        write_data_to_file(file_name, data_file_string)

def print_time_completed():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%I:%M:%S %p")
    print("\n*** Time Completed: ", formatted_time)
