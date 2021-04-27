# -*- coding: utf-8 -*-


def event_cb(resp_code: int, event_code: int, info: str, event: str):
    global event_dict, record_filename
    event_dict = {
        'resp_code': resp_code,
        'event_code': event_code,
        'info': info,
        'event': event        
    }
    print(f'Response Code: {resp_code} | Event code: {event_code} | Info: {info} | Event: {event}')
    f_rcd.close()
    
api.quote.set_event_callback(event_cb)
error_event_code = [1, 2, 3, 4, 5, 8, 9]


if isexist('event_dict') and event_dict['event_code'] in error_event_code:
    print("{:^100}".format(f"##########  Reinitialize \"Shioaji\"  ##########"))
    api = sj.Shioaji()
    print("{:^100}".format(f"##########  Login  ##########"))
    api.login(
        person_id, 
        passwd,  
        contracts_cb = lambda security_type: print(f"{repr(security_type)} fetch done.")
        #contracts_timeout=10000,
        #contracts_cb=print,
    )

    ca_resp = api.activate_ca(
        ca_path="C:/ekey/551/" + person_id + "/S/Sinopac.pfx",
        ca_passwd=person_id,
        person_id=person_id,
    )
    print(f"CA activatie: {ca_resp}")

    api.quote.set_event_callback(event_cb)
    api.quote.set_quote_callback(quote_cb)
    api.set_order_callback(place_cb)               
                