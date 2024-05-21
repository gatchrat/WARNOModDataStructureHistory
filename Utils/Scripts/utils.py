#!/usr/bin/python
# -*- coding: utf-8 -*-

import fnmatch
import os
import shutil
import sys
import zipfile

BASEDIR = '.base'
BASEZIP = 'base.zip'
NDF = '*.ndf'

def CopyFile(src, dest):
    dirname = os.path.dirname(dest)
    if not os.path.exists(dirname):
        os.makedirs(os.path.dirname(dest))
    else:
        assert os.path.isdir(dirname)
    shutil.copyfile(src, dest)

def _ForAllFiles(src, dest, pattern, f):
    for root, dirnames, filenames in os.walk(src):
        for filename in fnmatch.filter(filenames, pattern):
            source = os.path.join(root, filename)
            relPath = os.path.relpath(source, start=src)
            destination = os.path.join(dest, relPath)
            #print(' ', source, '=>', destination)
            f(source, destination)

def CopyAllFiles(src, dest, pattern):
    _ForAllFiles(src, dest, pattern, CopyFile)

def ZipAllFiles(src, dest, pattern):
    with zipfile.ZipFile(dest, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        _ForAllFiles(src, dest, pattern, lambda s, _: archive.write(s))

def CreateBaseZip():
    if os.path.exists(BASEZIP):
        os.remove(BASEZIP)
    ZipAllFiles(BASEDIR, BASEZIP, NDF)
    shutil.rmtree(BASEDIR)

def ExtractBaseZip(path):
    baseDir = os.path.join(path, BASEDIR)
    baseZip = os.path.join(path, BASEZIP)
    if os.path.exists(baseDir):
        error(baseDir + " directory already exists when it should not, you probably need to delete it.")
    os.mkdir(baseDir)
    zipfile.ZipFile(baseZip, 'r').extractall(baseDir)

def error(msg):
    print("Error:", msg)
    sys.exit()

def warning(msg):
    print("Warning:", msg)
    sys.exit()
