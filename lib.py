import configparser
from sqlalchemy import create_engine
import pandas as pd
import logging

config = configparser.ConfigParser()
config.read('config.ini')

logger = logging.getLogger(__name__)


class DatabaseIO:
    series = ['triggers']

    def __init__(self):
        db_config = config['RDS']
        url = db_config['url']
        db = db_config['db']
        username = db_config['username']
        password = db_config['password']
        self.engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{url}/{db}")

    def write_data(self, df, table):
        logger.info(f'Writing to {table}...')
        copy = df.copy()
        if table in self.series:
            copy = copy.reset_index()
        copy.to_sql(table, self.engine, if_exists='replace', chunksize=1000, index=False)
        logger.info('Done.')

    def read_data(self, table, parse_dates=False):
        logger.info(f'Reading data from {table}...')
        res = pd.read_sql(table, self.engine, parse_dates=parse_dates)
        if table in self.series:
            # set first column as index
            res = res.set_index(list(res)[0])
        logger.info('Done.')
        return res
