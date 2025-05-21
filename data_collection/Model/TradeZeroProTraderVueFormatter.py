import time

import requests
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1361901870536462526/BWXuWZormp__LbnTaNj9Kn26ReYf7_XNE8B7AGxFy_IKbC9mm0SH3E1Dk_Ze6aSdu8eN"

class TradeZeroProTraderVueFormatter:
    def __init__(self, data):
        self.data = data
        self.file_name = ""
        self.total_pnl = dict()
        self.total_trades = dict()
        self.format_data()
        self.create_file_name()
        self.create_file()
        # self.send_total_pnl()

    def send_total_pnl(self):
        print(self.total_pnl)
        for ticker, pnl in self.total_pnl.values():
            for trade in self.total_trades[ticker]:
                self.send_discord_message(",".join(trade))
            self.send_discord_message(f"{ticker}\t\t{pnl}")

    def create_file(self):
        discord_split = '\t \t'
        self.write_to_tradervue_file("Date,Time,Symbol,Quantity,Price,Side", "Date,Symbol,QTY,Buy,Sell".replace(',', discord_split))
        today_date = datetime.today().strftime('%Y-%m-%d') #or manually set date
        for row in self.data:
            entry_data, exit_data = self.transform_data(row, today_date)
            entry_string = ','.join(entry_data)
            exit_string = ','.join(exit_data)
            self.write_to_tradervue_file(entry_string)
            self.write_to_tradervue_file(exit_string)

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
        sheets_data = [today_date, symbol, quantity, buy, sell]
        self.total_pnl[symbol] = self.total_pnl.get(symbol, 0) + (float(exit_price) - float(entry_price)) * int(quantity)
        self.total_trades[symbol] = sheets_data
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
        response = requests.post(WEBHOOK_URL, json=data)

        if response.status_code != 204:
            print(f"Failed to send message: {response.status_code}, {response.text}")