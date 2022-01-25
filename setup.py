# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in frepple/__init__.py
from frepple import __version__ as version

setup(
	name="frepple",
	version=version,
	description="Integration between ERPNext and Frepple",
	author="Drayang Chua",
	author_email="dchu0011@student.monash.edu",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
