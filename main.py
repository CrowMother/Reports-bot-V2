# reports bot main

import os
import logging
import Bot_App as bot
import dotenv
from Bot_App import gsheet, util, schwab, data, SQL


FILTER = "FILLED"
TIME_DELTA=12

def main():
    SQL.initialize_db()

    logging.info("Starting Reports Bot ...")
    # Create schwab client
    client = bot.Schwab_client(
                bot.util.get_secret("SCHWAB_APP_KEY", "config/.env"),
                bot.util.get_secret("SCHWAB_APP_SECRET", "config/.env")
            )
    print("Schwab client initialized")
    # Create gsheet client
    gclient = gsheet.connect_gsheets_account(util.get_secret("GSHEETS_CREDENTIALS", "config/.env"))
    worksheet = gsheet.connect_to_sheet(gclient, util.get_secret("GSHEETS_SHEET_ID", "config/.env"), util.get_secret("GSHEETS_PAGE_NAME", "config/.env"))
    # loop

    # check time to run
    # if not time to run, sleep for 5 minutes and jump to loop

    # Create new header row for this date
    header_location = gsheet.get_next_empty_row(worksheet, 2)
    gsheet.copy_headers(worksheet, header_location)

    # get Schwab data
    response = client.get_account_positions(FILTER, TIME_DELTA)
    print("Schwab data retrieved")
    # store and process Schwab data
    data.store_orders(response)
    unposted_orders = data.get_unposted_orders()
    # update gsheet with Schwab data
    for order in response:
        row_data = gsheet.format_data(order)
        gsheet.write_row_at_next_empty_row(worksheet, row_data)
        #data.mark_as_posted(order[0])

    # jump to loop

if __name__ == "__main__":
    main()