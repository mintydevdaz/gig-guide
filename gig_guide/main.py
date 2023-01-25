from datetime import date, datetime, timedelta

import pandas as pd
from century import century
from moshtix import moshtix
from phoenix import phoenix
from pretty_html_table import build_table
from soh import sydney_opera_house


def main():
    df1 = moshtix()
    df2 = sydney_opera_house()
    # df3 = phoenix()
    # df4 = century()

    # Combine DataFrames
    df = pd.concat([df1, df2])
    # df = pd.concat([df1, df2, df3, df4])

    # Sort by datetime column
    df.sort_values(by="DT", inplace=True)

    # Create HTML table
    html_table = email_table(mini_table(df))

    # Create CSV file on Desktop
    final_table = remove_col(df)
    csv_path = write_csv(final_table)

    # TODO - prepare emails to guest list
    # TODO - optimise phoenix.py


def write_csv(df: pd.DataFrame) -> str:
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    filepath = f"/Users/darrenchung/Desktop/gigs_{dt_string}.csv"
    df.to_csv(filepath, index=False)
    print(f"CSV file saved at {filepath}")
    return filepath


def mini_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare table for conversion in pretty_html_table.
    Shows gigs within a 30-day timeframe from today.
    Alse removes the 'DT' column (first column).
    """
    start_date = date.today()
    end_date = start_date + timedelta(days=30)
    mask = (df["DT"] > start_date) & (df["DT"] <= end_date)
    df2 = df.loc[mask]
    return remove_col(df2)


def email_table(table: pd.DataFrame) -> str:
    return build_table(
        table,
        "blue_dark",
        font_family="Open Sans, sans-serif",
        text_align="left",
        width="auto",
    )


def remove_col(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop("DT", axis="columns")


if __name__ == "__main__":
    main()
