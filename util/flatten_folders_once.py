# if the current folder contains subfolders which also contain files/subfolders,
# then their content will be moved to the parent folder with a prefix of the folder name

import os
import shutil

folders = [each for each in os.listdir('.') if os.path.isdir(each)]
for folder in folders:
        for content in os.listdir(folder):
                shutil.move(os.path.join(folder, content), folder + '___' + content)
for folder in folders:
        os.rmdir(folder)