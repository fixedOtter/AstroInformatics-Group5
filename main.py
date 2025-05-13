# made by coolest team on 05.12.2025

# def things
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# constants of integration
uri = "mongodb://group5:IelC3eVkLz%2BMfPlGAKel4g%3D%3D@cmp4818.computers.nau.edu:27018"
client = MongoClient(uri)

foundObject = 339

#function to print the graph
def printGraph(objectNum):
  data = pd.DataFrame(client["ztf"]["snapshot 1"].find({"ssnamenr": str(objectNum)}))
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
  fig.savefig('graph_' + str(i) + '.png')

printGraph(foundObject)

client.close()