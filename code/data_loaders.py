from pathlib import Path

import pandas as pd

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

        # full_df.to_csv(DATA / 'hu_election_2014_2022.csv')

        full_df = full_df.drop(columns=['name'])

        logger.info("Dataset created")
        return full_df

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        return None


if __name__ == '__main__':
    logger.info("Reading data")
    combined_df = concat_dfs("hungarian_election2014.csv",
                             "hungarian_election2018.csv",
                             "hungarian_election2022.csv")
    logger.info("Dataset created")


