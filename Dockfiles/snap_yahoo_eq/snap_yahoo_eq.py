import boto3
import os
from datetime import datetime
from decimal import Decimal
from playwright import sync_playwright

DB_NAME = 'epython-marketdata'
NUM_STOCKS = os.environ.get('NUM_STOCKS', '25')
DRY_RUN = os.environ.get('DRY_RUN', 'FALSE') == 'TRUE'

if __name__ == '__main__':

    if not DRY_RUN:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(DB_NAME)

    with sync_playwright() as p:
        browser_type = p.chromium
        browser = browser_type.launch()
        page = browser.newPage()
        page.goto(
            'https://uk.finance.yahoo.com/most-active?'
            f'offset=0&count={NUM_STOCKS}')
        page.querySelector('.consent-form button').click()
        page.waitForSelector('#fin-scr-res-table')
        rows = page.querySelectorAll('#fin-scr-res-table tbody tr')

        for row in rows:
            cells = row.querySelectorAll('td')
            symbol = cells[0].querySelector('a').textContent()
            symbol = 'YAHOO_EQ_' + symbol
            price = cells[2].querySelector('span').textContent()
            item = {
                'symbol': symbol,
                'timestamp': Decimal('%.2f' %
                                     datetime.timestamp(datetime.now())),
                'price': price
            }
            print(f'Inserting {item}')

            if not DRY_RUN:
                table.put_item(Item=item)

        browser.close()
