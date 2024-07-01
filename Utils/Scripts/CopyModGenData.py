#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import os
import shutil
import sys
import utils

def CopyGeneratedAssetsFiles(assets_dest_dir, gen_path, subfolder):
    src_path = os.path.join(gen_path, subfolder)
    files = glob.glob(os.path.join(src_path, '**', '*.*'), recursive = True)
    for file in files:
        extension = os.path.splitext(file)[1]
        if extension != '.ndfbin' and extension != '.tag':
            dest_file = os.path.join(assets_dest_dir, os.path.relpath(file, gen_path))
            dest_dir = os.path.dirname(dest_file)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            shutil.copy(file, dest_file)

def CopyModGenData(saved_mod_path):
    gen_path = 'Gen'

    ndfbin_path = os.path.join(gen_path, 'AllPlatforms', 'NDF')
    ndfbin_files = glob.glob(os.path.join(ndfbin_path, '**', '*.ndfbin'), recursive = True)
    for ndfbin_file in ndfbin_files:
        tag_file = os.path.splitext(ndfbin_file)[0] + '.tag'
        if not os.path.isfile(tag_file):
            dest_file = os.path.join(saved_mod_path, os.path.relpath(ndfbin_file, ndfbin_path))
            dest_dir = os.path.dirname(dest_file)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            shutil.copy(ndfbin_file, dest_file)

    dest_gen_dir = os.path.join(saved_mod_path, 'Gen')
    if not os.path.exists(dest_gen_dir):
        os.makedirs(dest_gen_dir)
    CopyGeneratedAssetsFiles(dest_gen_dir, gen_path, 'AllPlatforms')
    CopyGeneratedAssetsFiles(dest_gen_dir, gen_path, 'PC')

def main(argv):
    if len(argv) != 3:
        utils.error(f"Usage: {argv[0]} GAME_NAME MOD_NAME")
        return 2

    game_name = argv[1]
    mod_name = argv[2]
    saved_mod_path = os.path.join(os.environ.get('userprofile'), 'Saved Games', 'EugenSystems', game_name, 'mod', mod_name)
    CopyModGenData(saved_mod_path)

    print(f"Mod Generation Success\nYou can find your config file here : {saved_mod_path}/Config.ini")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
