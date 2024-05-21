#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import zipfile
import glob

import utils

MODDATA = 'ModData'

def CreateNewMod(modDir):
    if os.path.exists(modDir):
        utils.error('Mod folder already exists.')

    try:
        print("Creating new mod directory:", modDir)
        shutil.copytree(MODDATA, modDir)
        newbase = os.path.join(modDir, utils.BASEZIP)
        with zipfile.ZipFile(newbase, 'r') as archive:
            archive.extractall(modDir)
        print('New mod created successfully!')

    except Exception as e:
        shutil.rmtree(modDir, True)
        utils.error("Could not create mod directory:" + str(e))

if __name__ == "__main__":
    if len(sys.argv) > 2:
        utils.error("Please enter only one mod name, in double quotes if it includes spaces.")

    mod_name = ""
    if len(sys.argv) == 2:
        mod_name = sys.argv[1]
    else:
        mod_name = input("Enter mod name : ")

    CreateNewMod(mod_name)
