#
# Idea is to use this to make the Das Web easier to use
#
# order entry/positions size calculation to start
# look into maybe piggybacking on network tab
# maybe bottle w/ simple template?
#
#
import time

import trader_commands as trader

ENTER_TRADE = 'action symbol or q: '

if __name__ == '__main__':
    running = input(ENTER_TRADE)
    while running != 'q':
        trade_details = running.split()
        trader.trade(trade_details)
        print(trade_details)
        running = input(ENTER_TRADE)

    print('done')
