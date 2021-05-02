# -*- coding: utf-8 -*-

"""
###### Expired_Date Generator
#Expired_Date = [15, 19, 18, 15, 20, 17, 15, 19, 16, 21, 18, 16] # 2020 A.C.
#Expired_Date = [20, 17, 17, 21, 19, 16, 21, 18, 15, 20, 17, 15] # 2021 A.C.

"""

import datetime
import numpy as np
DT = datetime.datetime.now()

#this_year = DT.year
def expired_date_gen(this_year): 
    M_1st_weekday = []
    for M in range(1,13):
        M_1st_date = datetime.datetime(this_year,M, 1, 0, 0, 0).date()
        M_1st_weekday.append(M_1st_date.weekday())
    M_1st_weekday = np.array(M_1st_weekday, dtype = int)
    Expired_Date = ( (2-M_1st_weekday) %7 + 15 ).tolist()
    Expired_Date.append(this_year)

    M_1st_weekday_word = str((M_1st_weekday+1).tolist())
    M_1st_weekday_word = M_1st_weekday_word.replace("1","Mon(1)").replace("2","Tue(2)")
    M_1st_weekday_word = M_1st_weekday_word.replace("3","Wed(3)").replace("4","Thu(4)")
    M_1st_weekday_word = M_1st_weekday_word.replace("5","Fri(5)").replace("6","Sat(6)").replace("7","Sun(7)")
    print("")
    print(f"This year is {this_year} A.C.")
    print(f"1st weekday in every month: {M_1st_weekday_word}")
    print(f"Expired date in every month: {Expired_Date[:-1]}")
    print("")
    
    return Expired_Date
Expired_Date = expired_date_gen(DT.year)