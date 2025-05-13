

from pymongo import MongoClient
from astropy.timeseries import LombScargle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

uri = "mongodb://group5:IelC3eVkLz%2BMfPlGAKel4g%3D%3D@cmp4818.computers.nau.edu:27018"
client = MongoClient(uri)

db = client["ztf"]

collection = db["snapshot 1"]

astroids = [339]



for i in astroids:
    data = collection.find({"ssnamenr": i})

    t = []
    y = []



    for item in data:
        t.append(item["jd"])
        y.append(item["H"])

 

    

    p_min = 2
    p_max = 50
    f_min = 1/p_max
    f_max = 1/p_min

    frequency = np.linspace(f_min, f_max, 1000)

    power = LombScargle(t, y).power(frequency)


    # index_of_max = np.argmax(power)

    period = [(1/i) * 2 for i in frequency]
    




    plt.plot(period, power)#, label='period', color='blue', linestyle='--')
    plt.xlim(2, 50)
    plt.title('Periodogram')
    plt.xlabel('period')
    plt.ylabel('power')
    plt.legend()
    plt.grid(True)
    plt.show()



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