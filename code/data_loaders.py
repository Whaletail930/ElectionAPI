import pandas as pd
import psycopg2

from logger_config import logger


# noinspection SqlNoDataSourceInspection,SqlDialectInspection
def ingest_data_to_df() -> pd.DataFrame:
    cursor = ""
    logger.info('Establishing database connection')
    try:
        connection = psycopg2.connect(database="electionresultsdb",
                                      user='postgres',
                                      password='postgres',
                                      host="localhost",
                                      port=5488)

        cursor = connection.cursor()

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
    logger.info('Connection successful')

    logger.info('Fetching data from DB')
    try:
        sql_context = """select 
                            district,
                            number_votes,
                            share_votes,
                            affiliation,
                            year
                        from 
                            public.electionresults"""

        cursor.execute(sql_context)

        logger.info('Data fetched successfully')

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")

    df = pd.DataFrame(cursor.fetchall(), columns=['district', 'number_votes', 'share_votes', 'affiliation', 'year'])

    max_share_votes_per_district_year = df.groupby(['year', 'district'])['share_votes'].transform(max)

    result_df = df[df['share_votes'] == max_share_votes_per_district_year]

    result_df = result_df.reset_index(drop=True)

    logger.info('Test dataset created successfully')

    return result_df


def get_number_votes() -> dict:
    df = ingest_data_to_df()

    average_votes_per_district = df.groupby('district')['number_votes'].mean()

    average_votes_dict = average_votes_per_district.astype(int).to_dict()

    return average_votes_dict
