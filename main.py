import os
import json
import random
from PIL import Image
from PIL.ImageQt import ImageQt

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QLabel,
    QSlider,
    QTextEdit,
    QMessageBox,
    QProgressBar,
    QApplication

)
from PyQt5.QtCore import (
    Qt,
    QRect,
)
from utils import get_asset_count, init_asset_counts, get_asset_by_id, load_assets_probabilities, \
    has_all_assets, get_images_from_assets_pair, get_assets_details, get_current_path, get_available_variables_count, \
    get_total_number_variables, get_json_for, get_generation_id, get_desc_for_key
from PyQt5 import QtGui



############################################
# Define image scaling factor
############################################
orig_im_h, orig_im_w = (2112, 1584)
scaling_factor = 4
extra_space = 200
(new_im_w, new_im_h) = (int(orig_im_w / scaling_factor), int(orig_im_h / scaling_factor))
(extra_w, extra_h) = (new_im_w + 2 * extra_space, new_im_h + extra_space)

#############################################
# Define extra % value for variables
#############################################
extra_percentage = 10
trials = 8


#############################################
# Define Widgets
#############################################

class Ui_MainWindow(object):
    def __init__(self):
        # Read asset counts
        init_asset_counts()
        assets_dict = get_assets_details()
        self.current_image = None

        # Define id's to keep track of textures
        # asset_class : current_id
        self.assets_details = {}

        # Define widgets/sliders/callbacks
        self.main_widget = QWidget(MainWindow)
        self.image_widget = QLabel(self.main_widget)
        self.progress_bar = QProgressBar(self.main_widget)
        self.save_folder_textedit = QTextEdit(self.main_widget)

        for i, key in enumerate(list(assets_dict.keys())[1:]):
            self.assets_details[key] = 0
            idx = i * 50
            self.label = QLabel(self.main_widget)
            self.slider = QSlider(self.main_widget)
            self.slider.setGeometry(QRect(new_im_w + int(extra_space / scaling_factor), idx + 50, extra_space, 22))
            self.slider.setOrientation(Qt.Horizontal)
            self.slider.setObjectName("{}.slider".format(str(key)))
            self.slider.setTickInterval(1)
            self.slider.setMinimum(0)
            count = get_asset_count(key)
            if count == 0:
                self.slider.setDisabled(True)
            else:
                self.slider.setDisabled(False)
                self.slider.setMaximum(get_asset_count(key))
            self.slider.valueChanged['int'].connect(self.slider_changed)
            self.label.setObjectName("{}.label".format(str(key)))
            self.label.setGeometry(
                QRect(new_im_w + extra_space + int(extra_space / scaling_factor) + 20, idx+52, 120, 13))
            self.label.setText("{} : 0".format(str(key)))

        self.generate_button = QPushButton(self.main_widget)
        self.edit_no_samples_text = QTextEdit(self.main_widget)
        self.save_btn_current_sample = QPushButton(self.main_widget)
        self.progress_bar_label = QLabel(self.main_widget)

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(extra_w, extra_h)
        MainWindow.setFixedSize(extra_w, extra_h)
        off_img_w, off_img_h = 20, 20
        self.main_widget.setObjectName("main_widget")

        self.image_widget.setGeometry(QRect(off_img_w, off_img_h, new_im_w, new_im_h))
        placeholder = QtGui.QPixmap("./assets/placeholder.png")
        placeholder = placeholder.scaled(new_im_w, new_im_h, Qt.KeepAspectRatio)
        self.image_widget.setPixmap(placeholder)
        self.image_widget.setObjectName("im_widget")

        # Setting up generate button
        self.generate_button.setGeometry(QRect(off_img_w - 5, extra_h - extra_space + off_img_h + 50, 100, 50))
        self.generate_button.setText("Generate")
        self.generate_button.clicked.connect(self.generate_btn_clicked)

        # Setting up save button
        self.save_btn_current_sample.setGeometry(QRect(off_img_w + 115 , extra_h - extra_space + off_img_h + 50, 100, 50))
        self.save_btn_current_sample.setText("Save")
        self.save_btn_current_sample.clicked.connect(self.save_current)

        # Setting up text field for number of generated samples
        self.text_edit_label = QLabel(self.main_widget)
        self.edit_no_samples_text.setPlaceholderText("1,2,3")
        self.edit_no_samples_text.setGeometry(QRect(off_img_w + 120, extra_h - extra_space + 15 + off_img_h, 50, 30))
        self.text_edit_label.setText("#Samples")
        self.text_edit_label.setGeometry(QRect(off_img_w + 120, extra_h - extra_space + off_img_h - 2, 60, 20))

        # Setting up progress bar
        self.progress_bar.setGeometry(QRect(5,  extra_h - off_img_h-5, extra_w - 10, 20))
        self.progress_bar_label.setGeometry(QRect(int(extra_w / 2),  extra_h - off_img_h - 35, 120, 30))
        self.progress_bar_label.setText("Progress Bar : 0 %")

        # Setting up text-box for folder and extension
        self.save_folder_textedit.setGeometry(QRect(off_img_w, extra_h - extra_space + 15 + off_img_h, 100, 30))
        self.save_folder_label = QLabel(self.main_widget)
        self.save_folder_label.setText("Folder")
        self.save_folder_label.setGeometry(QRect(off_img_w, extra_h - extra_space - 2 + off_img_h, 60, 20))

        MainWindow.setCentralWidget(self.main_widget)
        MainWindow.setWindowTitle("NFT Generator")
        MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))

    def update_assets(self):
        base_categ = list(self.assets_details.keys())[0]
        body_base_img = get_asset_by_id(base_categ, self.assets_details[base_categ])
        body_base_img = body_base_img.resize((new_im_w, new_im_h), Image.ANTIALIAS)
        # Get additional assets
        for key in self.assets_details:
            asset_img = get_asset_by_id(key, self.assets_details[key])
            if asset_img is not None:
                asset_img = asset_img.resize((new_im_w, new_im_h), Image.ANTIALIAS)
                body_base_img.paste(asset_img, mask=asset_img)
        self.current_image = ImageQt(body_base_img)

        self.image_widget.setPixmap(QtGui.QPixmap.fromImage(self.current_image))

    def slider_changed(self, val):
        slider_name = self.main_widget.sender().objectName()
        # Get asset category assigned to the slider
        asset_category = slider_name.split('.')[0]
        self.assets_details[asset_category] = int(val)
        label = self.main_widget.findChild(QLabel, "{}.label".format(asset_category))
        label.setText("{}: {}".format(asset_category, self.assets_details[asset_category]))
        self.update_assets()

    def save_current(self):
        #TODO: add ids for assets b1f1c1...
        if self.current_image is not None:
            self.current_image.save("saved.png")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Saved Successfully")
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Start drawing")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

    '''
    # GEN_IMAGES
    This is the method that generates all the images.
    '''
    def generate_btn_clicked(self):

        # Get folder path where to save the assets
        save_folder_name = self.save_folder_textedit.toPlainText()
        save_dir_path = os.path.join(get_current_path(), save_folder_name)

        # Create folder if it doesn't exist
        if not os.path.exists(save_dir_path):
            os.makedirs(save_dir_path)

        # Get number of samples, (if the number is valid, get the number else set to 1)
        str_content = self.edit_no_samples_text.toPlainText()
        number_of_assets = int(str_content) if str_content.isdigit() else 1

        # Get all assets with their probabilities
        variable_dict = load_assets_probabilities(number_of_assets + int(extra_percentage * number_of_assets / 100))

        # Select randomly 1 png for each category
        generated_assets = []

        # Counter to keep track of iterations done until the desired number of assets generated is met
        cnt = 0

        # Once it finishes all the random choices in one iteration, does another random select
        retries = 0

        # Take the generation ID, to further increment it when saving assets
        gen_id = get_generation_id()

        # Used for saving each variable's frequence
        frequency_dict = {}

        while True:
            temp_list = []
            # Take one variable of each from the random random selected ones.
            for key in variable_dict.keys():
                index = random.randint(0, len(variable_dict[key]["random_choices"]) - 1)
                temp_list.append((key, index, variable_dict[key]["random_choices"][index]))

            # Define a unique string for each asset
            id_placeholder = "|".join({str(val_name) for (_, _, val_name) in temp_list})

            # Check if it already exists (duplicate)
            if id_placeholder not in generated_assets:
                generated_assets.append(id_placeholder)

                # Validate it contains all the variables, if yes continue with layering the images
                valid = has_all_assets(temp_list)
                if valid:
                    base_img_dict, assets_imgs_list = get_images_from_assets_pair(temp_list)
                    # capital B in the filename stands for BASE asset, on which all the others would be layered on top
                    file_name = "{}-B{}_".format(gen_id, base_img_dict[next(iter(base_img_dict))])
                    for asset_dict in assets_imgs_list:
                        categ, idx = next(iter(asset_dict)), asset_dict[next(iter(asset_dict))]
                        file_name += "{}{}_".format(categ[0], idx)
                        base_img_dict["img"].paste(asset_dict["img"], mask=asset_dict["img"])

                    # Save image
                    base_img_dict["img"].save(os.path.join(save_dir_path, file_name + '.png'))

                    # Construct json for generated asset
                    asset_json = get_json_for(id_placeholder, gen_id)

                    # Assure "metadata" folder for asset.json is created
                    asset_json_metadata_path = os.path.join(get_current_path(), save_dir_path, "metadata")
                    if not os.path.exists(asset_json_metadata_path):
                        os.mkdir(asset_json_metadata_path)

                    # Write json for generated asset
                    with open(os.path.join(asset_json_metadata_path, file_name + '.json'), "w") as file_metadata:
                        json.dump(asset_json, file_metadata)

                    # Increase gen_id since the asset was saved
                    gen_id += 1

                    # Update progress bar
                    self.progress_bar_label.setText(
                        "Progress: {:.2f} %".format((cnt * 100) / number_of_assets))
                    self.progress_bar.setValue(int((cnt * 100) / number_of_assets))

                    # Update pyqt events pool
                    QApplication.processEvents()
                    cnt += 1

                    # Init dictionary with all the variables frequencies
                    variables = id_placeholder.split("|")
                    for entry in variables:
                        (categ, var_name) = entry.split('/')
                        if categ not in frequency_dict.keys():
                            frequency_dict[categ] = {}
                            frequency_dict[categ]["total"] = get_total_number_variables(categ)
                        if len(variable_dict[categ]["unused"]) > 0:
                            for entry in variable_dict[categ]["unused"]:
                                frequency_dict[categ][entry.split('/')[-1]] = 0
                        if var_name not in frequency_dict[categ].keys():
                            frequency_dict[categ][var_name] = 0
                        frequency_dict[categ][var_name] += 1

                    # Delete ids of the png files that were already generated
                    for (key, index, name) in temp_list:
                        variable_dict[key]["random_choices"].pop(index)
            else:
                # Delete ids of the png files that were already generated
                for (key, index, name) in temp_list:
                    variable_dict[key]["random_choices"].pop(index)

            # Check how many variables are left after the current asset generation
            variables_left = get_available_variables_count(variable_dict)
            if variables_left == 1:
                print('Reloading Assets # {}'.format(retries+1))
                variable_dict = load_assets_probabilities(number_of_assets)
                retries += 1

            # Break the loop when the desired number of assets is met, or ran out of trials
            if cnt == number_of_assets or retries == trials:
                self.progress_bar_label.setText(
                    "Progress: {:.2f} %".format(100.00))
                self.progress_bar.setValue(100)
                with open(os.path.join(get_current_path(), save_dir_path, "VariablesFrequencies.txt"), "w") as out_file:
                    for entry in frequency_dict.keys():
                        out_file.write("\n" + entry + "\n")
                        for key in list(frequency_dict[entry].keys())[1:]:
                            out_file.write("\t{} - {} out of {} ({:.2f} %) \n".format(get_desc_for_key(entry, key), frequency_dict[entry][key], number_of_assets, ((frequency_dict[entry][key] * 100) / number_of_assets)))
                break
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("{} Samples Generated Successfully.".format(cnt))
        msg.setWindowTitle("Success")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

        # Reset progress bar
        self.progress_bar_label.setText("Progress: {:.2f} %".format(0))
        self.progress_bar.setValue(0)


if __name__ == "__main__":
    while True:
        import sys
        app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        ui = Ui_MainWindow()
        ui.setup_ui(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
