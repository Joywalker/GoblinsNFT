"""
    Script for updating fields in metadata json
"""

import json
from glob import glob

KEY_VALUE = "<ipfshome>"
TARGET_VALUE = "QmNniGAnSogNhdVbdw9pcf8X1shHc6Wt8ckjtT18NekbCF"

metadata_jsons = glob("../Marvel/metadata/*.json")
for json_f in metadata_jsons:
    with open(json_f, 'r') as f:
        data = json.load(f)
        data['image'] = data['image'].replace(KEY_VALUE, TARGET_VALUE)

    with open(json_f, 'w') as f:
        json.dump(data, f, indent=4)