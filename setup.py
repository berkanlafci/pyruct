
from setuptools import setup, find_packages

packages = find_packages(exclude=('pyruct.tests*', 'pyruct.*.tests*'))

setup(
	name="pyruct",
	version="1.0.0",
	description = "Data processing tools for reflection ultrasound computed tomography (RUCT)",
	author = "Berkan Lafci",
	author_email = "lafciberkan@gmail.com",
	url = "https://github.com/berkanlafci/pyruct",
	keywords = ["reflection ultrasound computed tomography", "pulse-echo ultrasound", "image reconstruction", "data analysis"],
	classifiers = [],
	install_requires = ['numpy', 'matplotlib', 'scipy', 'h5py', 'Pillow'],
	provides = ["pyruct"],
	packages = packages,
	include_package_data=True,
	extras_require = {},
	entry_points = {},
	)
