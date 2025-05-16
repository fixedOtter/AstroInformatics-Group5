# AstroInformatics-Group5
Detect SSR's from ZTF Data in MongoDB

## installing stuff
make sure you have anaconda then use conda to make an environment
```
conda env create
```

then you can install the dependancies for the programs, look at requirements.txt
```
conda install pymongo pandas matplotlib numpy lombscar
```

## Once your environment is set up
```
python main.py section
```
where secction is a integer that corresponds to a 1000 sized slice that the program will analyze from the database