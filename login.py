# -*- coding: utf-8 -*-
"""
Created on Sun May 23 20:07:05 2021

@author: NtRdeMtrX
"""

import getpass
import shioaji as sj

def login(person_id = None, passwd = None, fetch_contract=True, verbose_file=None, initialized_api=None):
    if initialized_api == None:
        api = sj.Shioaji()
    else:
        api = initialized_api
    
    print("{:^100}".format(f"##########  Login  ##########"))    
    if verbose_file != None:
        try:
            print(file = verbose_file)
        except:
            print("Write file error.")
        else:            
            print("{:^100}".format(f"##########  Login  ##########"), file = verbose_file)
    if person_id == None or passwd == None:
        person_id = getpass.getpass("Personal ID:")
        passwd = getpass.getpass("Password:")
        #person_id = input("Personal ID:")
        #passwd = input("Password:")
    api.login(
        person_id, 
        passwd, 
        #hashed = False,
        #contracts_timeout=10000,
        fetch_contract = fetch_contract,
        #contracts_cb = print,
        contracts_cb = lambda security_type: print(f"{repr(security_type)} fetch done.")
    )
    
    ca_resp = api.activate_ca(
        ca_path="C:/ekey/551/" + person_id + "/S/Sinopac.pfx",
        ca_passwd=person_id,
        person_id=person_id,
    )
    print(f"CA activatie: {ca_resp}")
    if verbose_file != None:
        try:
            print(file = verbose_file)
        except:
            print("Write file error.")
        else:            
            print(f"CA activatie: {ca_resp}", file = verbose_file)
    
    fut_username = api.list_accounts()[0]['username'].replace(u'\u3000', u'')
    stock_username = api.list_accounts()[1]['username'].replace(u'\u3000', u'')
    fut_account_str = str(api.list_accounts()[0]).replace(person_id,"*****")\
                            .replace(fut_username,"***").replace('\\u3000','')
    stock_account_str = str(api.list_accounts()[1]).replace(person_id,"*****")\
                            .replace(stock_username,"***").replace('\\u3000','')
    print(f"[FutureAccount({fut_account_str}), \nStockAccount({stock_account_str})]")
    if verbose_file != None:
        try:
            print(file = verbose_file)
        except:
            print("Write file error.")
        else:            
            print(f"[FutureAccount({fut_account_str}), \nStockAccount({stock_account_str})]", file = verbose_file)
    
    return person_id, passwd, api

if __name__ == "__main__":
    person_id, passwd, api = login()

