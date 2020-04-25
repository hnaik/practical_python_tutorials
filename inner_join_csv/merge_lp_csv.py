#!/usr/bin/env python3

import csv
import numpy as np
import pandas as pd
import sys

from argparse import ArgumentParser


def compute_earth_distance(lat1, lon1, lat2, lon2):
    """Compute distance between two earth points
    
    This function computes distance between two points on the earth using the 
    Haversine formula
    :lat1: First latitude
    :lon1: First longitude
    :lat2: Second latitude
    :lon2: Second longitude
    :return: distance in meters
    """

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


def extract_records(file_path):
    """Function to extract records from CSV file

    :file_path: Path to the CSV file
    :return: extracted records as a list of dicts
    """

    with open(file_path) as f:
        reader = csv.DictReader(f)

        return [row for row in reader]


def merge_records(table_1, table_2):
    """Function to perform merge

    :table_1: Records from the first table
    :table_2: Records from the second table
    :return: merged_table
    """
    merged_table = {}

    for row in table_1:
        record = {
            'lat_1': float(row['lat']),
            'lon_1': float(row['lon']),
            'lat_2': None,
            'lon_2': None,
            'distance_sq_m': 0,
        }

        merged_table.update({row['id']: record})

    for row in table_2:
        table_2_key = row['id']
        record = merged_table[table_2_key]
        record['lat_2'] = float(row['lat'])
        record['lon_2'] = float(row['lon'])

        record['distance_sq_m'] = compute_earth_distance(
            record['lat_1'], record['lon_1'], record['lat_2'], record['lon_2']
        )

    return merged_table


def write_to_csv(merged_records, file_path):
    """Function to write merged records to a CSV file
  
    :merged_records: dictionary of merged records
    :file_path: Path to the output CSV file to be created
    """

    with open(file_path, 'w') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['id', 'lat_1', 'lon_1', 'lat_2', 'lon_2', 'distance'],
        )

        table = []
        for key, value in merged_records.items():
            row = {
                'id': key,
                'lat_1': value['lat_1'],
                'lon_1': value['lon_1'],
                'lat_2': value['lat_2'],
                'lon_2': value['lon_2'],
                'distance': value['distance_sq_m'],
            }

            table.append(row)

        writer.writeheader()
        writer.writerows(table)


def main():
    """Main Function"""

    csv_one = extract_records(args.csv_one)
    csv_two = extract_records(args.csv_two)
    merged_records = merge_records(csv_one, csv_two)
    write_to_csv(merged_records, args.output_csv_path)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--csv-one', required=True, help='first csv file')
    parser.add_argument('--csv-two', required=True, help='second csv file')
    parser.add_argument('--output-csv-path', required=True)
    args = parser.parse_args()

    main()
