#!/usr/bin/env python

import os
import argparse
import tempfile

from time import time
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    csv_file = params.csv

    if table_name == '':
        table_name = '_taxi_trips'

    if csv_file.startswith('http'):
        # if it is a url, download it to a temp directory
        print(f'Downloading {csv_file} ...')
        temp_dir = tempfile.mkdtemp()
        file_name = os.path.basename(csv_file)
        csv_file = os.path.join(temp_dir, file_name)
        os.system(f'wget {params.csv} -O {csv_file}')

    print(f'Processing {csv_file} ...')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_file, iterator=True, chunksize=100000)
    df = next(df_iter)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        t_start = time()
        df = next(df_iter)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print('inserted another chunk... took %.3f second' % (t_end - t_start))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV zones to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='hostname for postgres')
    parser.add_argument('--port', help='port number for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--csv', help='the location of the zones csv file')

    args = parser.parse_args()
    main(args)

        
        

