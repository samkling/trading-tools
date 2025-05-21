import os
from Resource import utils as u

def main():
    run_config = os.getenv('RUN_CONFIG')

    match run_config:
        case 'TRADERVUE':
            u.run_tradervue_import()
        case 'DATA':
            u.run_small_cap_data_collection()  # run small cap data for Google sheets
        case _: # fallback
            print(f"No RUN_CONFIG for {run_config}")
            # u.print_tickers(u.rp.wl.TICKERS_14_trim)

if __name__ == '__main__':
    main()
