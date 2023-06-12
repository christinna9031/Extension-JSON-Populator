# MIT License
# 
# Copyright (c) 2023 Christina K.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json
import time
import re

# Customizable variables
IGNORED_DIRS = {"node_modules"}  # Add any other folders you want to ignore here
EXTENSIONS_FOLDER_PATH = 'E:/Stream/SAMMI EXTENSIONS'  # Change this to the folder where your extensions are
EXTENSIONS_AUTHOR = 'YOUR NAME'  # Change this to your name
OUTPUT_FILE = 'extensions.json'  # Name of the output file

def find_sef_files(folder):
    """
    Function to find all the .sef files in the specified directory and its subdirectories.
    """
    sef_files = {}

    for dirpath, dirnames, filenames in os.walk(folder):
        # skip any sef files in the immediate root folder, assuming each extension is in its own folder
        if dirpath == folder or any(ignored_dir in dirpath for ignored_dir in IGNORED_DIRS):
            continue

        sef_files_in_folder = [f for f in filenames if f.endswith('.sef')]
        
        # if there are any sef files in the folder, get the newest one
        if sef_files_in_folder:
            newest_sef_file = max(sef_files_in_folder, key=lambda f: os.stat(os.path.join(dirpath, f)).st_mtime)
            sef_files[dirpath] = os.path.join(dirpath, newest_sef_file)
            
    return sef_files

def parse_sef_files(sef_files):
    """
    Function to parse the .sef files and extract the extension details.
    """
    extensions = {}
    
    # loop through each sef file
    for dirpath, filepath in sef_files.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            # split the file into lines
            content = f.read().splitlines()
            
            # set default values
            extension_name = ''
            extension_info = ''
            extension_version = '1.0'
            
            # loop through each line
            for i in range(len(content)):
                line = content[i]
                # if the line contains the extension name, set the extension name to the next line
                if '[extension_name]' in line:
                    extension_name = content[i+1].strip()
                # if the line contains the extension info, set the extension info to the next line
                elif '[extension_info]' in line:
                    extension_info = content[i+1].strip() or ''
                # if the line contains the extension version and the next line is not empty, set the extension version to the next line
                elif '[extension_version]' in line and content[i+1].strip():
                    extension_version = content[i+1].strip()  # Set only if non-empty

            # if the extension name is not in the extensions list or the extension version is greater than the latest version, add the extension to the list
            if extension_name not in extensions or float(extension_version) > float(extensions[extension_name]['details']['latest_version']):
                # add the extension to the list
                extensions[extension_name] = {
                    'extension_name': extension_name,
                    'details': {
                        'author': EXTENSIONS_AUTHOR,
                        'description': extension_info,
                        'latest_version': extension_version,
                        'download_link': ''
                    }
                }
    
    return list(extensions.values())

def main(folder_path):
    """
    Main function that runs the whole process of finding and parsing the .sef files.
    """
    # get the sef files
    sef_files = find_sef_files(folder_path)
    extensions = parse_sef_files(sef_files)
    
    data = {
        'extensions': extensions
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    main(EXTENSIONS_FOLDER_PATH)
