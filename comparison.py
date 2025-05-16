
from pymongo import MongoClient
from astropy.timeseries import LombScargle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mpld3
import os
from concurrent.futures import ProcessPoolExecutor

#connect to the database
uri = "mongodb://group5:IelC3eVkLz%2BMfPlGAKel4g%3D%3D@cmp4818.computers.nau.edu:27018"
client = MongoClient(uri)

#select the database
db = client["ztf"]

#select the collection
collection = db["snapshot_1_derived_properties"]


#compare asteriods we tested with others
def compare_ssnamenr_asteriod_periods(test_ssnamenr_array, output_diagram = False, slice_block = 0, snapshot = "1"):

    #create arrays
    our_test_array = []
    snapshot_test_array = []
    label_array = []
    max_period = 0

    collection = db[f"snapshot_{snapshot}_derived_properties"]

    #loop through data to test
    for asteriod in test_ssnamenr_array:
        #find associated data
        data = collection.find_one({"ssnamenr": str(asteriod["ssnamenr"])})
        
        #check if data was in snapshot_1_derived_properties collecetion
        if (data == None):
            continue
        
        #get the periods of the test data
        test_period = float(asteriod["period"])

        data_period = 0
        if (snapshot == "1"):
            data_period = float(data["rotper"])
        elif (snapshot == "2"):
            data_period_test = data["periods"]["periods"]
            min_chi2 = 1000000
            for period in data_period_test:
                if (period["chi2"] < min_chi2):
                    min_chi2 = period["chi2"]
                    data_period = float(period["period"])

        #add test periods to output arrays
        our_test_array.append(test_period)
        snapshot_test_array.append(data_period)
        label_array.append(asteriod["ssnamenr"])

        #check if the period is greater than the max period
        if (test_period > max_period):
            max_period = test_period
        if (data_period > max_period):
            max_period = data_period

    print("Our test periods size: ", len(our_test_array))
    print(f"Snapshot {snapshot} derived properties periods size: ", len(snapshot_test_array))
    
    #check if user wants output diagrams produced
    if (output_diagram == False):
        return our_test_array, snapshot_test_array, label_array
    
    #create comparison scatter plot
    # fig = plt.scatter(our_test_array, snapshot_test_array)
    fig, ax = plt.subplots(subplot_kw=dict(facecolor='#EEEEEE'))

    #create the scatter plot to hold all cards
    scatter = ax.scatter(our_test_array, snapshot_test_array)
    ax.set_title('Comparison of Asteroid Periods')
    ax.set_xlabel('Our Test Periods')
    ax.set_ylabel(f'Snapshot {snapshot} Derived Properties Periods')
    ax.set_xlim(1, int(max_period)+10)
    ax.set_ylim(1, int(max_period)+10)
    ax.grid(True)

    #create labels for the points
    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=label_array)
    mpld3.plugins.connect(fig, tooltip)

    # Save the figure as an HTML file with linear scale
    mpld3.save_html(fig, f"data/program_output/scatter_plot_snapshot_{snapshot}_linear_scale.html")

    #change to log scale
    ax.set_xlim(1, int(max_period)+1000)
    ax.set_ylim(1, int(max_period)+1000)
    ax.set_xscale('log')
    ax.set_yscale('log')

    #output the log scale of graph
    fig.savefig(f"data/program_output/scatter_plot_{snapshot}_log_scale.png")

    return our_test_array, snapshot_test_array, label_array


#create comparison graph using given arrays instead of pulling from database
def create_comparison_graph(our_test_array, snapshot_test_array, max_period, label_array, snapshot = "1"):
    #create comparison scatter plot
    # fig = plt.scatter(our_test_array, snapshot_test_array)
    fig, ax = plt.subplots(subplot_kw=dict(facecolor='#EEEEEE'))

    #create the scatter plot to hold all cards
    scatter = ax.scatter(our_test_array, snapshot_test_array, s=1)
    ax.set_title('Comparison of Asteroid Periods')
    ax.set_xlabel('Our Test Periods')
    ax.set_ylabel(f'Snapshot {snapshot} Derived Properties Periods')
    ax.set_xlim(1, int(max_period)+10)
    ax.set_ylim(1, int(max_period)+10)
    ax.grid(True)

    #create labels for the points
    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=label_array)
    mpld3.plugins.connect(fig, tooltip)

    # Save the figure as an HTML file
    mpld3.save_html(fig, f"data/program_output/scatter_plot_snapshot_{snapshot}_linear_scale.html")

    ax.set_xlim(1, int(max_period)+1000)
    ax.set_ylim(1, int(max_period)+1000)
    ax.set_xscale('log')
    ax.set_yscale('log')

    fig.savefig(f"data/program_output/scatter_plot_{snapshot}_log_scale.png")


def read_test_array_file(file_name):
    # Read the file and return the contents
    with open(file_name, "r") as file:
        lines = file.readlines()

    for i in range(len(lines)):
        # Remove the newline character from each line
        lines[i] = lines[i].strip().split()

    del lines[0]  # Remove the first line of labels
    return lines

if (__name__ == "__main__"):
    snapshot = "1"
    ##
    # file path format
    # {source_dicrectory}\data\monsoon output\attempt{index}\test_arrays.txt
    ##

    #get current directory
    directory = f"{os.getcwd()}\\data\\monsoon output"
    print(f"Current working directory: {directory}")

    files_out = []

    for index in range(0, 14):
        files_out.append(f"{directory}\\attempt{index}\\test_arrays.txt")

    print(f"Files out: {files_out[0]}")

    # Number of CPUs to use for parallel processing
    num_cpus = 4

    # Create a list to store the lines from all files
    lines = []

    with ProcessPoolExecutor(num_cpus) as pool:
        # call the function for each item concurrently
        for result in pool.map(read_test_array_file, files_out):
            lines = lines + result

    #set up arrays to hold the data
    our_test_array = []
    snapshot_test_array = []
    label_array = []
    max_period = 0

    #loop through data and combine the arrays
    for i in range(1,len(lines)):
        our_test_array.append(float(lines[i][1]))
        snapshot_test_array.append(float(lines[i][2]))
        label_array.append(int(lines[i][0]))

        if (float(lines[i][1]) > max_period):
            max_period = float(lines[i][1])
        if (float(lines[i][2]) > max_period):
            max_period = float(lines[i][2])
    
    #create the comparison graph
    create_comparison_graph(our_test_array, snapshot_test_array, max_period, label_array, snapshot)



    

    
    



