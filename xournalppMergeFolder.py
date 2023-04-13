#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 21:56:21 2020
@author: mate

Modified on Wed Apr 12 21:28:48 2023
@author: AyushmaanAggarwal
"""

import subprocess
import os
import sys
import time

args = sys.argv

#Testing whether enough arguments are provided
if len(args)!=3:
    print("ERROR: please call via Xournalpputils.py input_folder output_file")
    exit()

# Get all the xopp files in the desired folder
input_folder = args[1]
input_files = []
for filename in os.listdir(input_folder):
    if ".xopp" in filename and not "autosave" in filename:
        input_files.append(filename)
        
input_files.sort()
output_file = args[-1]
output_xml = output_file[:output_file.index(".")]+".xml"

# Confirm with user that the right action is being performed
print("The following files will be combined in the following order:")
for input_file in input_files:
    print(input_file, end=", ")
print(); print()
if os.path.exists(output_file):
    print("The following file will be overwritten:")
else:
    print(f"The following file will be created:")
print(output_file); print()

print("Would you like to continue [y,n]: ", end="")
user_input = input()
print()
if not "y" in user_input and not "Y" in user_input:
    exit()
    
xml_files = []

# Convert the .xopp files to .xml files
subprocess.os.popen(f"mkdir '{input_folder}/temp_xml'")
time.sleep(0.25)

print("Converting files")
print("Progress: ", end=""); sys.stdout.flush()
        
for file in input_files:
    xmlName = f"{input_folder}/temp_xml/{file[:file.index('.')]}.xml"
    file = f'"{file}"'
    archiveName = f'"{xmlName}.gz"'
    subprocess.os.popen("cp "+file+" "+archiveName)
    time.sleep(.5)
    gzip_error = subprocess.os.popen("gunzip -f "+archiveName).read()
    if gzip_error != "":
        print(gzip_error)
    xml_files.append(xmlName)
    print("*", end=" ")
    sys.stdout.flush()
print(); print()

print("Finished opening all files")

# the headers to the xml files contain either "xml version", "xournal", "title", "preview"
print(); print("Processing files")
string = ""
headerIdentifiers =  "xml version", "xournal", "title", "preview"

# Add headers to the string
with open(xml_files[0], 'r') as file:
    for line in file.readlines():
        isHeader = any([line.__contains__(header) for header in headerIdentifiers]) 
        if isHeader and not line.__contains__("/xournal"):
            string += line + "\n"
            
# Add the pages to the string
print("Progress: ", end=""); sys.stdout.flush()
for xml_file in xml_files:
    with open(xml_file, "r") as file:
        for line in file.readlines():
            isHeader = any([line.__contains__(header) for header in headerIdentifiers]) 
            if not isHeader:
                string += line + "\n"
    print("*", end=" ")
    sys.stdout.flush()
string += "</xournal>"

print();print()
# save string as xml output file
with open(output_xml, 'w') as file:
    file.write(string)
    
# convert xml file back to .xopp
print("Packing temporary file "+output_xml+"...")
print(subprocess.os.popen(f"gzip '{output_xml}'").read())
time.sleep(1)
subprocess.os.popen("mv "+output_xml+".gz "+ output_file)

# deleting temporary folder
subprocess.os.popen(f"rm -rf '{input_folder}/temp_xml'")
print(f"Completed writing to {output_file}")