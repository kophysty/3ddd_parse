
import json
import time
import os
from datetime import datetime

    
try:
    import json_save
    import parse2
except Exception as exc:
    print(exc)
    list_json = os.listdir(path='dates/')

    with open(f'dates/{len(list_json) - 1}.json') as file:
        data = json.load(file)
        l_js = data['list']
        if(len(l_js) == 0):
            os.remove(f'dates/{len(list_json) - 1}.json')
            if(os.path.isfile(f'{datetime.now().strftime("%d.%m.%y")}.csv')):
                os.remove(f'{datetime.now().strftime("%d.%m.%y")}.csv')

time.sleep(30)
