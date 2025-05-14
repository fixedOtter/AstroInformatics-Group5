# whats being pulled in
from pymongo import MongoClient
from astropy.timeseries import LombScargle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



#function to get the ssnamenr and period for a given list of asteroids
def get_ssr_candidate_ssnamenr_and_period(asteriods_ssnamenr, collection):


    out_array = []
    #if no asteroids are given, return all asteroids
    if (asteriods_ssnamenr == None):
        #get the first 50 asteroids in the collection
        test_asteroids = collection.find({}).limit(50)
        #if no asteroids are given, return all asteroids
        
        #get the period and power array for the asteroid
        for test_asteroid in test_asteroids:
            power_array, period_array, _ = get_period_and_power_array(ssnamenr=test_asteroid["ssnamenr"], collection=collection)
        
            #find the max power and period
            max_power_index = np.argmax(power_array)
            max_period = period_array[max_power_index]

            #add the max period with the associated ssnamenr to the output array
            out_array.append({"ssnamenr": test_asteroid["ssnamenr"], "period": float(max_period)})
            print("Fully calculated period for ssnamenr: ", test_asteroid["ssnamenr"])


    else:

        #loop through each asteroid in the list
        for ssnamenr in asteriods_ssnamenr:
            #get the period and power array for the asteroid
            power_array, period_array, _ = get_period_and_power_array(ssnamenr, collection=collection)
            
            #find the max power and period
            max_power_index = np.argmax(power_array)
            max_period = period_array[max_power_index]


            #add the max period with the associated ssnamenr to the output array
            out_array.append({"ssnamenr": ssnamenr, "period": float(max_period)})
            print("Fully calculated period for ssnamenr: ", ssnamenr)


    #return the out_array
    return out_array

#returns the period and power array for a given ssnamenr
def get_period_and_power_array(ssnamenr, collection):
    #get all data associated with asteroid
    data = collection.find({"ssnamenr": ssnamenr})

    #initialize
    t_times_green = []
    y_magnitudes_green = []
    t_times_red = []
    y_magnitudes_red = []

    #add data to lists
        #jd is julian data
        #H is absolute magnitude
    for item in data:
        if (item["fid"] == 1):
            t_times_green.append(float(item["jd"]))
            y_magnitudes_green.append(float(item["H"]))
        elif (item["fid"] == 2):
            t_times_red.append(float(item["jd"]))
            y_magnitudes_red.append(float(item["H"]))

    #find mean difference between the two filters
    #this is used to normalize the data
    mean_diff = np.mean(y_magnitudes_green) - np.mean(y_magnitudes_red)

    #set the combined t_times and y_magnitudes
    t_times = t_times_green
    y_magnitudes = y_magnitudes_green

    #add the red filter data to the combined data with the modified magnitudes
    for i in range(len(y_magnitudes_red)):
        y_magnitudes_red[i] += mean_diff
        t_times.append(t_times_red[i])
        y_magnitudes.append(y_magnitudes_red[i])

    #find smallest time
    small_time = min(t_times)

    #subtract the smallest time from all times
    #this is done to make the times start at 0
    for i in range(len(t_times)):
        #convert to float
        t_times[i] = (float(t_times[i]) - small_time) * 24

    #calculate frequency min and max from period min and max
    p_min = .0416
    p_max = 416.66
    f_min = 1/p_max
    f_max = 1/p_min

    #sets frequency range and spread
    frequency = np.linspace(f_min, f_max, 1000000)

    #calculate power using LobScargle
    power = LombScargle(t_times, y_magnitudes).power(frequency)

    #set period array(multiply by 2 to get full rotation)
    period = [(1/i) * 2 for i in frequency]

    #return power array and period array
    return power, period, frequency

def createPlot(ssnamenr, db, max_period = -1):
    #get the period and power array for a given ssnamenr
    power, period, _ = get_period_and_power_array(ssnamenr, db)

    #find the max power and period
    plt.plot(period, power)
    plt.xlim(2, 50)
    plt.title(f'Periodogram {ssnamenr}')
    plt.xlabel('period')
    plt.ylabel('power')
    # plt.legend()
    plt.grid(True)

    #plot the max period if it is not -1
    if max_period != -1:
        plt.axvline(max_period, color='red', linestyle='--', label=f'Max Period: {max_period:.2f}')
    
    plt.show()

if __name__ == "__main__":
    #connect to the database
    uri = "mongodb://group5:IelC3eVkLz%2BMfPlGAKel4g%3D%3D@cmp4818.computers.nau.edu:27018"
    client = MongoClient(uri)

    #select the database
    db = client["ztf"]

    #select the collection
    collection = db["snapshot 1"]

    astroids = [12345]#,685, 243]

    #get the period and power array for each asteroid
    out_array = get_ssr_candidate_ssnamenr_and_period(astroids, collection)

    print(out_array)
    createPlot(astroids[0], db, out_array[0]["period"])

