from Resource import utils as u
import runParams as p

def main():
    u.gather_data(p.TRADE_DATE, p.TICKERS)
    u.print_time_completed()

if __name__ == '__main__':
    main()

