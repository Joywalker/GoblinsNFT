import os
import numpy as np

from NFTObject import NFTObject
from utils import ORDER
from numpy.random import choice
from AssetsParser import AssetsParser

dir_path = os.path.join(os.path.dirname(__file__))

NUMBER = 100
asset_combinations = set()

parser = AssetsParser(os.path.join(dir_path, "assets", "assets_selection.json"))

while len(asset_combinations) <= NUMBER:
    asset_ids = []
    for k in ORDER:
        ids, weights = parser.get_asset_id_weights(k)
        [selection] = choice(ids, 1, p=np.asarray(weights) / 100)
        asset_ids.append(selection)
    asset_code = "_".join(asset_ids)
    asset_combinations.add(asset_code)

parser.test_rarities(asset_combinations)
# Generate NFT's
for item in asset_combinations:
    # Asset json
    asset_metadata = parser.get_meta_for_nft(item)
    nft_obj = NFTObject(descrb_name=item, meta_dict=asset_metadata)
    nft_obj.compose_and_save()
    nft_obj.generate_metadata()
    print('Saved {}'.format(item))