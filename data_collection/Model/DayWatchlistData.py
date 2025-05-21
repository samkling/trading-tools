from datetime import datetime

class DayWatchlistData:
    def __init__(self, data):
        self.watchlist = data[2]
        self.trade_date = data[0]
        self.previous_date = data[1]
