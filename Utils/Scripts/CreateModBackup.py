#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import zipfile
from time import gmtime, strftime

import utils

ASSETDATA = 'AssetsModding'
COMMONDATA = 'CommonData'
GAMEDATA = 'GameData'
GENFOLDER = 'Gen'

BACKUPFOLDER = 'Backup'

def ZipAllFiles(directory, baseDirectory, zipFile):
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            source = os.path.join(root, filename)
            relPath = os.path.relpath(source, start='.')
            zipFile.write(relPath)


def CreateModBackup(name):
    if name is None or name == "":
        name = strftime("%Y_%m_%d_%H_%M_%S", gmtime())

    if not os.path.exists(BACKUPFOLDER):
        os.mkdir(BACKUPFOLDER)
    if not name.endswith(".zip"):
        name = name + ".zip"

    fullPath = os.path.join(BACKUPFOLDER, name);

    if os.path.exists(fullPath):
        utils.error("Backup " + name + " already exists, please use an other name.")

    try:
        with zipfile.ZipFile(fullPath, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            ZipAllFiles(ASSETDATA, '.', archive)
            ZipAllFiles(COMMONDATA, '.', archive)
            ZipAllFiles(GAMEDATA, '.', archive)

    except Exception as e:
        if os.path.exists(fullPath):
            os.remove(fullPath)
        utils.error("Could not create backup file :" + str(e))



if __name__ == "__main__":
    if len(sys.argv) > 2:
        utils.error("Please enter only one name, in double quotes if it includes spaces.")

    backup_name = ""
    if len(sys.argv) == 2:
        if sys.argv[1] != '-autoname':
            backup_name = sys.argv[1]
    else:
        backup_name = input("Enter backup name : ")

    CreateModBackup(backup_name)
