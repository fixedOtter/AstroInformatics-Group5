

from pymongo import MongoClient
from astropy.timeseries import LombScargle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#connect to the database
uri = "mongodb://group5:IelC3eVkLz%2BMfPlGAKel4g%3D%3D@cmp4818.computers.nau.edu:27018"
client = MongoClient(uri)

#select the database
db = client["ztf"]

#select the collection
collection = db["snapshot_1_derived_properties"]

#compare asteriods we tested with others
def compare_ssnamenr_asteriod_periods(test_ssnamenr_array):

    #create arrays
    our_test_array = []
    snapshot_test_array = []

    #loop through data to test
    for asteriod in test_ssnamenr_array:
        #find associated data
        data = collection.find_one({"ssnamenr": str(asteriod["ssnamenr"])})
        
        #check if data was in snapshot_1_derived_properties collecetion
        if (data == None):
            continue
        
        #get the periods of the test data
        test_period = float(asteriod["period"])
        data_period = float(data["rotper"])

        #add test periods to output arrays
        our_test_array.append(test_period)
        snapshot_test_array.append(data_period)

    #create comparison scatter plot
    plt.scatter(our_test_array, snapshot_test_array)
    plt.xlim(2, 50)
    plt.title(f'Similarity test')
    plt.xlabel('PD 2024')
    plt.ylabel('PD 2023')
    plt.legend()
    plt.grid(True)
    plt.show()

    

