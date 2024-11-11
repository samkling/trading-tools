"""
ticker details API Response
    https://polygon.io/docs/stocks/get_v3_reference_tickers__ticker

"""
class PolygonTickerDetailsData:
    def __init__(self, data):
        try:
            self.market_cap = data["results"]["market_cap"]
            self.shares_outstanding = 0
        except KeyError:
            print(f"{data['results']['ticker']} doesn't have market cap data")
            self.shares_outstanding = data['results']['share_class_shares_outstanding']
            self.market_cap = -1

    def print_summary(self):
        print(self.market_cap)
