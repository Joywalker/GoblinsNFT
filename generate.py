import json
import os
import numpy as np

from Handlers.NFTObject import NFTObject
from utils import ORDER
from numpy.random import choice
from Handlers.AssetsParser import AssetsParser

# Set path
dir_path = os.path.join(os.path.dirname(__file__))

# Load config and parse parameters
config_json = json.load(open("config.json", 'r'))

# Setup paths
imgs_path = os.path.join(dir_path, config_json["paths"]['collection'], config_json["paths"]['images'])
json_path = os.path.join(dir_path, config_json["paths"]['collection'], config_json["paths"]['metadata'])

if not os.path.exists(imgs_path):
    os.makedirs(imgs_path)
if not os.path.exists(json_path):
    os.makedirs(json_path)

# Get generation config
nft_config = config_json["assets_config"]

asset_combinations = set()
parser = AssetsParser(os.path.join(dir_path, "assets", "assets_selection.json"), config_json=nft_config)

while len(asset_combinations) <= config_json["general"]['count']:
    asset_ids = []
    for k in ORDER:
        ids, weights = parser.get_asset_id_weights(k)
        [selection] = choice(a=ids, size=1, p=np.asarray(weights) / 100)
        asset_ids.append(selection)
    asset_code = "_".join(asset_ids)
    asset_combinations.add(asset_code)

# parser.test_rarities(asset_combinations)
# Generate NFT's
for idx, item in enumerate(asset_combinations):
    # Asset json
    asset_metadata = parser.get_meta_for_nft(item)
    nft_obj = NFTObject(descrb_name=item, meta_dict=asset_metadata,
                        config_json={"imgs": imgs_path, "json": json_path, "settings": nft_config},
                        idx=idx)
    nft_obj.compose_and_save()
    nft_obj.generate_metadata()
    print('Saved {}'.format(item))