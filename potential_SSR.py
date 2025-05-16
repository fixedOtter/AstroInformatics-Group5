
##
# This script checks for potential SSRs in the output array
# using a basic criteria of period between 1000 and 5000, can be 
# modified to include more complex criteria if needed.
##
def check_for_SSR(output_array):
    #Empty array for adding 
    Potential_SSR= []
    
    #Iterate through the output array and check for SSRs
    for item in output_array: 
    
        #get the ssnamenr and period from the item
        ssr = item["ssnamenr"]
        period = item["period"]

        #check if the period is between 1000 and 5000
        if  1000 <= period <= 5000: 

            # Potential_SSR.append(output_array)
            Potential_SSR.append({"ssnamenr": ssr, "period": period})
    
    return Potential_SSR


