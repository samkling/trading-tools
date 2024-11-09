import pyautogui as p
import time as t
from trade import Trade

WINDOW_CLICK = [519, 188]
ORDER_INPUTS_Y = 330
SYMBOL_X = 300
ORDER_TYPE_X = 635
ROUTE_X = 1020

def click_window():
    p.moveTo(WINDOW_CLICK[0], WINDOW_CLICK[1])
    p.click()
    t.sleep(.55)

def clear_field():
    t.sleep(.1)
    p.hotkey('command', 'a')
    p.press('backspace')

def reset_order_window():
    p.moveTo(SYMBOL_X, ORDER_INPUTS_Y)
    p.click()
    clear_field()
    p.typewrite('aapl')
    p.press('enter')
    click_window()
    p.moveTo(SYMBOL_X, ORDER_INPUTS_Y)
    p.click()
    clear_field()
    p.press('enter')
def type_symbol(trade):
    p.moveTo(SYMBOL_X, ORDER_INPUTS_Y)
    p.click()
    p.typewrite(trade.symbol)
    p.press('enter')
    click_window()
    t.sleep(1)

# def get_bid():
#     p.moveTo(445,370)
#     p.click(clicks=2)
#     p.hotkey('command', 'c')
#     print(pc.paste())

def set_order_type(trade):
    p.moveTo(ORDER_TYPE_X, ORDER_INPUTS_Y)
    p.click()
    if trade.order_type == 'M': #market order
        p.press('down')
        p.press('enter')
    elif trade.order_type == 'S':
        pass
    click_window()

def set_order_route(trade):
    p.moveTo(ROUTE_X, ORDER_INPUTS_Y)
    p.click()
    if trade.order_type == "M": #market order CPGOS
        p.press('down')
        p.press('down')
        p.press('enter')
    elif trade.order_type == 'S':
        pass
    click_window()

# def set_quantity(trade, bid):
#     p.moveTo(450, ORDER_INPUTS_Y)
#     p.click()
#     shares = (trade.stop - bid) // trade.risk
#     p.typewrite(shares)

def setup_order(trade):
    type_symbol(trade)
    set_order_type(trade)
    set_order_route(trade)

def trade(trade):
    click_window()
    reset_order_window()
    new_trade = Trade(trade[0], trade[1])
    setup_order(new_trade)



