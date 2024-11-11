"""
This class holds 1 minute candle data returned from polygon api
in the form of:
    Ticker
    ResultsCount
    Results
    Post High Low
"""
class PolygonMinuteTickerData:
    def __init__(self, data):
        self.ticker = data["ticker"]
        self.results_count = data["resultsCount"]
        self.results = data["results"]
        self.post_high_low = -1
        self.find_post_high_low()

    def print_summary(self):
        print(self.ticker)
        print(self.results_count)
        print(self.results)

    def find_post_high_low(self):
        if self.post_high_low > 0:
            return self.post_high_low
        high_of_day = 0
        post_high_low = 0
        for bar in self.results:
            if bar['h'] > high_of_day:
                high_of_day = bar['h']
                post_high_low = bar['c']
            elif bar['l'] < post_high_low:
                post_high_low = bar['l']
        self.post_high_low = post_high_low
        return self.post_high_low
