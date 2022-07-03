pyruct
=======================================================

[![Paper](https://img.shields.io/badge/Paper-IEEE%20TUFFC-b31b1b)](https://ieeexplore.ieee.org/document/9768674)
[![Documentation](https://img.shields.io/badge/Documentation-pyruct-brightgreen)](https://berkanlafci.github.io/pyruct/)
[![Data](https://img.shields.io/badge/Data-Zenodo-blue)](https://zenodo.org/record/6541837#.YrwSZXhByEI)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)](https://mit-license.org/)  

Python Package for Reflection Ultrasound Computed Tomography (RUCT) Delay And Sum (DAS) Beamforming

Paper&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: [IEEE TUFFC Link](https://ieeexplore.ieee.org/document/9768674)  
Documentation&nbsp;: [Website Link](https://berkanlafci.github.io/pyruct/)  
Data&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: [Zenodo Link](https://zenodo.org/record/6541837#.YrwUoHhByEJ)  

<img src="https://github.com/berkanlafci/pyruct/blob/main/docs/_img/readmeImage.png" width="1000" height="180">

Latest package release:  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5599811.svg)](https://doi.org/10.5281/zenodo.5599811)

Public dataset:  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6541837.svg)](https://doi.org/10.5281/zenodo.6541837)

The imaging setup is explained in the following paper [Lafci, B. et al.](https://ieeexplore.ieee.org/document/9768674) Synthetic Transmit Aperture (STA) method for pulse-echo ultrasound was used in data acquisition. All images were reconstructed using Delay And Sum (DAS) algorithm and compounded to create final high contrast images.

Installation
-------------------------------------------------------
This project uses pip package manager. Please run the following command in your terminal to install the package.
```bash
pip install git+https://github.com/berkanlafci/pyruct.git
```

Usage
-------------------------------------------------------
After installing package, the functions can be called using python scripts.

Example scripts to use pyruct package can be found in _examples folder.

For example, delay and sum example on cpu is called with following commands in terminal.
```bash
python exampleCpuDAS.py
```
The example scripts can be written by users.

pyruct package can be imported in python scripts using following line.
```python
import pyruct as pt
```
After importing the package, the functions can be called with following lines in python script.
```python
usData      = pt.usReader(filePath=filePath) 	# read data
das         = pt.cpuDAS()                      	# create reconstruction object
imageRecon  = das.recon(usData.sigMat)         	# reconstruct image
```

Data
-------------------------------------------------------
Test data is publicly available [here](https://doi.org/10.5281/zenodo.5599242).

After the download, place the data in "data/rawData/" folder that shares the same root directory with "exampleCpuDAS.py" script that can be run for testing "pyruct".

Citation
-------------------------------------------------------
If you use this package and/or data in your research, please cite the following paper.

B. Lafci, J. Robin, X. L. Deán-Ben and D. Razansky, "Expediting Image Acquisition in Reflection Ultrasound Computed Tomography," in IEEE Transactions on Ultrasonics, Ferroelectrics, and Frequency Control, doi: [10.1109/TUFFC.2022.3172713](https://ieeexplore.ieee.org/document/9768674).

Acknowledgements
-------------------------------------------------------
This project is supported by Swiss Data Science Center (SDSC) grant C19-04.

License
-------------------------------------------------------
This project is licensed under [MIT License](https://mit-license.org/).