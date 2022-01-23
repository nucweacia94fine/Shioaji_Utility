# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 19:26:07 2021

@author: NtRdeMtrX
"""
"""
[Importing and Using Example]

from stock_code_name_corresp_check import stock_code_name_corresp_check
from stock_code_name_corresp_check import code_name_list_read

print(stock_code_name_corresp_check("2330"))
print(stock_code_name_corresp_check("兆豐金"))
print(stock_code_name_corresp_check("123"))
print(code_name_list_read())


"""

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as BtfS

#### List Generator
def code_name_list_gen():
    code_name_dict = {"Code": [], "Name": [], "Market": []}
    for mode in [2,4,5]:
    # for mode in [2]:
        print(f"List mode: {mode}")
        req_url = f"https://isin.twse.com.tw/isin/C_public.jsp?strMode={mode}"
        response = requests.get(req_url)
            
        # response.encoding = 'gb2312' # 簡
        # response.encoding = 'big5' # 繁
        # response.encoding = 'gbk' # 簡繁
        # response.encoding = 'gb18030' # 簡繁        
        response.encoding = 'ms950' # 繁
        # print(response.text[0:3000])
        soup = BtfS(response.text, 'lxml')      # soup = BtfS(response.text, 'html.parser')
        soup_filter1 = soup.find('table', {'class': 'h4'})
        df_soup_filter1 = pd.read_html(soup_filter1.prettify(), header=0)[0]
        row_filter = np.where(df_soup_filter1['有價證券代號及名稱'] != df_soup_filter1['上市日'])[0]
        df_code_name = df_soup_filter1.iloc[row_filter,:]['有價證券代號及名稱']
        df_market = df_soup_filter1.iloc[row_filter,:]['市場別']
        for code_name in df_code_name:
            if " " in code_name:
                code_name_split = code_name.split(" ")
            elif "\u3000" in code_name:
                code_name_split = code_name.split("\u3000")                
            # if len(code_name_split) !=2:
            #     print(code_name)
            #     print(code_name_split)
            #     break
            code_name_dict["Code"] += [code_name_split[0]]
            code_name_dict["Name"] += [code_name_split[1]]
        # print(code_name_dict)
        for market in df_market:
            code_name_dict["Market"] += [market]
    DF_code_name_dict = pd.DataFrame(code_name_dict)
    # DF_code_name.sort_values(by=["Code"])
    return DF_code_name_dict

#### List Read
def code_name_list_read(update=False):
    DT = datetime.date.today()
    filename = f"Stock_code_name_list_{DT.year}{DT.month:02}.csv"
    if not os.path.isfile(filename) or update:                
        DF_code_name = code_name_list_gen()
        DF_code_name.to_csv(filename, index=False, encoding="utf-8")
    else:
        DF_code_name = pd.read_csv(filename)
    return DF_code_name
    
#### List Check 
import os
import datetime


def stock_code_name_corresp_check(input_str:str, update=False):
    DT = datetime.date.today()
    filename = f"Stock_code_name_list_{DT.year}{DT.month:02}.csv"
    if not os.path.isfile(filename) or update:                
        DF_code_name = code_name_list_gen()
        DF_code_name.to_csv(filename, index=False, encoding="utf-8")
    else:
        DF_code_name = pd.read_csv(filename)
    
    if input_str.isdigit():
        if len(np.where(DF_code_name["Code"] == input_str)[0]) != 0:
            return DF_code_name.loc[DF_code_name["Code"] == input_str].iloc[0,1]
        else:
            return None
    else:        
        if len(np.where(DF_code_name["Name"] == input_str)[0]) != 0:
            return DF_code_name.loc[DF_code_name["Name"] == input_str].iloc[0,0]
        else:
            return None

if __name__ == "__main__":
    print(stock_code_name_corresp_check("2330"))
    print(stock_code_name_corresp_check("兆豐金"))
    print(stock_code_name_corresp_check("123"))
    print(code_name_list_read())