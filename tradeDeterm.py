# -*- coding: utf-8 -*-
"""
Created on Sat May 22 23:07:19 2021

@author: NtRdeMtrX (nucweacia94fine)
"""
"""

[Importing and Using Example]

from tradeDeterm import tradeDeterm

trade_determ, *_= tradeDeterm() # Default date is today().date().
print(f"Trade or not: {trade_determ}")

trade_determ, *_= tradeDeterm(datetime.date(2021,1,5))
print(f"Trade or not: {trade_determ}")


"""


import os
import urllib
import requests

import datetime
from datetime import timedelta

import numpy as np
import pandas as pd

def holiday_CSV_download(DL_year_AC: int = None):
    if DL_year_AC == None:
        DL_year_AC = datetime.datetime.now().year
    DL_year = DL_year_AC - 1911
    DL_directory = './Holiday_Schedule_Download/'
    DL_filename = "holidaySchedule_" + str(DL_year) + ".csv"
    DL_path = DL_directory + DL_filename
    # 檢查目錄是否存在 
    if os.path.exists(DL_directory):
        # print(f"The directory \"{DL_directory}\" is already exist.")
        pass
    else:
        print(f"The directory is not exist. Create directory \"{DL_directory}\"")
        os.makedirs(DL_directory)
    
    if os.path.exists(DL_path):
        # print(f"The file \"{DL_filename}\" is already exist.")
        pass
    else:
        DL_url = "https://www.twse.com.tw/holidaySchedule/holidaySchedule?response=csv&queryYear=" + str(DL_year)
        
        
        if requests.get(DL_url).status_code >= 400:
            print(requests.get(DL_url))
        else:
            print(f"Downloading {DL_filename} ....")
            urllib.request.urlretrieve(DL_url, DL_path)
    return DL_path

def date_range(start:datetime ,stop:datetime ,step:timedelta):
    while start < stop :        
        yield start
        start += step
        
        
def holiday_list_gen(CSV_path: str, gen_year_AC:int = None):
    if gen_year_AC == None:
        gen_year_AC = datetime.datetime.now().year  
    
    if os.path.exists(CSV_path):        
        DF_temp = pd.read_csv(CSV_path, encoding=("big5"), header=1).iloc[:,:2]
        dict_temp = {}
        for i in range(DF_temp.shape[0]):
            str_temp = DF_temp.iloc[i,1].split("日")[:-1]
            # print(str_temp)
            for j in range(len(str_temp)):
                dict_temp[str_temp[j] + "日"] = DF_temp.iloc[i,0]
        # print(dict_temp)            
        
        issue_list = tuple(dict_temp.values())
        date_list_temp = tuple(dict_temp.keys())
        # print(date_list_temp)
        date_list = [ datetime.datetime.strptime(date, "%m月%d日").replace(year=gen_year_AC).date() for date in date_list_temp ]
        # print(date_list)
        holiday_index = []
        for i in range(len(issue_list)):
            if not issue_list[i] in ("國曆新年開始交易日","農曆春節前最後交易日","農曆春節後開始交易日"):
                holiday_index += [i]
                
        # print(holiday_index) 
        lunar_NY_strat = date_list[issue_list.index("農曆春節前最後交易日")] + timedelta(days=1)
        lunar_NY_stop = date_list[issue_list.index("農曆春節後開始交易日")]
        # print(lunar_NY_strat, lunar_NY_stop)   
         
        
        holiday_list1 = set( np.array(date_list)[holiday_index] )
        holiday_list2 = { d for d in date_range(lunar_NY_strat,lunar_NY_stop,timedelta(days=1)) }
        # print(holiday_list1)
        # print(holiday_list2)
        # print(len(holiday_list2))
        # holiday_list2 = { for }
        
        holiday_list = holiday_list1 | holiday_list2
        
        return holiday_list
    else:
        print(f"The path is not exist.")
        return None
    
def tradeDeterm(date_in = None):
    if date_in == None:
        date_in = datetime.datetime.today().date()
    year_AC = date_in.year     
    CSV_path = holiday_CSV_download(year_AC)
    holiday_list = holiday_list_gen(CSV_path, year_AC)
    # print(holiday_list)
    if date_in.weekday() in (5, 6) or date_in in holiday_list: # weekday() output is 0~6
        print(f"{date_in} is the holiday. Market Closed.")
        return False, CSV_path, holiday_list
    else:
        print(f"{date_in} is the trading day. Market open!")
        return True, CSV_path, holiday_list
    

def trading_day_calendar(gen_year_AC:int = None):
    if gen_year_AC == None:
        gen_year_AC = datetime.datetime.now().year    
    Trade_or_not = {}
    for d in date_range(datetime.date(gen_year_AC,1,1), datetime.date(gen_year_AC+1,1,1), timedelta(days=1)):
        if d.day == 1:
            if d.month > 1:
                for i in range(31-len(temp)):
                    temp += [np.nan]
                Trade_or_not[d.month-2] = temp
            temp = []            
        temp += [tradeDeterm(d)[0]]
    else:
        for i in range(31-len(temp)):
                    temp += [np.nan]
        Trade_or_not[d.month-1] = temp
        
    
    DF_calendar = pd.DataFrame(Trade_or_not, index=range(1,32))
    return DF_calendar


"""
"""
if __name__ == "__main__":
    # CSV_path = holiday_CSV_download()
    # holiday_list = holiday_list_gen(CSV_path)
    trade_determ, *_= tradeDeterm(datetime.date(2021,1,5))
    # trade_detem, CSV_path, holiday_list= tradeDeterm(datetime.date(2021,1,4))
    print(f"Trade or not: {trade_determ}")
    
    day_list = ((1,1), (1,4), (12,31), (2,5), (2,6), (2,16), (2,17), (4,1), (4,2), (4,5), (4,6), (10,11), (6,14), (3,1), (9,20))
    ans_list = (False, True, False, True, False, False, True, True, False, False, True, False, False, False, False)
    for i in range(len(ans_list)):
        # print(day_list[i])
        # print(ans_list[i])
        trade_determ = tradeDeterm(datetime.date(2021,day_list[i][0],day_list[i][1]))[0]
        assert trade_determ == ans_list[i]
    assert tradeDeterm()[0] == False
    assert tradeDeterm(datetime.date(2020,1,2))[0] == True
    assert tradeDeterm(datetime.date(2019,1,4))[0] == True
    
    DF_calendar = trading_day_calendar()
    
