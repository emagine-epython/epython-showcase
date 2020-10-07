import click
import s3fs
import subprocess
import pandas as pd
import os
import os.path

DST_REMOTE_BASEDIR = 'epython-marketdata/bitflyer/'
SRC_REMOTE_BASEDIR = 'angotsuka-notebook/market_data/bitflyer/monthly/'


@click.group()
def cli():
    pass


@cli.command()
@click.argument('dest',
                type=click.Path(exists=True, file_okay=False,
                                dir_okay=True))
def download(dest):
    """ Download BitFlyer marketdata from TAY Global Ltd to dest folder.
        Please contact to tony.yum@tayglobal.com for access
    """
    command = f'aws s3 sync s3://{SRC_REMOTE_BASEDIR} {dest}'
    print(command)
    subprocess.run(command, shell=True, check=True)


@cli.command()
@click.argument('src',
                type=click.Path(exists=True, file_okay=False,
                                dir_okay=True))
def upload(src):
    """Upload to epyton-marketdata from local src folder"""
    fs = s3fs.S3FileSystem()
    pair = 'FX_BTC_JPY'
    for month in os.listdir(src):
        path = os.path.join(src, month, pair + '.feather')
        df = pd.read_feather(path)
        s3_path = f'{DST_REMOTE_BASEDIR}pair={pair}/' \
            f'month={month}/{pair}.csv.gz'
        filename = f'/tmp/{pair}.csv.gz'
        df.to_csv(filename, compression='gzip', index=False)
        print(f'Writing to s3://{s3_path}')
        try:
            with open(filename, 'rb') as srcf:
                with fs.open(s3_path, 'wb') as dstf:
                    dstf.write(srcf.read())
        finally:
            os.remove(filename)


if __name__ == '__main__':
    cli()
