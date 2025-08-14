import time
from typing import List, Dict, Any
from collections import defaultdict, deque
from Resource.properties import DISCORD_WEBHOOK_URL
import requests
from datetime import datetime

class ThinkOrSwimTraderVueFormatter:
    def __init__(self, data):
        self.data = data
        self.file_name = ""
        self.total_trades = []
        self.tickers = set()
        self.format_data()
        self.create_file_name()
        self.create_file()
        self.send_total_pnl()

    def executions_to_trades(self, executions: List[List[str]]) -> List[List[Any]]:
        """
        Convert a list of executions into a list of flat trades:
        [date, symbol, quantity, avg_buy_price, avg_sell_price]
        """
        symbol_queue = defaultdict(deque)
        trades = []

        for exec in executions:
            exec.pop()
            date, time, symbol, qty_str, price_str, side = exec
            qty = int(qty_str)
            price = float(price_str)
            side = side.upper()

            symbol_queue[symbol].append({
                'date': date,
                'time': time,
                'symbol': symbol,
                'qty': qty,
                'price': price,
                'side': side
            })

            # Try to flatten when net position reaches 0
            net_pos = 0
            temp_queue = deque()
            for e in symbol_queue[symbol]:
                signed_qty = e['qty'] if e['side'] == 'BUY' else -e['qty']
                net_pos += signed_qty
                temp_queue.append(e)
                if net_pos == 0:
                    break

            if net_pos == 0:
                # Time to close a trade
                buy_qty, buy_total = 0, 0.0
                sell_qty, sell_total = 0, 0.0
                first_date = datetime.strptime(temp_queue[0]['date'], "%Y-%m-%d").strftime("%m/%d/%Y")
                matched_qty = 0

                for e in temp_queue:
                    if e['side'] == 'BUY':
                        buy_qty += e['qty']
                        buy_total += e['qty'] * e['price']
                    else:
                        sell_qty += e['qty']
                        sell_total += e['qty'] * e['price']
                    matched_qty += e['qty'] if e['side'] == 'BUY' else 0  # Only count BUY side as total quantity

                avg_buy = round(buy_total / buy_qty, 5) if buy_qty else 0.0
                avg_sell = round(sell_total / sell_qty, 5) if sell_qty else 0.0

                trades.append([first_date, symbol, buy_qty, avg_buy, avg_sell])

                # Remove matched executions from the queue
                for _ in range(len(temp_queue)):
                    symbol_queue[symbol].popleft()
        return trades

    def send_total_pnl(self):
        print("\nSheets Paste-able")
        trades = self.executions_to_trades(self.total_trades)[::-1]
        for trade in trades:
            t_date, ticker = trade[0:2]
            qty = str(trade[2])
            buy_price = str(trade[3])
            sell_price = str(trade[4])

            print_trade = [ticker, t_date, t_date, 'Notes', 'Notes', qty, buy_price, sell_price]
            self.write_to_tradervue_file("\t ".join(print_trade))

    def create_file(self):
        discord_split = '\t \t'
        # self.write_to_tradervue_file("Date,Time,Symbol,Quantity,Price,Side", "Date,Symbol,QTY,Buy,Sell".replace(',', discord_split))
        self.write_to_tradervue_file("\nDate,Time,Symbol,Quantity,Price,Side,Transfee")
        today_date = datetime.today().strftime('%Y-%m-%d') #or manually set date
        for row in self.data:
            trade = self.get_trade(row, today_date)
            trade_string = ','.join(trade)
            self.write_to_tradervue_file(trade_string)

    def get_trade(self, trade_info, today_date):
        schwab_fee = 0.00016/2 #instead of just adding on the sell, add half to both
        t = trade_info[1].split()[1].split(":")
        print(t[0])
        t[0] = str(int(t[0]) + 3)
        t_time = ":".join(t)
        t_qty = trade_info[4][1:]
        t_symbol = trade_info[6]
        t_price = trade_info[10]
        t_side = trade_info[3]
        trade = [today_date, t_time, t_symbol, t_qty, t_price, t_side, str(int(t_qty)*schwab_fee)]
        self.tickers.add(t_symbol)
        self.total_trades.append(trade)
        return trade

    def write_to_tradervue_file(self, data_string, discord_string=None):
        with open(self.file_name, "a") as file:
            file.write(f"{data_string}\n")
        print(f"{data_string}")
        if discord_string is not None:
            self.send_discord_message(f"{discord_string}")

    def create_file_name(self):
        today_date = datetime.today().strftime('%Y-%m-%d')
        self.file_name = f"TraderVueImport/{today_date}.csv"

    def format_data(self):
        data = []
        self.data = self.data.split('\n')
        for row in self.data:
            if len(row) > 0:
                data.append(row.split(','))
        self.data = data

    def print_data(self):
        for row in self.data:
            print(row)

    def send_discord_message(self, content):
        time.sleep(1)
        data = {
            "content": content  # plain text message
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)

        if response.status_code != 204:
            print(f"Failed to send message: {response.status_code}, {response.text}")