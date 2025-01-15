"""
 [ticker, GAP, HOD, Fade, Signal]
"""
class ThinkOrSwimWatchlistFormatter:
    def __init__(self, data):
        self.data = data
        self.tickers = []
        self.format_data()

    def format_data(self):
        data_array = self.data.strip().split('\n')
        print("Data count: ", len(data_array))
        self.tickers = []
        for item in data_array:
            ticker_data = item.split('\t')
            try:
                self.tickers.append(ticker_data[0]) #get ticker
            except Exception as e:
                print(e)
                print("Error getting ticker in ThinkOrSwimWatchlistFormatter")
                print("Data String: ", ticker_data)
        print("Tickers count: ", len(self.tickers))
        print(f"Tickers: {self.tickers}\n")