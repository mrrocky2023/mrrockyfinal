from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mrrocky/__init__.py
from vtigercrm import __version__ as version

setup(
	name="mrrocky",
	version=version,
	description="mrrocky",
	author="l",
	author_email="l",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
