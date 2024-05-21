#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import winreg

import utils

PATHTOMOD = os.path.join("EugenSystems", "WARNO", "mod")
FILEEXTENSION = ('.ndfbin', '.spk', '.ppk', '.dic', '.tgv', '.mpk', '.apk')

def CleanUpModFolder(modName):
    try:
        savedGameRegistry = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FolderDescriptions\\{4C5C32FF-BB9D-43b0-B5B4-2D72E54EAAA4}")
        registryValue = winreg.QueryValueEx(savedGameRegistry, "RelativePath")
        savedGameDirectory = registryValue[0]
    except Exception as e:
        utils.error("SavedGame registry not found, please cleanup your mod folder by yourself, except Config.ini. Error : " + str(e))

    modFolder = os.path.join(os.path.expanduser('~'), savedGameDirectory, PATHTOMOD, modName)
    if not os.path.isdir(modFolder):
        utils.warning("directory not found : " + modFolder + ". There will be no cleanup.")
        return

    for root, dirs, files in os.walk(modFolder):
        for filename in files:
            if filename.lower().endswith(FILEEXTENSION):
                os.remove(os.path.join(root, filename))
