"""
    Class describing an NFT image.
"""

import os
import json
from PIL import Image
from utils import ORDER, RESOLUTION

__all__ = ['NFTObject']

dir_path = os.path.join(os.path.dirname(__file__))


class NFTObject:
    def __init__(self, descrb_name: str, meta_dict: dict):
        self.asset_name = descrb_name.replace('_', '')
        self.image_name = self.asset_name + '.png'
        self.meta_name = self.asset_name + '.json'
        self.assets_ids = descrb_name.split('_')
        self.metadata = meta_dict

    def compose_and_save(self):
        baseline = Image.new('RGBA', size=RESOLUTION["8K"])
        for asset_id, asset_class in zip(self.assets_ids, ORDER):
            image_path = os.path.join(dir_path, "../assets", asset_class, "{}.png".format(asset_id))
            image_rgba = Image.open(image_path).convert('RGBA').resize(RESOLUTION["8K"])
            baseline = Image.alpha_composite(baseline, image_rgba)

        baseline.save(self.image_name)

    def generate_metadata(self):
        metadata = {
            "Collection Name": "The Bounty Goblins",
            "Edition": "Marvel Drop",
            "Name": "DEMO",
            "token_id": self.asset_name,
            "attributes": []
        }
        for asset_id, asset_class in zip(self.assets_ids, ORDER):
            trait_details = self.metadata[asset_class]
            metadata['attributes'].append({
                'trait_type': asset_class,
                'trait_value': trait_details['desc'],
                'trait_category': trait_details['category'],
                "universe": trait_details['universe']
            })

        with open(self.meta_name, 'w') as fin:
            json.dump(metadata, fin)
