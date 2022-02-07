# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:24:12 2022

@author: NtRdeMtrX (nucweacia94fine)
"""
"""

[Information]
Titile: An example of pickling the shioaji contracts.
Pickling example: Whole Contracts Objects
Requirement: 
    login.py (from nucweacia94fine)
    getpass (from pip)

"""

import pickle
import login

###### Login 1st
person_id, passwd, api = login.login()

###### Use str to force the program to wait until fetching completed
str(api.Contracts)

###### Serialize(pickle) the api.Contracts
filename_pkl = "Serialize_test.pkl"

print(f"Serializing the contracts to \"{filename_pkl}\"...")
f_pkl = open(filename_pkl, 'wb')
pickle.dump(api.Contracts, f_pkl)
f_pkl.close()

# In[] 
###### Contract Test
temp_1 = 0
for layer_1 in api.Contracts.keys():
    print(f"<< {layer_1} >>")
    temp_2 = 0
    for layer_2 in api.Contracts[layer_1].keys():
        temp_3 = 0
        for layer_3 in api.Contracts[layer_1][layer_2].keys():            
            temp_3 += 1
        print(f"{layer_2}: {temp_3}", end=" | ")
        temp_2 += temp_3
    print()
    temp_1 += temp_2
print("... for loop done ...")
print(f"Total Contrants Number: {temp_1}")
    
contract1 = api.Contracts.Stocks["2330"]
print()
print(contract1)
contract2 = api.Contracts.Futures["MXFB2"]
print()
print(contract2)

# In[] 
###### Logout
print("=== Logout. ===")
api.logout()

###### Delete Variable
del api, contract1, contract2

# In[] 
###### Login Again
*_, api = login.login(person_id=person_id,
                      passwd=passwd,
                      fetch_contract=False)

###### Load the api.Contracts
print(f"Loading the contracts from \"{filename_pkl}\"...")
f_pkl = open(filename_pkl, 'rb')
api.Contracts = pickle.load(f_pkl)
f_pkl.close()

# In[] 
###### Contract Test
temp_1 = 0
for layer_1 in api.Contracts.keys():
    print(f"<< {layer_1} >>")
    temp_2 = 0
    for layer_2 in api.Contracts[layer_1].keys():
        temp_3 = 0
        for layer_3 in api.Contracts[layer_1][layer_2].keys():            
            temp_3 += 1
        print(f"{layer_2}: {temp_3}", end=" | ")
        temp_2 += temp_3
    print()
    temp_1 += temp_2
print("... for loop done ...")
print(f"Total Contrants Number: {temp_1}")
    
contract1 = api.Contracts.Stocks["2330"]
print()
print(contract1)
contract2 = api.Contracts.Futures["MXFB2"]
print()
print(contract2)

###### Logout
print("=== Logout. ===")
api.logout()
