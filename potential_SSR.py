
def check_for_SSR(output_array):
    
    Potential_SSR= []
    
    for item in output_array: 
    
        ssr = item["ssnamenr"]
        period = item["period"]

        if  1000 <= period <= 5000: 
            Potential_SSR.append({"ssnamenr": ssr, "period": period})
    # print(Potential_SSR)
    return Potential_SSR

                  

    