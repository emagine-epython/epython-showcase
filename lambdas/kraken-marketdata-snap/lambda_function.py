import requests
import boto3
from datetime import datetime
from decimal import Decimal

URL = 'https://api.kraken.com/0/public/Ticker?'
'pair=XBTGBP,XBTEUR,XBTUSD,ETHXBT,XMRXBT,XBTUSDT,LTCXBT'
DB_NAME = 'epython-marketdata'
EXCHANGE = 'KRAKEN'


def lambda_handler(event, context):

    r = requests.get(URL)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DB_NAME)
    res = r.json()

    for key, item in res['result'].items():
        item['symbol'] = EXCHANGE + '_' + key
        item['timestamp'] = Decimal(
            '%.2f' % datetime.timestamp(datetime.now()))
        print(f'Inserting: {item}')

        table.put_item(Item=item)
