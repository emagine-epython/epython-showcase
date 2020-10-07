import click
import urllib.request
import s3fs

REMOTE_BASEDIR = 'epython-marketdata/fxcm/'
URL_TEMPLATE = 'https://candledata.fxcorporate.com/m1/{pair}' \
               '/{year}/{week}.csv.gz'


def _weekly_key(year: int, week: int, pair: str) -> str:
    return f'year={year}/week={week}/pair={pair}'


def snap_pair(year, week, pair):
    print(f"Snapping year: {year}, week: {week}, pair: {pair}")
    url = URL_TEMPLATE.format(year=year, week=week, pair=pair)

    print(f"Reading data from {url}")
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    key = _weekly_key(year, week, pair)
    response = urllib.request.urlopen(req)
    s3_path = f'{REMOTE_BASEDIR}{key}/{pair}.gz'
    print(f'Writing to s3://{s3_path}')
    fs = s3fs.S3FileSystem()
    with fs.open(s3_path, 'wb') as f:
        f.write(response.read())


@click.command()
@click.option('--years', required=True, type=str,
              help='comma separated list of years')
@click.option('--pairs', required=True,
              type=str, help='comma separated list of pairs')
def download(years, pairs):
    for year in years.split(','):
        year = int(year)
        for pair in pairs.split(','):
            for week in range(1, 53):
                try:
                    snap_pair(year, week, pair)
                except Exception as exp:
                    print("Error: {}".format(exp))


# Exmaple: python epython/marketdata/utils/fxcm.py \
#    --years=2014,2015,2016,2017,2018 \
#    --pairs=EURUSD,GBPUSD,NZDUSD,USDCAD,USDCHF,USDJPY
if __name__ == '__main__':
    download()
