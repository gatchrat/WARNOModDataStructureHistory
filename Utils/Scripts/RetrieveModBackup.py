#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import glob
import zipfile

import winreg

import utils
import generated.generatedutils

MODDATA = os.path.join('..', 'ModData')
PATHTOMOD = os.path.join("EugenSystems", "%GAMENAME%", "mod")
GENFOLDER = 'Gen'

BACKUPFOLDER = 'Backup'


def RetrieveModBackup(name):
    if not os.path.exists(BACKUPFOLDER):
        utils.error("No backup folder.")

    if name is None or name == "":
        backupList = glob.glob(os.path.join(BACKUPFOLDER, "*.zip"))
        if len(backupList) == 0:
            utils.error("No backup file found.")
        name = max(backupList, key=os.path.getctime);

    if not name.endswith(".zip"):
        name = name + ".zip"

    fullPath = name
    if os.path.dirname(name) != BACKUPFOLDER:
        fullPath = os.path.join(BACKUPFOLDER, name);

    if not os.path.exists(fullPath):
        utils.error("Can't find " + fullPath)

    try:
        with zipfile.ZipFile(fullPath, 'r', compression=zipfile.ZIP_DEFLATED) as archive:
            archive.extractall('.')

    except Exception as e:
        utils.error("Could not retrieve backup file :" + str(e))

    #copy de la gen de la base pour assurer une gen fonctionnelle apres le retrieve
    shutil.rmtree(GENFOLDER)
    shutil.copytree(os.path.join(MODDATA, GENFOLDER), GENFOLDER)

    #cleanup du dossier de mod dans SavedGames
    generated.generatedutils.CleanUpModFolder(os.path.split(os.getcwd())[1])

if __name__ == "__main__":
    if len(sys.argv) > 2:
        utils.error("Please enter only one name, in double quotes if it includes spaces.")

    backup_name = ""
    if len(sys.argv) == 2:
        if sys.argv[1] != '-autoname':
            backup_name = sys.argv[1]
    else:
        backup_name = input("Enter backup name : ")

    RetrieveModBackup(backup_name)
