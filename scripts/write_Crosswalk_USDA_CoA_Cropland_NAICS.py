# write_Crosswalk_USDA_CoA_Cropland_NAICS.py (scripts)
# !/usr/bin/env python3
# coding=utf-8

"""
Create a crosswalk for CoA Cropland Naics to NAICS 2012. Downloaded data is already provided in NAICS
"""
import pandas as pd
from flowsa.common import datapath, fbaoutputpath

def unique_activity_names(datasource, years):
    """read in the ers parquet files, select the unique activity names"""
    df = []
    for y in years:
        df = pd.read_parquet(fbaoutputpath + datasource + "_" + str(y) + ".parquet", engine="pyarrow")
        df.append(df)
    df = df[['SourceName', 'ActivityConsumedBy']]
    # rename columns
    df = df.rename(columns={"SourceName": "ActivitySourceName",
                            "ActivityConsumedBy": "Activity"})
    df = df.drop_duplicates()
    return df


if __name__ == '__main__':
    # select years to pull unique activity names
    years = ['2012', '2017']
    # df of unique ers activity names
    df = unique_activity_names('USDA_CoA_Cropland_NAICS', years)
    # drop activities with symbol '&'
    df = df[~df['Activity'].str.contains('&')]
    # Activity and Sector are the same
    df['Sector'] = df['Activity'].copy()
    # Add additional columns
    df['SectorSourceName'] = "NAICS_2012_Code"
    df['SectorType'] = None
    # reorder
    df = df[['ActivitySourceName', 'Activity', 'SectorSourceName', 'Sector', 'SectorType']]
    # sort df
    df = df.sort_values(['Activity', 'Sector'])
    # reset index
    df.reset_index(drop=True, inplace=True)
    # save as csv
    df.to_csv(datapath + "activitytosectormapping/" + "Crosswalk_USDA_CoA_Cropland_NAICS_toNAICS.csv", index=False)
