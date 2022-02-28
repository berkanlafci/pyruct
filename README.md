pyruct
=======================================================

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5599811.svg)](https://doi.org/10.5281/zenodo.5599811)

Python Package for Reflection Ultrasound Computed Tomography (RUCT) Delay And Sum (DAS) Beamforming

<img src="https://github.com/berkanlafci/pyruct/blob/main/docs/_img/readmeImage.png" width="1000" height="180">

| Hex key test data can be found in the following link:
| [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5599242.svg)](https://doi.org/10.5281/zenodo.5599242)

The imaging setup is explained in these papers [Lafci, B. et al.](https://www.sciencedirect.com/science/article/pii/S1476558620301639), [Merčep, E. et al](https://www.nature.com/articles/s41377-019-0130-5). Synthetic Transmit Aperture (STA) method for pulse-echo ultrasound was used in data acquisition. All images were reconstructed using Delay And Sum (DAS) algorithm and compounded to create final high contrast images.

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
Test data will be made publicly available.

After the download, place the data in "data/rawData/" folder that shares the same root directory with "exampleCpuDAS.py" script that can be run for testing "pyruct".

Citation
-------------------------------------------------------
If you use this package in your research, please cite it as follows

Lafci, B., Robin, J., Dean-Ben, X. L., & Razansky, D. (2021). pyruct (Version 1.0.3) [Computer software]. https://doi.org/10.5281/zenodo.5599811

Acknowledgements
-------------------------------------------------------
This project is supported by Swiss Data Science Center (SDSC).

References
-------------------------------------------------------
[1] Lafci, B., Merčep, E., Herraiz, J.L., Deán-Ben, X.L., Razansky, D. Noninvasive multiparametric characterization of mammary tumors with transmission-reflection optoacoustic ultrasound, Neoplasia, Volume 22, Issue 12, 2020, Pages 770-777, ISSN 1476-5586, https://doi.org/10.1016/j.neo.2020.10.008.

[2] Merčep, E., Herraiz, J.L., Deán-Ben, X.L., Razansky, D. Transmission–reflection optoacoustic ultrasound (TROPUS) computed tomography of small animals. Light Sci Appl 8, 18 (2019). https://doi.org/10.1038/s41377-019-0130-5

License
-------------------------------------------------------
This project is licensed under [MIT License](https://mit-license.org/).