from Resource import utils as u
import runParams as p

def main():
    u.process_data(p.TRADE_DATE, p.PREVIOUS_DATE, p.TICKERS)
    u.print_time_completed()

if __name__ == '__main__':
    main()

