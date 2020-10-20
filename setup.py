# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in wps_report/__init__.py
from wps_report import __version__ as version

setup(
	name='wps_report',
	version=version,
	description='wps_report',
	author='Frappe',
	author_email='craftinteractive.ae',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
