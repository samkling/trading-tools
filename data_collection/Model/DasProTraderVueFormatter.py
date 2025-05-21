import time
from Resource.properties import DISCORD_WEBHOOK_URL
import requests
from datetime import datetime

class DasProTraderVueFormatter:
    def __init__(self, data):
        self.data = data.split('\n')
        self.file_name = ""
        self.format_data()
        self.create_file_name()
        self.create_file()

    def create_file(self):
        discord_split = '\t \t'
        self.write_to_tradervue_file("Date,Time,Symbol,Quantity,Price,Side,Commission,ECNFee", "Date,Time,Symbol,Side,QTY,Price".replace(',', discord_split))
        today_date = datetime.today().strftime('%Y-%m-%d') #or manually set date
        for row in self.data:
            data_string = ','.join([today_date, row[0], row[1], row[2], row[3], row[4], str(int(row[2])*0.003), row[6]])
            discord_string = discord_split.join([today_date, row[0], row[1], row[4], row[2], row[3]])
            self.write_to_tradervue_file(data_string,discord_string)

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