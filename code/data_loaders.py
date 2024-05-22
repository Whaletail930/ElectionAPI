from pathlib import Path

import pandas as pd
import psycopg2

from logger_config import logger

# Eventually, data will come from a db

DATA = Path(r"C:\Users\belle\PycharmProjects\GDEIntAlk\DATA")


def twenty_two_csv_to_df(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df.drop(df.columns[0], axis=1)
    df['year'] = 2022
    df['district'] = df['district'].str.extract(r' - (.*)')

    idx = df.groupby('district')['share_votes'].idxmax()
    df = df.loc[idx]

    return df


def eighteen_csv_to_df(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path, engine='python', encoding="utf-8")
    df['year'] = 2018
    df['share_votes'] = df['share_votes'].str.rstrip('%').astype(float)

    idx = df.groupby('district')['share_votes'].idxmax()
    df = df.loc[idx]

    return df


def fourteen_csv_to_df(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path, engine='python', encoding="utf-8")
    df['year'] = 2014

    idx = df.groupby('district')['share_votes'].idxmax()
    df = df.loc[idx]

    return df


def concat_dfs(csv_2014_filename: str, csv_2018_filename: str, csv_2022_filename: str) -> pd.DataFrame or None:
    logger.info("Reading data")
    try:
        df2014 = fourteen_csv_to_df(DATA / csv_2014_filename)
        df2018 = eighteen_csv_to_df(DATA / csv_2018_filename)
        df2022 = twenty_two_csv_to_df(DATA / csv_2022_filename)

        df2022 = df2022.replace('Fidesz/KDNP', 'FIDESZ-KDNP')
        df2014 = df2014.replace('SZEM-NŐPÁRT', 'SZEM PÁRT')
        df2014 = df2014.replace('EU. ROM', 'EU.ROM')

        final_columns = ['name', 'district', 'number_votes', 'share_votes', 'affiliation', 'year']

        df2014 = df2014[final_columns]
        df2018 = df2018[final_columns]
        df2022 = df2022[final_columns]

        full_df = pd.concat([df2014, df2018, df2022], ignore_index=True)

        full_df = full_df.reset_index(drop=True)

        full_df = full_df.drop(columns=['name'])

        logger.info("Dataset created")
        return full_df

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        return None


# noinspection SqlNoDataSourceInspection,SqlDialectInspection
def ingest_data_to_df() -> pd.DataFrame:
    connection = psycopg2.connect(database="electionresultsdb",
                                  user='postgres',
                                  password='postgres',
                                  host="localhost",
                                  port=5488)

    cursor = connection.cursor()

    sql_context = """select 
                        district,
                        number_votes,
                        share_votes,
                        affiliation,
                        year
                    from 
                        public.electionresults"""

    cursor.execute(sql_context)

    df = pd.DataFrame(cursor.fetchall(), columns=['district', 'number_votes', 'share_votes', 'affiliation', 'year'])

    return df


def get_number_votes():
    pass


if __name__ == '__main__':
    logger.info("Reading data")
    """combined_df = concat_dfs("hungarian_election2014.csv",
                             "hungarian_election2018.csv",
                             "hungarian_election2022.csv")"""
    ingest_data_to_df()
    logger.info("Dataset created")


