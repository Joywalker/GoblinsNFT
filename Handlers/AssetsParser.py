"""
    Class describing an NFT image.
"""
import os
import json
import numpy as np
from utils import ORDER
from typing import List
from collections import Counter
import matplotlib.pyplot as plt

__all__ = ['AssetsParser']


class AssetsParser:
    def __init__(self, assets_json: str):
        assert os.path.isfile(assets_json)
        json_file = open(assets_json, 'r')
        self.json_contents = json.load(json_file)
        self.assets_params = self.__get_assets_params()

    def __get_assets_params(self):
        """Iterate json and save category, asset_id, weight, description"""
        formatted_json = {asset_category: {} for asset_category in ORDER}
        for key in self.json_contents["variables_metadata"].keys():
            for asset in self.json_contents["variables_metadata"][key]["assets"]:
                if asset["do_select"] == "True":
                    formatted_json[key][asset['id']] = asset

            # Re-distribute assets weights
            formatted_json[key] = self.__check_weights_distribution(formatted_json[key])
        return formatted_json

    @staticmethod
    def __check_weights_distribution(assets_list: dict):
        weights = [assets_list[v]['weight'] for v in assets_list.keys()]
        total_prob = np.sum(weights)

        diff = abs(100 - total_prob)
        threshold = diff / len(weights)

        if total_prob < 100:
            weights = [w + threshold for w in weights]
        elif total_prob > 100:
            weights = [w - threshold for w in weights]

        # Repopulate weights
        for weight, k in zip(weights, assets_list.keys()):
            assets_list[k]['weight'] = weight

        return assets_list

    def get_meta_for_nft(self, nft_id_string: str):
        assets_ids = nft_id_string.split('_')
        final_dict = {}
        for categ, asset_id in zip(ORDER, assets_ids):
            final_dict[categ] = self.get_asset_meta((categ, asset_id))

        return final_dict

    def get_asset_id_weights(self, categ_name: str):
        assets = self.assets_params[categ_name]
        assets_ids = [assets[k]["id"] for k in assets.keys()]
        assets_weights = [assets[k]["weight"] for k in assets.keys()]
        return assets_ids, assets_weights

    def test_rarities(self, assets_set: set):
        # Prepare plots and axes
        n_plots = len(ORDER)
        fig, axs = plt.subplots(n_plots)

        # Combine all the operations and display
        splitted_by_categ = [np.asarray(asset.split("_")) for asset in assets_set]
        [stacked] = np.dstack([categ_set for categ_set in splitted_by_categ])

        # Generate plots and display
        for i, (categ, stacked_set) in enumerate(zip(ORDER, stacked)):
            frequency = Counter(stacked_set.tolist())
            x_vals = [self.get_asset_attr(categ, k, "desc") for k in frequency.keys()]
            y_vals = [frequency[k] for k in frequency.keys()]
            bar_colors = [self.get_asset_group_color(categ, k) for k in frequency.keys()]

            axs[i].bar(x_vals, y_vals, color=bar_colors)
            axs[i].set_ylabel(categ)
            axs[i].set_xticks([x for x, _ in enumerate(x_vals)], x_vals)
            axs[i].set_xlabel("Occurences")
            axs[i].set_title("{} Selection Map".format(categ))

        plt.subplots_adjust(left=0.05,
                            bottom=0.05,
                            right=0.99,
                            top=0.9,
                            wspace=0.05,
                            hspace=0.9)
        plt.show()

    def get_asset_group_color(self, categ: str, asset_id : str):
        rank = self.assets_params[categ][asset_id]["category"]
        if rank == "Epic":
            return 'r'  # red
        elif rank == "Common":
            return 'g'  # green
        else:
            return 'b'  # blue

    def get_asset_attr(self, categ: str, id: str, attr: str):
        return self.assets_params[categ][id][attr]

    def get_asset_meta(self, asset_ids: tuple):
        """Gets pair category idx, asset idx"""
        asset_categ, asset_id = asset_ids
        final_res = self.assets_params[asset_categ][asset_id]
        print(asset_categ + " " + asset_id)
        return final_res

