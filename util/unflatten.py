import shutil
import os

for file in os.listdir('.'):
	if '__' in file:
		name_split = file.split('___', 1)
		foldername = name_split[0]
		filename = name_split[1]
		os.makedirs(foldername, exist_ok=True)
		shutil.move(file, os.path.join(foldername, filename))
