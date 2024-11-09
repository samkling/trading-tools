
class Trade:
    def __init__(self, order_type, symbol):
        self.order_type = order_type.upper() #m or s
        self.symbol = symbol
