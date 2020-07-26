
"""
Credit to the YouTuber Tech With Tim for the general framework of this script
"""

import subprocess
import sys
import get_pip
import os
import importlib
import contextlib

def install_pkg(package):

    subprocess.call([sys.executable, '-m', 'pip', 'install', package])

required = []
failed = []

try:
    requirements = open("requirements.txt", "r")
    packages = requirements.readlines();
    requirements = [package.strip().lower() for package in packages]
    requirements.close()
except FileNotFoundError:
    print("[ERROR] no requirements.txt found in local directory")

if required:
    pass
else:
    print("[INFO] No packages necessary to install")

if failed:
    print("[INFO] " + len(failed) + " packages were not installed. Those packages are:\n")
    for i in range(0, len(failed)):
        print("\t" + packages[i] + "\n")
    print("\n")