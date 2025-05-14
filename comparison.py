
from pymongo import MongoClient
from astropy.timeseries import LombScargle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mpld3
import os

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
    label_array = []
    max_period = 0

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
        label_array.append(asteriod["ssnamenr"])

        #check if the period is greater than the max period
        if (test_period > max_period):
            max_period = test_period
        if (data_period > max_period):
            max_period = data_period

    #create comparison scatter plot
    # fig = plt.scatter(our_test_array, snapshot_test_array)
    fig, ax = plt.subplots(subplot_kw=dict(facecolor='#EEEEEE'))

    #create the scatter plot to hold all cards
    scatter = ax.scatter(our_test_array, snapshot_test_array)
    ax.set_title('Comparison of Asteroid Periods')
    ax.set_xlabel('Our Test Periods')
    ax.set_ylabel('Snapshot 1 Derived Properties Periods')
    ax.set_xlim(0, int(max_period)+10)
    ax.set_ylim(0, int(max_period)+10)
    ax.grid(True)


    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=label_array)
    mpld3.plugins.connect(fig, tooltip)

    # Save the figure as an HTML file
    mpld3.save_html(fig, "scatter_plot.html")
        
    
    print("Our test periods size: ", len(our_test_array))
    print("Snapshot 1 derived properties periods size: ", len(snapshot_test_array))


    

