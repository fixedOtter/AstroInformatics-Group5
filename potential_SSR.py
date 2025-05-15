
from pymongo import MongoClient

# uri = "mongodb://group5:IelC3eVkLz%2BMfPlGAKel4g%3D%3D@cmp4818.computers.nau.edu:27018"
# client = MongoClient(uri)

#select the database
# db = client["ztf"]

# select the collection
# collection = db["snapshot 2"]





def check_for_SSR(output_array):
    #Empty container for adding 
    Potential_SSR= []
    
    for item in output_array: 
    
        ssr = item["ssnamenr"]
        period = item["period"]

        if  1000 <= period <= 5000: 

            Potential_SSR.append(output_array)
    print(Potential_SSR)

            Potential_SSR.append({"ssnamenr": ssr, "period": period})
    # print(Potential_SSR)

    return Potential_SSR


                  


check_for_SSR(output_array)



