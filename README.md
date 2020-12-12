# LabelMeJsonToDarknet

This script converts all annotations files from labelme jason format
to Darknet yolo format ready to use.

Also creates a labels.names with the correct order even if you guys don have it.

TODO - create an in-line parameters version and a split for train and test datasets.

Instructions: put all your image and json files in the folder "dataset" at the same level of the script, 
or edit dataset variable with the correct path

just run the command - python3 convert.py

THe script will create a "result" folder containing all the new txt annotations for darknet, the images to train and the labels.names
