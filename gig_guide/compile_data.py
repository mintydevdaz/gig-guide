from datetime import date, timedelta

import pandas as pd
from century import century
from moshtix import moshtix
from phoenix import phoenix
from pretty_html_table import build_table
from soh import sydney_opera_house


def master_file():
    """Create master CSV file. Store DataFrame in memory."""
    df = master_df()
    write_csv(df, filename="master")
    return df


def email_file(df: pd.DataFrame):
    """Create the email attachment as aCSV file"""
    small_table = thirty_days_table(df)
    rm_col = remove_col(small_table)
    write_csv(rm_col, filename="email")


def body_table() -> str:
    """Create pretty_html_table for Master CSV file"""
    df = pd.read_csv("/Users/darrenchung/Desktop/gigs_email.csv")
    return build_table(
        df,
        "blue_dark",
        font_family="Open Sans, sans-serif",
        text_align="left",
        width="auto",
    )


def master_df() -> pd.DataFrame:
    """Compiles all gig data into pd.DataFrames"""
    df1 = moshtix()
    df2 = sydney_opera_house()
    # df3 = phoenix()
    # df4 = century()
    main_df = pd.concat([df1, df2])
    # main_df = pd.concat([df1, df2, df3, df4])
    main_df.sort_values(by="DT", inplace=True)
    return main_df


def thirty_days_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare table for conversion into pretty_html_table.
    Shows gigs within a 30-day timeframe from today.
    Alse removes the 'DT' column (first column).
    """
    start_date = date.today()
    end_date = start_date + timedelta(days=30)
    mask = (df["DT"] > start_date) & (df["DT"] <= end_date)
    return df.loc[mask]


def write_csv(df: pd.DataFrame, filename: str):
    """Writes DataFrame to CSV"""
    f = f"/Users/darrenchung/Desktop/gigs_{filename}.csv"
    print(f"Saved CSV -> {f}")
    return df.to_csv(f, index=False)


def remove_col(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop("DT", axis="columns")
