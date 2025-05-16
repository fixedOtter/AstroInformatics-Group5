# Processing data from ZTF to identify Super Slow Rotators (AstroInformatics-Group5)
Northern Arizona University May 2025: The purpose of our Astroinformatics Bootcamp is to prepare and write code for the upcoming data to be delieverd from the LSST. In thanks to Zwicky Transient Facility, we are able to derive the information of interest decribed by this data. The collection of information we focused on was the rotational periods of all objects from 2018-today. From these rotational periods we were able to derive the periodograms and Magnitude vs Phase information. The periodograms reveal the period. The periodogram derives the actual period the asteroids are rotating at, while the lightcurve represents the ideal rotation period the Super Slow Rotators are traveling at. The

## Installation
make sure you have anaconda then use conda to make an environment
```
conda env create
```

then you can install the dependancies for the programs, look at requirements.txt
```
conda install pymongo pandas matplotlib numpy lombscar
```

## To begin
```
python main.py section
```
where secction is a integer that corresponds to a 1000 sized slice that the program will analyze from the database
