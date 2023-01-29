from century import century
from moshtix import moshtix
from phoenix import phoenix
from soh import sydney_opera_house

import pandas as pd


def compile_tables() -> pd.DataFrame:
    """
    Compiles all gig data into pd.DataFrames
    """

    # Get DataFrames
    df1 = moshtix()
    df2 = sydney_opera_house()
    # df3 = phoenix()
    # df4 = century()

    # Combine DataFrames
    main_df = pd.concat([df1, df2])
    # main_df = pd.concat([df1, df2, df3, df4])

    # Sort values (in place)
    main_df.sort_values(by="DT", inplace=True)
    return main_df


if __name__ == "__main__":
    compile_tables()
