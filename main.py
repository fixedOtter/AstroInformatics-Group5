# made by coolest team on 05.12.2025

# def things
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

import lombs_gargle_calculator as lgc
import comparison as compare

import time

import potential_SSR as pSSR

# constants of integration
uri = "mongodb://group5:IelC3eVkLz%2BMfPlGAKel4g%3D%3D@cmp4818.computers.nau.edu:27018"
client = MongoClient(uri)

foundObject = 1865


def run_comparison(slice_block):

  #test asteroids
  asteroids = []

  #select the database
  db = client["ztf"]

  #select the collection
  collection = db["snapshot_1_derived_properties"]


  #Get all test asteroids
  test_asteroids = collection.find({}).limit(1000).skip(slice_block * 1000)

  for item in test_asteroids:
    #print(item["ssnamenr"])
    asteroids.append(int(item["ssnamenr"]))
  
  lgc_time_start = time.time()

  #get output array of the periods of inputted asteroids using snapshot 1
  out_array = lgc.get_ssr_candidate_ssnamenr_and_period(asteroids)
  # print("Out array: ", out_array)

  lgc_time_end = time.time()
  lgc_time = lgc_time_end - lgc_time_start

  possible_SSRs_start = time.time()
  possible_SSRs = pSSR.check_for_SSR(out_array)
  possible_SSRs_end = time.time() - possible_SSRs_start
  
  with open("potential_SSR.txt", "w") as f:
    for ssr in possible_SSRs:
      f.write(str(ssr) + "\n")


  compare_time_start = time.time()

  #create comparison graph using snapshot_1_derived_properties
  our_test_array, snapshot_test_array, label_array = compare.compare_ssnamenr_asteriod_periods(out_array, True)

  compare_time_end = time.time()
  compare_time = compare_time_end - compare_time_start

  print("LombScargle time: ", lgc_time)
  print("Comparison time: ", compare_time)
  print("Possible SSRs time: ", possible_SSRs_end)
  print("Total time: ", lgc_time + compare_time + possible_SSRs_end)

  with open("test_arrays.txt", "w") as f:
    f.write(f"ssnamenr Our_Period Snaps_Period\n")
    for index in range(len(our_test_array)):
      f.write(f"{label_array[index]} {our_test_array[index]} {snapshot_test_array[index]}\n")

  return


#function to print the graph
def printModuloGraph(objectNum):

  cursorObj = client["ztf"]["snapshot 1"].find({"ssnamenr": objectNum})
  lenOfObj = len(list(cursorObj))

  if lenOfObj < 50: 
    print('not enough measurements')
    return

  data = pd.DataFrame(client["ztf"]["snapshot 1"].find({"ssnamenr": objectNum}))
  astData = pd.DataFrame(client["ztf"]["snapshot_1_derived_properties"].find({"ssnamenr":str(objectNum)}))
  # Create variables for colored filters
  green = data["fid"] == 1
  red = data["fid"] == 2
  #-------------------
  fig,ax = plt.subplots(3)
  fig.set_size_inches(11,9)
  fig.tight_layout(w_pad=3.5, h_pad=3.5)
  #------------------- Havg vs JD
  ax[0].scatter(data[green]["jd"], data[green]["H"], color='g')
  ax[0].scatter(data[red]["jd"], data[red]["H"], color='r')

  ax[0].errorbar(data[green]["jd"], data[green]["H"], yerr = data[green]["sigmapsf"], fmt = 'o', color='g')
  ax[0].errorbar(data[red]["jd"], data[red]["H"], yerr = data[red]["sigmapsf"], fmt = 'o', color='r')
  # Invert Magnitudes on y axis
  ax[0].invert_yaxis()
  ax[0].set_xlabel("Julian Date")
  ax[0].set_ylabel("Absolute Magnitude(H)")
  ax[0].set_title("Observations for Object")  

  #---------------------------------------------------------------------- LIGHT CURVES

  rotper = astData["rotper"][0]
  jdlinh = np.linspace(0, rotper, 10000)

  # Slope of light curve
  y =astData["havg"][0]+astData["modelFit"][0][0]+astData["modelFit"][0][1]*np.sin(2*np.pi*jdlinh/astData["rotper"][0]*2)+ astData["modelFit"][0][2]*np.cos(2*np.pi*jdlinh/astData["rotper"][0]*2)
  
  #------------------- Offset Curves
  # Light Curve Plot
  ax[1].errorbar(data[green]["jd"]*24 % astData["rotper"][0], data[green]["H"], yerr = data[green]["sigmapsf"], fmt = 'o', color='g')
  ax[1].errorbar(data[red]["jd"]*24 % astData["rotper"][0], data[red]["H"], yerr = data[red]["sigmapsf"], fmt = 'o', color='r')

  ax[1].plot(jdlinh, y, color='Gray')

  ax[1].plot(jdlinh, y + astData["grColor"][0], color='Black')
  
  # Invert Magnitudes on y axis
  ax[1].invert_yaxis()
  ax[1].set_title("Light curve")
  ax[1].set_xlabel("Phase (hours)")
  ax[1].set_ylabel("H (mag)")
  
  #------------------- Combined Curve
  
  # Light Curve Plot
  ax[2].errorbar(data[green]["jd"]*24 % astData["rotper"][0], data[green]["H"]-astData["grColor"][0], yerr = data[green]["sigmapsf"], fmt = 'o', color='g')
  ax[2].errorbar(data[red]["jd"]*24 % astData["rotper"][0], data[red]["H"], yerr = data[red]["sigmapsf"], fmt = 'o', color='r')

  ax[2].plot(jdlinh, y, color='Black')
  
  # Invert Magnitudes on y axis
  ax[2].invert_yaxis()
  ax[2].set_title("Light curve(green offset by g-r)")
  ax[2].set_xlabel("Phase (hours)")
  ax[2].set_ylabel("H (mag)")

  fig.show()
  fig.savefig('graph_' + str(objectNum) + '.png')


# main actually running stuff
# printModuloGraph(foundObject)
if (__name__ == "__main__"):
  slice_block = 0

  if (len(sys.argv) != 2):
    print("Slice number not provided, exiting")
    sys.exit(1)

  #gets the size of the slice block
  slice_block = int(sys.argv[1])

  option = "compare"

  if option == "compare":
    run_comparison(slice_block)
  elif option == "graph":
  # main actually running stuff
    printModuloGraph(foundObject)

    client.close()