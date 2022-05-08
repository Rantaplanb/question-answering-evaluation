import os, sys
sys.path.append(os.path.dirname(os.path.abspath('../utils')))

import utils.translator
import translators as ts
import time


greek_text = "Με λένε βαγγέλη και σπουδάζω επιστήμη υπολογιστών στο Ηράκλειο."

def request_bing_translation(input, src, dest):
    nap_time = 3
    exception_counter = 0
    exception_total_counter = 0
    while(True):
        try:
            if exception_total_counter > 100:
                print("Reached 100 exceptions sleeping for 2 minutes...")
                time.sleep(120)
                exception_total_counter = 0
            print(ts.bing(input, from_language=src, to_language=dest))
            exception_counter = 0
            nap_time = 3
        except Exception as e:
            if(exception_counter > 5):
                nap_time += nap_time
            exception_counter += 1
            exception_total_counter += 1
            print("An exception occured: ", e)
            print("Sleeping for ", nap_time, ", exceptions happend: ", exception_counter)
            time.sleep(nap_time)