import configparser
from sqlalchemy import create_engine
import pandas as pd
import logging
import ast

config = configparser.ConfigParser()
config.read('config.ini')

logger = logging.getLogger(__name__)


class DatabaseIO:
    list_cols = ['tags', 'dominant_color', 'posted_tags', 'last_color']
    bool_cols = ['accepted_static', 'accepted_ml', 'comments_disabled', 'is_private', 'is_verified', 'has_pf',
                 'is_business']
    date_cols = {
        'uploaded': ['uploaded_at', 'taken_at_datetime'],
        'users': ['followed_at', 'unfollowed_at'],
        'metadata': ['scraped_at'],
    }

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
        for col in copy.columns:
            if col in self.list_cols:
                copy[col] = copy[col].apply(str)
        copy.to_sql(table, self.engine, if_exists='replace', chunksize=1000, index=False)
        logger.info('Done.')

    def read_data(self, table, parse_dates=None):
        logger.info(f'Reading data from {table}...')
        if parse_dates is None:
            parse_dates = []
        parse_dates = list(set(parse_dates + self.date_cols.get(table, [])))
        if parse_dates == []:
            parse_dates = False
        res = pd.read_sql(table, self.engine, parse_dates=parse_dates)

        for col in res.columns:
            if col in self.bool_cols:
                res[col] = res[col].astype('bool')
            if col in self.list_cols:
                res[col] = res[col].apply(ast.literal_eval)
        logger.info('Done.')
        return res
