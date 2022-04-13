"""
    Script for updating fields in metadata json.
    Date: 11.04.2022
    Author: Joywalker
"""

# Imports
import os
import json
import argparse
from glob import glob

# Setup arguments
parser = argparse.ArgumentParser(description='Count asset rarities.')
parser.add_argument('--config', type=str, default="update_config.json", help='Path to generated dataset.')
args = parser.parse_args()

# Load config
with open(args.config, 'r') as f:
    config_data = json.load(f)


# Define additional methods
def perform_action(action_type: str, item: str, source_v: str, target_v: str) -> str:
    if action_type == 'replace':
        item = item.replace(source_v, target_v)

    return item


# Execute config
for k in config_data.keys():
    if config_data[k]['active']:
        # Prepare files
        coll_path = config_data[k]['collection_path']
        if k.lower() == 'metadata':
            files = glob(os.path.join(coll_path, os.sep, k) + "*.json")
            for file in files:
                with open(file, 'r') as f:
                    data = json.load(f)
                    for action in config_data[k]['actions']:
                        act_topic = action['topic']
                        act_type = action['type']
                        source = action['source']
                        target = action['target']
                        data[act_topic] = perform_action(act_type, data[act_topic], source, target)
                with open(file, 'w') as f:
                    json.dump(data, f, indent=4)