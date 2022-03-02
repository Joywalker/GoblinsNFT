import itertools
import os
import csv
import json
import random
import numpy as np
from glob import glob
from PIL import Image

##############################
# Load assets types count
##############################
assets_folder = "assets"
asset_types = {"meta": {}}
def_path = os.path.dirname(os.path.realpath(__file__))


def init_asset_counts():
    # Read json file and generate selected assets
    asset_selector_json_path = os.path.join(def_path, assets_folder, "assets_selection.json")
    with open(asset_selector_json_path) as json_f:
        data = json.load(json_f)
        # Add the rest of the keys
        for k in list(data.keys())[:-1]:
            asset_types["meta"][k] = data[k]
        for entry in data["variables_metadata"]:
            # 1 == True, 0 == False
            if data["variables_metadata"][entry]["selected"] == 1:
                if entry not in asset_types.keys():
                    asset_types[entry] = {}
                asset_types[entry]["sel"] = data["variables_metadata"][entry]["selected"]
                asset_types[entry]["can_export"] = data["variables_metadata"][entry]["can_export"]
                asset_types[entry]["assets"] = ["{}/{}".format(entry, el[0]) for el in data["variables_metadata"][entry]["assets"]]
                asset_types[entry]["desc"] = [el[1] for el in data["variables_metadata"][entry]["assets"]]
                asset_types[entry]["weights"] = [el[2] for el in data["variables_metadata"][entry]["assets"]]
                asset_types[entry]["no"] = len(asset_types[entry]["assets"])


def get_asset_count(asset_name):
    assert asset_name in asset_types.keys(), "Check if asset name corresponds"
    return asset_types[asset_name]["no"]


def get_asset_by_id(asset_class, id):
    assert asset_class in asset_types.keys(), "Check if asset name corresponds"
    if len(asset_types[asset_class]["assets"]) == 0:
        return None
    else:
        path_to_asset = os.path.join(def_path, assets_folder, asset_types[asset_class]["assets"][id-1])
        return Image.open(path_to_asset)


def get_assets_details():
    return asset_types


# Return total count of variables per category
def get_total_number_variables(cate_name):
    return len(asset_types[cate_name]["assets"])


# Probability computation
# Load csv file with assets probabilites
def load_assets_probabilities(no_of_samples):
    # Choose assets randomly based on their weights
    dict = {}
    for key in list(asset_types.keys())[1:]:
        # Parse asset category
        assets = [asset for asset in asset_types[key]["assets"]]
        weights = [prob for prob in asset_types[key]["weights"]]
        choices = random.choices(assets, weights=weights, k=no_of_samples)
        dict[key] = {
            "random_choices" : choices,
            "unused": [val for val in assets if val not in choices]
        }
    return dict


def has_all_assets(assets_pair):
    # Flags :   body, arms, face, skin, eyes, mouth, clothing, hat, neck| Total: 9
    bool_vec = [False for i in range(len(list(asset_types.keys())[1:]))]
    for entry in assets_pair:
        category = entry[0]
        try:
            idx = list(asset_types.keys())[1:].index(category)
            bool_vec[idx] = True
        except ValueError:
            print("Element {} is not valid")
    return True if all(bool_vec) else False


# Get the count of assets left in the lists
def get_available_variables_count(assets_dict):
    return np.max([len(assets_dict[val]["random_choices"]) for val in assets_dict.keys()])

def get_base_asset():
    for key in asset_types.keys():
        return asset_types[key]

def get_images_from_assets_pair(assets_pair):
    assets_imgs_list = []
    # Iterate assets to get base

    base_img_pair = {assets_pair[0][0]: assets_pair[0][2].split('_')[-1].split('.')[0] , "img": Image.open(os.path.join(def_path, assets_folder, assets_pair[0][2]))}
    for (categ, idx, name) in assets_pair[1:]:
        image_path = os.path.join(def_path, assets_folder, name)
        assets_imgs_list.append({categ: name.split('_')[-1].split('.')[0], "img": Image.open(image_path)})
    return base_img_pair, assets_imgs_list


def get_current_path():
    return def_path


# Construct json for each generated asset
def get_json_for(variables_string, nft_no):
    temp_json = {"description": asset_types["meta"]["description"],
                 "image": asset_types["meta"]["url"],
                 "planet": asset_types["meta"]["planet"],
                 "species": asset_types["meta"]["species"],
                 "NFT no.": int(nft_no),
                 "attributes": []
                 }

    variables_list = variables_string.split("|")
    for entry in variables_list:
        (categ, var_name) = entry.split('/')
        # Check if pair can be exported
        if asset_types[categ]["can_export"] == 1:
            temp_json["attributes"].append({
                "trait_type": categ,
                "value": asset_types[categ]["desc"][asset_types[categ]["assets"].index(entry)]
            })

    return temp_json


def get_generation_id():
    return asset_types["meta"]["genIteration"]


def get_desc_for_key(categ_key, val_key):
    # Get description for asset variable
    idx = asset_types[categ_key]["assets"].index(categ_key + "/" + val_key)
    return asset_types[categ_key]["desc"][idx]
