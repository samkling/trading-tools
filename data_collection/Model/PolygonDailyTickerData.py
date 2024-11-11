"""
Daily Ticker Data OHLC/Volume
"""
class PolygonDailyTickerData:
    def __init__(self, data):
        self.ticker = data["symbol"]
        self.open = data["open"]
        self.high = data["high"]
        self.low = data["low"]
        self.close = data["close"]
        self.volume = data["volume"]

    def print_summary(self):
        print(self.ticker)
        print(self.open)
        print(self.high)
        print(self.low)
        print(self.close)
        print(self.volume)

    def get_tabbed_ohlc(self):
        return f"{self.open}\t {self.high}\t {self.low}\t {self.close}"
