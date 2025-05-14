from pymongo import MongoClient

uri = "mongodb://group5:IelC3eVkLz%2BMfPlGAKel4g%3D%3D@cmp4818.computers.nau.edu:27018"
client = MongoClient(uri)

#select the database
db = client["ztf"]

#select the collection
collection = db["snapshot 2"]



def check_for_SSR(asteroids_potentials):
    
    Potential_SSR= []
    
    for item in asteroids_potentials: 
    
        test_ssr = item["ssnamenr"]
        test_period = item["period"]

        if  1000 <= test_period <= 5000: 
            Potential_SSR.append(test_ssr)
    print(Potential_SSR)
    return Potential_SSR
# list_asteroids = [{"ssnamenr": "500", "period":2000}, {"ssnamenr": "700", "period":776}, {"ssnamenr": "1000", "period":4444}]
                  


check_for_SSR()

    
