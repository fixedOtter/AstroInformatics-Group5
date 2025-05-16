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


def run_comparison(slice_block, snapshot):

  #test asteroids
  asteroids = []

  #select the database
  db = client["ztf"]

  #select the collection
  collection = db[f"snapshot {snapshot}"]

  collection_der = db[f"snapshot_{snapshot}_derived_properties"]

  #Get all test asteroids
  test_asteroids = collection_der.find({}).limit(1000).skip(slice_block * 1000)

  for item in test_asteroids:
    #print(item["ssnamenr"])
    if item != None:
      asteroids.append(int(item["ssnamenr"]))
  
  lgc_time_start = time.time()

  #get output array of the periods of inputted asteroids using snapshot 1
  out_array = lgc.get_ssr_candidate_ssnamenr_and_period(asteroids, snapshot)
  # print("Out array: ", out_array)

  lgc_time_end = time.time()
  lgc_time = lgc_time_end - lgc_time_start

  #add timings
  possible_SSRs_start = time.time()
  possible_SSRs = pSSR.check_for_SSR(out_array)
  possible_SSRs_end = time.time() - possible_SSRs_start
  
  #print the possible SSRs
  with open(f"data/program_output/potential_SSR_{slice_block}.log", "w") as f:
    for ssr in possible_SSRs:
       f.write(str(ssr) + "\n")

  #add timings
  compare_time_start = time.time()

  #create comparison graph using snapshot_1_derived_properties
  our_test_array, snapshot_test_array, label_array = compare.compare_ssnamenr_asteriod_periods(out_array, True, snapshot)

  compare_time_end = time.time()
  compare_time = compare_time_end - compare_time_start

  #print out timings
  print("LombScargle time: ", lgc_time)
  print("Comparison time: ", compare_time)
  print("Possible SSRs time: ", possible_SSRs_end)
  print("Total time: ", lgc_time + compare_time + possible_SSRs_end)

  #save our periods and snapshot periods to a file
  with open(f"data/program_output/test_arrays_{slice_block}.log", "w") as f:
    f.write(f"ssnamenr Our_Period Snaps_Period\n")
    for index in range(len(our_test_array)):
      f.write(f"{label_array[index]} {our_test_array[index]} {snapshot_test_array[index]}\n")


  #save our periods and snapshot periods to a file
  with open(f"data/program_output/results_block_{slice_block}.log", "w") as f:
    f.write(f"For snapshot {snapshot}\n")
    f.write(f"For slice block {slice_block}\n")
    f.write(f"Asteroids tested: {len(asteroids)}\n")
    f.write(f"Number of possible SSR's: {len(possible_SSRs)}\n")


  return


#function to print the light curve graph
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
  snapshot = "1"

  if (len(sys.argv) != 3):
    print("Usage: python main.py <snapshot> <slice_block>")
    print("slice_block size: 1000")
    print("snapshot: 1 or 2")
    print("defaulting to slice 0")
    print("defaulting to snapshot 1")
  else:
    #gets the snapshot number
    snapshot = sys.argv[1]
    #gets the size of the slice block
    slice_block = int(sys.argv[2])

  print("Snapshot: ", snapshot)
  print("Slice Block: ", slice_block)

  option = "compare"

  if option == "compare":
    #run the comparison and periodogram code for the given slice block of a snapshot
    run_comparison(slice_block, snapshot)
  elif option == "graph":
    #object to create light curve graph for
    foundObject = 1865
    printModuloGraph(1865)

    client.close()