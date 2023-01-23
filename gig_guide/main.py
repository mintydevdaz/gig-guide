from datetime import datetime

import pandas as pd
from century import century
from moshtix import moshtix
from phoenix import phoenix
from soh import sydney_opera_house


def main():
    df1 = moshtix()
    df2 = phoenix()
    df3 = sydney_opera_house()
    df4 = century()

    # Combine DataFrames
    res = pd.concat([df1, df2, df3, df4])

    # Sort by datetime column then remove it
    res.sort_values(by="DT", inplace=True)
    final_table = res.drop("DT", axis="columns")

    write_csv(final_table)


def write_csv(df):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    filepath = f"/Users/darrenchung/Desktop/gigs_{dt_string}.csv"
    print(f"CSV file saved at {filepath}")
    return df.to_csv(filepath, index=False)


if __name__ == "__main__":
    main()
