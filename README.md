# Processing data from ZTF to identify Super Slow Rotators (AstroInformatics-Group5)
Northern Arizona University May 2025: The purpose of our Astroinformatics Bootcamp is to prepare and write code for the upcoming data to be delieverd from the LSST. In thanks to Zwicky Transient Facility, we are able to derive the information of interest decribed by this data. The collection of information we toyed with 1was the rotational periods of all objects from 2018-today. From these rotational periods we were able to derive the periodograms and Magnitude vs Phase information. The periodograms reveal the period. The periodogram derives the actual period the asteroids are rotating at, while the lightcurve represents the ideal rotation period the Super Slow Rotators are traveling at. Furthermore we were tasked with comparing the periodograms derived from the ZTF data occurring between 2018-2025 data set to periodograms derived from ZTF and LCDB data from 2018-2020. Some of our data outputs reflect the rotation of the Earth with the simultaneous rotation of the SSR which caused aliasing errors naturally. Monsoon was then utilized to submit this job and paralleize the data output. 
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

# File Structure

### main.py 
The file that pulls in our various scripts for data anaylsis and the file that queries the database for the data. 

### lombs_gargle_calculator.py
This file derives our period vs. power periodograms for us to determine the cycle of our potential slow rotators. 

### lightcurve_script.py 
This file plots phase versus absolute magnitude in concordance with our derived periods from our Lomb Scargle algorithm 

### potential_ssr.py 
This checks the period information of each asteroid in the database and adds them to an array if they meet the criteria

### app.ipynb
This code places the periodogram and light curves plots side by side for comparison 

# Software used 
Python, jupyter notebooks, Monsoon, OnDemand 
