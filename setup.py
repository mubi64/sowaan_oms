from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sowaan_oms/__init__.py
from sowaan_oms import __version__ as version

setup(
	name="sowaan_oms",
	version=version,
	description="Sowaan OMS is to manage online orders",
	author="Sowaan Pvt. Limited",
	author_email="info@sowaan.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
