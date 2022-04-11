"""
    Rarity checker takes care of iterating all over the generated metadata and counts the appearances of each asset
    in order to count and establish rarity percentages.

    Date: 11.04.2022
    Author: Razvant Alexandru
"""

# Define imports
import json
import os
import argparse
from glob import glob

# Setup argument parser
parser = argparse.ArgumentParser(description='Count asset rarities.')
parser.add_argument('--metadata_path', type=str, help='Path to generated dataset.')
parser.add_argument('--save', type=bool, help='Boolean flag to save results into a json file.')
args = parser.parse_args()


# Setup additional methods
def mark_occurence(rarity_data: dict, k: str, v: str) -> None:
    if k not in rarity_data['status']:
        rarity_data['status'][k] = {}

    if v not in rarity_data['status'][k]:
        rarity_data['status'][k][v] = 1
    else:
        rarity_data['status'][k][v] += 1


# Start loop
metadata_files = glob(args.metadata_path + os.sep + "*.json")
rarity_dict = {
    "count": len(metadata_files),
    "status": {}
}
for m_file in metadata_files:
    with open(m_file, 'r') as fin:
        m_data = json.load(fin)
        # Iterate through each asset
        for attr in m_data['attributes']:
            mark_occurence(rarity_dict, attr['trait_type'], attr['trait_value'])
