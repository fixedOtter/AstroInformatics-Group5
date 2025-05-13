# whats being pulled in
from pymongo import MongoClient
from astropy.timeseries import LombScargle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# defining things
uri = "mongodb://group5:IelC3eVkLz%2BMfPlGAKel4g%3D%3D@cmp4818.computers.nau.edu:27018"
client = MongoClient(uri)

# db = client["ztf"]
# collection = db["snapshot 1"]

astroids = [15481]



for i in astroids:
    # getting the asteroids from the collection
    data = client["ztf"]["snapshot 1"].find({"ssnamenr": i})

    # creating arrays for the 
    #   julian date (t for time)
    #   magnitude (y)
    #   uncertainty (dy)
    t = []
    y = []
    dy = []

    # subract initial value and muliply by 24

    # pushing data to the arrays
    for item in data:
        t.append(float(item["jd"]))
        y.append(float(item["H"]))
        dy.append(item["sigmapsf"])

    minVal = min(t)

    for i in range(len(t)):
        t[i] = (float(t[i])-minVal)*24

      
    # translating the period to the frequency
    p_min = 1
    p_max = 50
    f_min = 1/p_max
    f_max = 1/p_min
    frequency = np.linspace(f_min, f_max, 1000000)

    # calculating the L-S with the t and y points and the frequency
    power = LombScargle(t, y, dy).power(frequency)

    # then putting from frequency back to period - multiplying by two because mike said
    period = [(1/i) * 2 for i in frequency]
    
    # then plotting the data
    plt.plot(period, power)#, label='period', color='blue', linestyle='--')
    plt.xlim(1, 50)
    plt.title('Periodogram')
    plt.xlabel('period')
    plt.ylabel('power')
    # plt.legend()
    plt.grid(True)
    plt.show()




    # DO WE NEED!?? I DONT KNOW

    # index_of_max = np.argmax(power)

    # max_frequency = frequency[index_of_max]
    # max_power = power[index_of_max]
    # print("Max Frequency: ", max_frequency)
    # print("Max Power: ", max_power)

    # print("Frequency: ", frequency)
    # print("Power: ", power)

    # max_index = power.index(max(power))

    # print("Frequency: ", frequency[max_index])
    # print("Power: ", power[max_index])

# time: jd
# absolute magnitude: H_br
# magnitude: H
# Julian Date: jd
# 