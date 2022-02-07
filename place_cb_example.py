# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 20:27:47 2022

@author: NtRdeMtrX (nucweacia94fine)
"""
"""

[Information]
Titile: An example of Shioaji place callback with queue structure
Contract example: 小型臺指MXF
Requirement: 
    login.py (from nucweacia94fine)
    getpass (from pip)

"""

##################################################################################################################
########################################    Initialize and Login    ##############################################

import numpy as np
import datetime
from dateutil.relativedelta import relativedelta # for timedelta with no months 


record_filename = "Trading_Record_test.text"

import login
person_id, passwd, api = login.login()


# In[] 
##################################################################################################################
############################################    Contract Setting    ##############################################

###### Expired_Date Generator
#Expired_Date = [15, 19, 18, 15, 20, 17, 15, 19, 16, 21, 18, 16] # 2020 A.C.
#Expired_Date = [20, 17, 17, 21, 19, 16, 21, 18, 15, 20, 17, 15] # 2021 A.C.

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

###### Serialize(pickle) the api.Contracts
# import pickle
# filename_pkl = f"Serialized_Contracts_{DT.year}{DT.month:02d}.pkl"
# if ( not os.path.isfile(filename_pkl) ) or ( DT.day == Expired_Date[DT.month-1]+1 ):
#     f_pkl = open(filename_pkl, 'wb')
#     pickle.dump(api.Contracts.Futures, f_pkl)
#     f_pkl.close()


###### Subscribe and Contract Code Generator
def future_code_gen(api, DT, Expired_Date, future_type):    
    DT_next = DT + relativedelta(months=1)
    if DT.day > Expired_Date[DT.month-1]:
        code = future_type + chr(ord('A')+ DT_next.month-1) + str(DT_next.year % 10)
    elif DT.day == Expired_Date[DT.month-1]:
        if DT.hour >= 5:
            code = future_type + chr(ord('A')+ DT_next.month-1) + str(DT_next.year % 10)
        else:
            code = future_type + chr(ord('A')+ DT.month-1) + str(DT.year % 10)
    else:
        code = future_type + chr(ord('A')+ DT.month-1) + str(DT.year % 10)
        
    contract = api.Contracts.Futures[code]
    api.quote.subscribe(contract, quote_type='tick')
    update_datetime = datetime.datetime.strptime(contract.update_date, "%Y/%m/%d").date()
    return code, contract, update_datetime

fut_code, contract_mxf, update_datetime = future_code_gen(api, DT, Expired_Date, "MXF")
print(fut_code, contract_mxf, update_datetime)

# In[] 
##################################################################################################################
############################################    Callback Setting    ##############################################

order_cb_queue = []
def place_cb(stat, msg):
    global order_cb_queue   
    T_order_cb = datetime.datetime.now()
    print('\n|| Order Callback ||')
    order_cb_queue += [{"stat": stat, "msg": msg, "time": T_order_cb}]  # Save as dictionary    
    # order_cb_queue += [(stat, msg, T_order_cb)]                       # Save as tuple

api.set_order_callback(place_cb)

   
def order_cb_read(order_list=None, deal_list=None):
    global order_cb_queue, record_filename, T_order, trade_fut
    
    order_cb_temp = order_cb_queue.pop(0)
#### Read callback as dictionary
    stat = order_cb_temp["stat"]
    msg = order_cb_temp["msg"]
    T_order_cb = order_cb_temp["time"]
#### Read callback as tuple
    # stat = order_cb_temp[0]
    # msg = order_cb_temp[1]
    # T_order_cb = order_cb_temp[2]
    
    """
    [Orderstate type]
    "TFTOrder": sj.constant.OrderState.TFTOrder     (現股委託)
    "TFTDeal": sj.constant.OrderState.TFTDeal       (現股成交)
    "FOrder": sj.constant.OrderState.FOrder         (期貨委託)
    "FDeal": sj.constant.OrderState.FDeal           (期貨成交)
    "Order": sj.constant.OrderState.Order           (其餘委託)
    "Deal": sj.constant.OrderState.Deal             (其餘成交)            
    """
    
    f_rcd = open(record_filename, "a", encoding='utf-8')    
    if stat == "FORDER":        # sj.constant.OrderState.FOrder --> <OrderState.FOrder: 'FORDER'>
        if "trade_fut" in globals() and msg['order']['id'] == trade_fut.order.id:
            print(f"{T_order_cb} | Order Time Offset: {T_order_cb - T_order}\n")
            print(f"{stat}\n{msg}")
            order_cb_state = stat
            order_message = msg
            
            print('\n|| Order Callback ||', file = f_rcd)
            print(f"{T_order_cb} | Order Time Offset: {T_order_cb - T_order}\n", file = f_rcd)
            print(order_cb_state, file = f_rcd)
            #print("Operation:", file = f_rcd)
            #print(str(order_message.get('operation',"Not Found")).replace(", ", ",\n"), file = f_rcd)
            print("Contract:", file = f_rcd)
            print(str(order_message.get('contract',"Not Found")).replace(", ", ",\n"), file = f_rcd)
            print("Order:", file = f_rcd)
            print(str(order_message.get('order',"Not Found")).replace(", ", ",\n"), file = f_rcd)
            print("Status:", file = f_rcd)
            print(str(order_message.get('status',"Not Found")).replace(", ", ",\n"), file = f_rcd)
            
            order_list.append(order_message)

    elif stat == "FDEAL":       # sj.constant.OrderState.FDeal --> <OrderState.FDeal: 'FDEAL'>
        if "trade_fut" in globals() and msg['trade_id'] == trade_fut.order.id:
            print(f"{T_order_cb} | Order Time Offset: {T_order_cb - T_order}\n")
            print(f"{stat}\n{msg}")
            deal_cb_state = stat
            deal_message = msg
            
            print('\n|| Order Callback ||', file = f_rcd)
            print(f"{T_order_cb} | Order Time Offset: {T_order_cb - T_order}\n", file = f_rcd)
            print(deal_cb_state, file = f_rcd)
            print(str(deal_message).replace(", ", ",\n"), file = f_rcd)
            if len(deal_list) == 0:
                deal_list.append(deal_message)
            elif deal_message['exchange_seq'] != deal_list[-1]['exchange_seq']:
                deal_list.append(deal_message)
    print('', file = f_rcd)
    f_rcd.close()
    return order_list, deal_list

# In[]
##################################################################################################################
#########################################    Main Function Example    ############################################
order_list = []
deal_list = []       # Save dealed list for profit calculation
if not "trade_fut_last" in globals():
    trade_fut_last = None
def main(test_mode = False): # True False
    global api, contract_mxf, order_cb_queue, record_filename, T_order, order_list, deal_list, trade_fut, trade_fut_last
        
    T_last = datetime.datetime.now()
    while True:
    #### Main function block (Testing order)
        T_now = datetime.datetime.now()
        if test_mode:
            option = input("\"O\" for Order. \"E\" for exit. Any key for continue:")
            if option.upper() == "O":
                T_order = datetime.datetime.now()
                ### Test order
                order = api.Order(action="Buy",
                                  price=1,
                                  quantity=1,
                                  order_type="ROD",          ## {ROD, IOC, FOK}
                                  price_type="LMT",          ## {LMT, MKT, MKP} (限價、市價、範圍市價)
                                  octype="Cover",             ## {Auto, New, Cover, DayTrade} 
                                                              ## (自動、新倉、平倉、當沖)
                                  account=api.futopt_account)
                trade_fut = api.place_order(contract_mxf, order)
            elif option.upper() == "E":
                break
        else:
            if T_now.second != T_last.second and T_now.second % 10 == 0:
                # print(T_now - T_last)
                T_order = datetime.datetime.now()
                ### Test order
                order = api.Order(action="Buy",
                                  price=1,
                                  quantity=1,
                                  order_type="ROD",          ## {ROD, IOC, FOK}
                                  price_type="LMT",          ## {LMT, MKT, MKP} (限價、市價、範圍市價)
                                  octype="Cover",             ## {Auto, New, Cover, DayTrade} 
                                                              ## (自動、新倉、平倉、當沖)
                                  account=api.futopt_account)
                trade_fut = api.place_order(contract_mxf, order, timeout=0)
    #### End of main function block
    
    #### Read the callback queue with while loop
        if "trade_fut" in globals() and trade_fut_last != trade_fut:
            T_read1 = datetime.datetime.now()
            while len(order_cb_queue) > 0:
                order_list, deal_list = order_cb_read(order_list, deal_list)                    
            #### Only queue out for 1ms in 1 funtion loop.
                T_read2 = datetime.datetime.now()
                if T_read2-T_read1 >= datetime.timedelta(microseconds=1000):
                    print((T_read2-T_read1).microseconds)
                    break
            ###### End of queue reading loop.    
            if len(order_cb_queue) == 0:
                print("Order callback is empty.")
                trade_fut_last = trade_fut
                # break
        
        T_last = T_now
    ###### End of main function loop.
        
    
if __name__=="__main__":
    main()
