#!/usr/bin/python
# -*- coding: utf-8 -*-

import diff3
import fnmatch
import os
import shutil
import sys
import glob

import utils
import generated.generatedutils

MODDATA = os.path.join('..', 'ModData')

def _UpdateDirectory(directory):
    conflictedFiles = []

    shutil.rmtree(directory + '_backup', True)
    shutil.copytree(directory, directory + '_backup')

    try:
        moddataPath = os.path.join(MODDATA, utils.BASEDIR, directory)

        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, utils.NDF):

                moddedFile = os.path.join(root, filename)
                relPath = os.path.relpath(moddedFile, start=directory)
                baseFile = os.path.join(utils.BASEDIR, directory, relPath)
                newFile = os.path.join(moddataPath, relPath)

                if not os.path.exists(newFile) and not os.path.exists(baseFile):
                    continue

                old = []
                new = []
                mod = []

                if not os.path.exists(newFile) and os.path.exists(baseFile):
                    with open(baseFile, encoding='utf8') as f:
                        old = f.readlines()
                    with open(moddedFile, encoding='utf8') as f:
                        mod = f.readlines()

                    os.remove(moddedFile)
                    if old != mod:
                        print("  File %s does not exist anymore in the current version of the game." % moddedFile)
                        print("  Your changes cannot be saved automatically, but you can do it manually with the backup file %s." % os.path.join(directory + '_backup', relPath))
                    continue

                if os.path.exists(baseFile):
                    with open(baseFile, encoding='utf8') as f:
                        old = f.readlines()
                with open(newFile, encoding='utf8') as f:
                    new = f.readlines()
                with open(moddedFile, encoding='utf8') as f:
                    mod = f.readlines()

                merge = diff3.merge(new, old, mod)

                with open(moddedFile, 'w', encoding='utf8', newline='') as f:
                    f.writelines(merge['body'])

                if merge['conflict'] > 0:
                    conflictedFiles.append(moddedFile)

        for root, dirnames, filenames in os.walk(moddataPath):
            for filename in fnmatch.filter(filenames, utils.NDF):

                newFile = os.path.join(root, filename)
                relPath = os.path.relpath(newFile, start=moddataPath)
                moddedFile = os.path.join(directory, relPath)
                if not os.path.exists(moddedFile):
                    utils.CopyFile(newFile, moddedFile)

    except Exception as e:
        shutil.rmtree(directory, True)
        shutil.copytree(directory + '_backup', directory)
        raise e

    return conflictedFiles

def UpdateMod():
    try:
        print("Updating mod:", os.getcwd().split('\\')[-1])

        utils.ExtractBaseZip('.')
        utils.ExtractBaseZip(MODDATA)

        #On update les bats
        batFiles = glob.iglob(os.path.join(MODDATA, "*.bat"))
        for bat in batFiles:
            if os.path.isfile(bat):
                shutil.copy2(bat, '.')

        conflicts = _UpdateDirectory('GameData') + _UpdateDirectory('CommonData')

        if len(conflicts) > 0:
            print("\nMod updated with conflicts. Files needing manual correction:\n")
            for c in conflicts:
                print("   ", c)
            input("\nPlease merge your changes, and press <Enter> when you're done. You will then be based on the latest release of the game.")

        shutil.rmtree(utils.BASEDIR, True)
        shutil.rmtree(os.path.join(MODDATA, utils.BASEDIR), True)

        shutil.rmtree('Gen', True)
        shutil.copytree(os.path.join(MODDATA, 'Gen'), 'Gen')

        os.remove(utils.BASEZIP)
        shutil.copy(os.path.join(MODDATA, utils.BASEZIP), utils.BASEZIP)

        generated.generatedutils.CleanUpModFolder(os.path.split(os.getcwd())[1])

        print("Mod updated successfully!")

    except Exception as e:
        shutil.rmtree(utils.BASEDIR, True)
        shutil.rmtree(os.path.join(MODDATA, utils.BASEDIR), True)
        utils.error("could not update mod: " + str(e))

if __name__ == "__main__":
    if len(sys.argv) != 1:
        utils.error("no parameters required.")

    UpdateMod()
