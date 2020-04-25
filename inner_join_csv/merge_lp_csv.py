#!/usr/bin/env python3

import csv
import pandas as pd
import numpy as np
from argparse import ArgumentParser
import pandas, sys

import distance_diff

def parse_args():
    '''
    Input arguments needed to execute tool.
    '''
    parser = ArgumentParser()
    parser.add_argument('--csv-one', required=True, help='first csv file')
    parser.add_argument('--csv-two', required=True, help='second csv file')
    parser.add_argument('--output-csv-path', required=True)

    return parser.parse_args()

# struct Record {
#     int id;
#     float lat;
#     float 
# };

# struct Record **tables =
# fd = open('/path', 'r')

# def foo(file_path):
#     records = []
#     with open(file_path, 'r') as f:
#         for idx, row in enumerate(f):
#             if idx == 0:
#                 continue
#             line = row.rstrip()
#             parts = line.split(',')
#             # record = dict(ident=int(parts[0]),
#             #               lat=float(parts[1]), lon=float(parts[2]))
#             record = {
#                 'id': int(parts[0]),
#                 'lat': float(parts[1]),
#                 'lon': float(parts[2])
#             }
#             records.append(record)
#     return records

# def dist_from_coordinates(lat1, lon1, lat2, lon2):
#     R = 6371  # Earth radius in km

#     # conversion to radians
#     d_lat = np.radians(lat2 - lat1)
#     d_lon = np.radians(lon2 - lon1)

#     r_lat1 = np.radians(lat1)
#     r_lat2 = np.radians(lat2)

#     # haversine formula
#     a = (
#         np.sin(d_lat / 2.0) ** 2
#         + np.cos(r_lat1) * np.cos(r_lat2) * np.sin(d_lon / 2.0) ** 2
#     )

#     haversine = (2 * R * np.arcsin(np.sqrt(a))) * 1000

#     return haversine


def extract_records(file_path):
    with open(file_path) as f:
        reader = csv.DictReader(f)

        return [row for row in reader]

    
def merge_records(table_1, table_2):
    merged_table = {}

    for row in table_1:
        record = {
            'lat_1': float(row['lat']),
            'lon_1': float(row['lon']),
            'lat_2': None,
            'lon_2': None,
            'distance_sq_m': 0
        }

        merged_table.update({row['id']: record})

    for row in table_2:
        table_2_key = row['id']
        record = merged_table[table_2_key]
        record['lat_2'] = float(row['lat'])
        record['lon_2'] = float(row['lon'])

        record['distance_sq_m'] = distance_diff.dist_from_coordinates(
            record['lat_1'],
            record['lon_1'],
            record['lat_2'],
            record['lon_2']
        )
        

    return merged_table


def write_to_csv(merged_records, file_path):
    with open(file_path, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'id', 'lat_1', 'lon_1', 'lat_2', 'lon_2', 'distance'])

        table = []
        for key, value in merged_records.items():
            row = {
                'id': key,
                'lat_1': value['lat_1'],
                'lon_1': value['lon_1'],
                'lat_2': value['lat_2'],
                'lon_2': value['lon_2'],
                'distance': value['distance_sq_m']
            }

            table.append(row)

        writer.writeheader()
        writer.writerows(table)
        
    
def merge_csvfiles():
    options = parse_args()
    print(f'file 1: {options.csv_one}, file 2: {options.csv_two}')
    

    csv_one = extract_records(options.csv_one)
    csv_two = extract_records(options.csv_two)

    merged_records = merge_records(csv_one, csv_two)
    write_to_csv(merged_records, options.output_csv_path)
    
    # print(csv_one)
    # print(csv_two)

    # records = foo(options.csv_one)
    # records = extract_records(options.csv_one)
    # print(records)
    
    # records_1 = extract_records(options.csv_one)
    # for record in records_1:
    #     print(record)
        
    # csvone = pd.read_csv(options.csv_one)
    # csvtwo = pd.read_csv(options.csv_two)
    # merged = csvone.merge(csvtwo, on='id')

    # merged.to_csv('merged.csv', index=False)


if __name__ == '__main__':
    merge_csvfiles()
