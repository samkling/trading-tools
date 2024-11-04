import utils as u

if __name__ == '__main__':
    date = "10/24/2024"
    tickers = """
    CTNT
TRIB
PCT
CMAX
CLIK
OPTX
VCNX
TWG
ALGS
NUKK
ZCAR
QNCX
LQR
NXL
ATGL
UPXI
EFSH
TCBP
MNPR
TVGN
ZENA
CCTG
NXU
LGCB
    """.split()

    u.gather_data(date, tickers)
    u.print_time_completed()
