from Model.DayWatchlistData import DayWatchlistData
from Model.PolygonApi import PolygonApi
from Model.PolygonDailyTickerData import PolygonDailyTickerData
from Model.PolygonMinuteTickerData import PolygonMinuteTickerData
from Model.PolygonTickerDetailsData import PolygonTickerDetailsData
from Model.TradeZeroProTraderVueFormatter import TradeZeroProTraderVueFormatter
from Model.ThinkOrSwimTraderVueFormatter import ThinkOrSwimTraderVueFormatter

from datetime import datetime, timedelta
import pytz
import time

from Model.ThinkOrSwimWatchlistFormatter import ThinkOrSwimWatchlistFormatter
from Resource import properties as p
import runParams as rp

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
    return (f"https://api.polygon.io/v1/open-close/{ticker.upper()}/{format_polygon_date(date)}"
            f"?adjusted=true&apiKey={p.API_KEY}")

def build_ticker_details_request_url(date, ticker):
    return (f"https://api.polygon.io/v3/reference/tickers/{ticker.upper()}?date={format_polygon_date(date)}"
            f"&apiKey={p.API_KEY}")

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
    process_errors = 0
    error_tickers = []
    for ticker in tickers:
        ticker = ticker.upper()
        file_name = create_file_name(date, ticker)
        try:
            minute_bar_data = polygon.get_minute_bars(date, ticker)
            daily_bar_data = polygon.get_daily_bar_data(date, ticker)
            previous_daily_bar_data = polygon.get_daily_bar_data(previous_date, ticker)
            ticker_details_response_data = polygon.get_ticker_details_data(date, ticker)

            data_list = [minute_bar_data, daily_bar_data, previous_daily_bar_data, ticker_details_response_data]
            if None in data_list:
                print(data_list)
                print("no api data")
                raise Exception

            minute_ticker_data = PolygonMinuteTickerData(minute_bar_data)
            daily_ticker_data = PolygonDailyTickerData(daily_bar_data)
            previous_daily_ticker_data = PolygonDailyTickerData(previous_daily_bar_data)
            ticker_details_data = PolygonTickerDetailsData(ticker_details_response_data)

            data_file_string = build_data_file_string(date, ticker, minute_ticker_data, daily_ticker_data,
                                                      previous_daily_ticker_data, ticker_details_data)
            write_data_to_file(file_name, data_file_string)
        except Exception as e:
            process_errors += 1
            error_tickers.append(ticker)
            print(f"Error for ticker {ticker}. Please check \n{e}")
    return process_errors, error_tickers

def run_small_cap_data_collection():
    for i in range(len(rp.TICKERS_BY_DAY)):
        day_watchlist_data = DayWatchlistData(rp.TICKERS_BY_DAY[i])
        tickers = ThinkOrSwimWatchlistFormatter(day_watchlist_data.watchlist).tickers
        process_errors, error_tickers = process_data(day_watchlist_data.trade_date, day_watchlist_data.previous_date, tickers)
        if i+1 < len(rp.TICKERS_BY_DAY):
            time.sleep(61)
        print_time_completed(process_errors, error_tickers)
    print_time_completed()

def medved_to_tos(medved_data):
    # Output with TOS header
    # tos_lines = [",Exec Time,Spread,Side,Qty,Pos Effect,Symbol,Exp,Strike,Type,Price,Net Price,Order Type"]
    tos_lines = []
    data = medved_data.strip().split("\n")[::-1]

    for line in data:
        if line.startswith("Symbol") or line.startswith("Symb") or not line.strip():
            continue

        parts = line.split("\t") #4 spaces
        # print(parts)
        symbol, order_date, action, qty_str, status, fills, *_ = parts

        # Convert COVER → BUY
        side = "BUY" if action.upper() == "COVER" else action.upper()

        # Quantity (remove commas)
        qty = qty_str.replace(",", "")
        qty = f'-{qty}' if side[0] == 'S' else f'+{qty}'

        # Extract fill qty and price from "1500@0.7904 (2)" style
        if "@" in fills:
            after_at = fills.split("@", 1)[1]
            before_at = fills.split("@", 1)[0]
            qty = before_at.replace(",", "")
            qty = f'-{qty}' if side[0] == 'S' else f'+{qty}'
            price = after_at.split()[0]  # take only first number
        else:
            price = ""

        # Convert time from Eastern → Pacific
        dt_et = datetime.strptime(order_date, "%m/%d/%y %I:%M:%S %p")
        dt_pt = dt_et - timedelta(hours=3)
        # print(dt_pt)
        exec_time = dt_pt.strftime("%m/%d/%y %H:%M:%S")

        # Spread = STOCK (always in your example)
        spread = "STOCK"

        # Position effect: TO OPEN if BUY/SHORT, TO CLOSE if SELL/COVER
        pos_effect = "TO OPEN" if side in ("BUY", "SHORT") else "TO CLOSE"

        # Order type: assume LMT if price present, else MKT
        order_type = "LMT" if price else "MKT"

        tos_lines.append(
            f",{exec_time},{spread},{side},{qty},{pos_effect},{symbol},,,STOCK,{price},{price},{order_type}")

    return "\n".join(tos_lines)

def extract_section_as_string(filename, start_marker=",Exec Time,Spread,Side,Qty,Pos Effect,Symbol,Exp,Strike,Type,Price,Net Price,Order Type"):
    section_lines = []
    capture = False

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if capture:
                if stripped == "":
                    break
                section_lines.append(line.rstrip("\n"))
            if stripped == start_marker:
                capture = True

    # Join into one string, like a docstring
    return "\n".join(section_lines)

def run_tradervue_import():
    # DasWebTraderVueFormatter(rp.DAS_HISTORY)
    # DasProTraderVueFormatter(rp.DAS_HISTORY)
    if len(rp.TZ_HISTORY) > 5:
        TradeZeroProTraderVueFormatter(rp.TZ_HISTORY)
    if len(rp.TOS_HISTORY) > 5:
        tos_hist = "../" + extract_section_as_string(rp.TOS_HISTORY.strip()) if ".csv" in rp.TOS_HISTORY else rp.TOS_HISTORY
        print(tos_hist)
        ThinkOrSwimTraderVueFormatter(tos_hist)
    if len(rp.MEDVED_TRADER_HISTORY) > 5:
        medved_data = medved_to_tos(rp.MEDVED_TRADER_HISTORY)
        print(medved_data)
        ThinkOrSwimTraderVueFormatter(medved_data)
    print_time_completed()

def print_time_completed(process_errors=None, tickers=None):
    current_time = datetime.now().strftime("%I:%M:%S %p")
    if None not in [process_errors, tickers]:
        print(f"\nErrors encountered: {process_errors}")
        print(tickers)
    print(f"\n*** Time Completed: {current_time}")

def print_tickers(watchlist):
    ThinkOrSwimWatchlistFormatter(watchlist)
