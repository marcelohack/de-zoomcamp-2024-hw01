#!/usr/bin/env python

import os
import argparse
import tempfile

from time import time
import pandas as pd
from sqlalchemy import create_engine


yellow_taxi_dtypes = {
    'VendorID': pd.Int64Dtype(),
    'passenger_count': pd.Int64Dtype(),
    'trip_distance': float,
    'RatecodeID': pd.Int64Dtype(),
    'store_and_fwd_flag': str,
    'PULocationID': pd.Int64Dtype(),
    'DOLocationID': pd.Int64Dtype(),
    'payment_type': pd.Int64Dtype(),
    'fare_amount': float,
    'extra': float,
    'mta_tax': float,
    'tip_amount': float,
    'tolls_amount': float,
    'improvement_surcharge': float,
    'total_amount': float,
    'congestion_surcharge': float
}

green_taxy_dtypes = {
    'VendorID': pd.Int64Dtype(),
    'RatecodeID': pd.Int64Dtype(),
    'store_and_fwd_flag': str,
    'PULocationID': pd.Int64Dtype(),
    'DOLocationID': pd.Int64Dtype(),
    'passenger_count': pd.Int64Dtype(),        
    'trip_distance': float,
    'fare_amount': float,
    'extra': float,
    'mta_tax': float,
    'tip_amount': float,
    'tolls_amount': float,
    'ehail_fee': float,
    'improvement_surcharge': float,
    'total_amount': float,
    'payment_type': pd.Int64Dtype(),
    'trip_type': pd.Int64Dtype(),
    'congestion_surcharge': float
}

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    table_suffix = params.table_suffix
    csv_file = params.csv

    taxi_color = 'yellow' if 'yellow' in csv_file else 'green' if 'green' in csv_file else 'yellow'

    if table_suffix == '' or table_suffix is None:
        table_suffix = 'taxi_trips'

    if table_name == '' or table_name is None:
        table_name = f'{taxi_color}_{table_suffix}'
    

    if csv_file.startswith('http'):
        # if it is a url, download it to a temp directory
        print(f'Downloading {csv_file} ...')
        temp_dir = tempfile.mkdtemp()
        file_name = os.path.basename(csv_file)
        csv_file = os.path.join(temp_dir, file_name)
        os.system(f'wget {params.csv} -O {csv_file}')

    print(f'Processing {csv_file} ...')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    if taxi_color == 'yellow':
        dtype = yellow_taxi_dtypes
    elif taxi_color == 'green':
        dtype = green_taxy_dtypes
    else:
        dtype = None

    df_iter = pd.read_csv(csv_file, iterator=True, dtype=dtype, chunksize=100000)
    df = next(df_iter)

    adjust_dataframe(df, taxi_color)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        t_start = time()
        df = next(df_iter)
        adjust_dataframe(df, taxi_color)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print('inserted another chunk... took %.3f second' % (t_end - t_start))

def adjust_dataframe(df, taxi_color = 'yellow'):
    # Convert datetime text columns to datetime objects
    if taxi_color == 'yellow':
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    elif taxi_color == 'green':
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='hostname for postgres')
    parser.add_argument('--port', help='port number for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to - default is taxi_color + table_suffix, i.e. yellow_taxi_trips')
    parser.add_argument('--table_suffix', help='suffix to append to table name - default is taxi_trips')
    parser.add_argument('--csv', help='the location of the csv file')

    args = parser.parse_args()
    main(args)

        
        

