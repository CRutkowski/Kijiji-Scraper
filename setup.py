#! /usr/bin/env python3
from setuptools import setup
import sys
if sys.version_info[0] < 3: raise Exception("Sorry, you must use Python 3")
# Helper method that will parse __init__.py to extract VERSION
def parse_setup(key):
    part={}
    for line in INIT.splitlines():
        if key in line:
            exec(line, part)
            break
    return(part[key])
# Read and store init file
INIT = open("./kijiji_scraper/__init__.py",'r').read()
# The text of the README file
README = open("./README.md",'r').read()

setup(
    name                =   'kijiji_scraper',
    description         =   "Track Kijiji ad information and sends out an email when a new ads are found.",
    url                 =   'https://github.com/CRutkowski/Kijiji-Scraper',
    install_requires    =   ['requests','bs4','pyyaml'],
    version             =   parse_setup('VERSION'),
    packages            =   ['kijiji_scraper',], 
    entry_points        =   {'console_scripts': ['kijiji = kijiji_scraper.launcher:main'],},
    classifiers         =   ["Programming Language :: Python :: 3"],
    license             =   'MIT',
    long_description    =   README,
    long_description_content_type   =   "text/markdown"
)