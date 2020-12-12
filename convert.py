# -*- coding: utf-8 -*-

'''
This script converts all annotations files from labelme jason format
to Darknet yolo format ready to use.

Also creates a labels.names with the correct order even if you guys don have it.

TODO - create an in-line parameters version and a split for train and test datasets.

Instructions: put all your image and json files in the folder "dataset" at the same level of the script, 
or edit dataset variable with the correct path

just run the command - python3 convert.py

THe script will create a "result" folder containing all the new txt annotations for darknet, the images to train and the labels.names


'''
import os
from os import walk, getcwd
from PIL import Image
import json
from shutil import copyfile
    

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
    
"""-------------------------------------------------------------------""" 

""" Configura os Paths"""   
dataset = "./dataset/"
output = "./result/"

wd = getcwd()
list_file = open('train.txt', 'w')

""" Pega uma lista com os jsons """
file_name_list = []
file_name_list_full = []
for file in os.listdir(dataset):
    if file.endswith(".json"):
        file_name_list.append(file[:-5])
        
    

""" Processa cada bbox """
labels = []
            
for filen in file_name_list:
    #print(json_name)
    json_name = filen + '.json'
    image_name = filen + '.jpg'
    txt_name = filen + '.txt'
    finalfile = ''
    if os.path.exists(dataset + json_name) and os.path.exists(dataset + image_name):
        file_name_list_full.append(image_name)
        with open(dataset + json_name) as f:
            data = json.load(f)
            #print(data["shapes"])
            for x in data["shapes"]:
                if not x["label"] in labels:
                    labels.append(x["label"])
                #print(x["label"], labels.index(x["label"]))

                x1 = x["points"][0][0]
                y1 = x["points"][0][1]
                x2 = x["points"][1][0]
                y2 = x["points"][1][1]
                #print(x1,x2,y1,y2)

                xmin = min(x1,x2)
                xmax = max(x1,x2)
                ymin = min(y1,y2)
                ymax = max(y1,y2)

                im = Image.open(dataset + image_name)
                w = int(im.size[0])
                h = int(im.size[1])

                b = (xmin, xmax, ymin, ymax)
                bb = convert((w,h), b)
                finalfile += str(labels.index(x["label"])) + ' ' + str(bb[0]) + ' ' + str(bb[1]) + ' ' + str(bb[2]) + ' ' + str(bb[3]) + '\n'

        print(' ')
        file1 = open(output + txt_name,"w")
        file1.writelines(finalfile) 
        file1.close()
        copyfile(dataset + image_name, output + image_name)
        print(finalfile)
            
print(labels)
file2 = open(output + 'labels.names',"w")
for l in labels:
    file2.write(l + '\n') 
file2.close()

for l2 in file_name_list_full:
    list_file.write(l2 + '\n') 
list_file.close()       