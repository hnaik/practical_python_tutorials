#!/usr/bin/env python3
import pandas as pd
import numpy as np
from argparse import ArgumentParser


def parse_args():
    '''
    Input arguments needed to execute tool.
    '''
    parser = ArgumentParser()
    parser.add_argument('--csvfile', required=True, help='first csv file')

    return parser.parse_args()


options = parse_args()
input_file = options.csvfile
print(input_file)
output_file = "output.csv"


df = pd.read_csv(input_file)
print(df)
df.columns = df.columns.str.strip()
df[['lat_x', 'lon_x', 'lat_y', 'lon_y']] = df[
    ['lat_x', 'lon_x', 'lat_y', 'lon_y']
].astype(float)


def dist_from_coordinates(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    # conversion to radians
    d_lat = np.radians(lat2 - lat1)
    d_lon = np.radians(lon2 - lon1)

    r_lat1 = np.radians(lat1)
    r_lat2 = np.radians(lat2)

    # haversine formula
    a = (
        np.sin(d_lat / 2.0) ** 2
        + np.cos(r_lat1) * np.cos(r_lat2) * np.sin(d_lon / 2.0) ** 2
    )

    haversine = (2 * R * np.arcsin(np.sqrt(a))) * 1000

    return haversine


new_column = []  # empty column for distance
for index, row in df.iterrows():
    lat1 = row['lat_x']  # first row of location.lat column here
    lon1 = row['lon_x']  # first row of location.long column here
    lat2 = row['lat_y']  # second row of location.lat column here
    lon2 = row['lon_y']  # second row of location.long column here
    value = dist_from_coordinates(lat1, lon1, lat2, lon2)  # get the distance
    new_column.append(value)  # append the empty list with distance values

df.insert(
    5, "distance_meters", new_column
)  # 4 is the index where you want to place your column. Column index starts with 0. "Distance" is the header and new_column are the values in the column.

with open(output_file, 'w') as f:
    df.to_csv(f, index=False)  # creates the output.csv


if __name__ == '__main__':
    dist_from_coordinates(lat1, lon1, lat2, lon2)
