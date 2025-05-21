import time
from Resource.properties import DISCORD_WEBHOOK_URL
import requests
from datetime import datetime

class TradeZeroProTraderVueFormatter:
    def __init__(self, data):
        self.data = data
        self.file_name = ""
        self.total_trades = dict()
        self.tickers = set()
        self.format_data()
        self.create_file_name()
        self.create_file()

    def send_total_pnl(self):
        print("\nSheets Paste-able")
        for ticker in self.tickers:
            for trade in self.total_trades[ticker]:
                # self.send_discord_message("\t ".join(trade))
                self.write_to_tradervue_file("\t ".join(trade))

    def create_file(self):
        discord_split = '\t \t'
        # self.write_to_tradervue_file("Date,Time,Symbol,Quantity,Price,Side", "Date,Symbol,QTY,Buy,Sell".replace(',', discord_split))
        self.write_to_tradervue_file("Date,Time,Symbol,Quantity,Price,Side")
        today_date = datetime.today().strftime('%Y-%m-%d') #or manually set date
        for row in self.data:
            entry_data, exit_data = self.transform_data(row, today_date)
            entry_string = ','.join(entry_data)
            exit_string = ','.join(exit_data)
            self.write_to_tradervue_file(entry_string)
            self.write_to_tradervue_file(exit_string)
        self.send_total_pnl()

    def transform_data(self, data, today_date):
        symbol = data[0]
        entry_time = data[11].split()[1]
        exit_time = data[12].split()[1]
        entry_side = "B" if data[1].upper() == "LONG" else "SS" #if long else short
        exit_side = "S" if data[1].upper() == "LONG" else "B"
        quantity = str(abs(int(data[5])))
        entry_price = data[7]
        exit_price = data[8]
        buy = entry_price if entry_side == "B" else exit_price
        sell = exit_price if entry_side == "B" else entry_price
        entry_data = [today_date, entry_time, symbol, quantity, entry_price, entry_side]
        exit_data = [today_date, exit_time, symbol, quantity, exit_price, exit_side]
        sheets_date = datetime.strptime(today_date, "%Y-%m-%d").strftime("%m/%d/%Y")
        sheets_data = [symbol, sheets_date, sheets_date, "Notes", "Notes", quantity, buy, sell]
        self.total_trades[symbol] = self.total_trades.get(symbol, []) + [sheets_data]
        self.tickers.add(symbol)
        return entry_data, exit_data

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
                data.append(row.split('\t'))
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