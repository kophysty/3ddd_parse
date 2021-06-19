import json
from datetime import datetime
import parse2
import analitic
import os

list_json = os.listdir(path='dates/')

list_json.reverse()

print(list_json)

date_now = datetime.now().strftime('%d.%m.%y')

list_before = []

trs = parse2.trs_dict

def json_clear(trs): 
    if(len(list_json) != 0):
        with open(f'dates/{len(list_json)-1}.json') as file:
            data = json.load(file)
            l_js = data['list']
            json_dates = {'f_date': l_js[0]['data'], 'l_date': l_js[-1]['data']}
            index_clear = [0, len(trs)]
            clear = {'clear': False}
            j = 0
        # while j < len(trs):
        #     if(trs[j]['data'] == json_dates['f_date']):
        #         index_clear[0] = j
        #         clear['clear'] = True
        #     j+=1
        # j = 0
            while j < len(trs):
                if(trs[j]['data'] == json_dates['f_date']):
                    index_clear[0] = j
                    clear['clear'] = True
                j+=1
            
            if(clear['clear'] == True):
                del trs[index_clear[0]:(index_clear[-1])]

json_clear(trs)

if(len(list_json) == 0):
    json_dict = {'date': date_now, 'list': parse2.trs_dict}

    with open(f'{len(list_json)}.json', 'a+') as file:
        json.dump({'date': date_now, 'list': parse2.trs_dict, 'likes': analitic.models_info['likes'], 'comments': analitic.models_info['comments']}, file, indent=3)

    os.replace(f'{len(list_json)}.json', f'dates/{len(list_json)}.json')
else: 
    for j in list_json:
        with open(f'dates/{j}') as file:
            data = json.load(file)
            l_js = data['list']
            list_before.extend(l_js)

    with open(f'{len(list_json)}.json', 'a+') as file:
        json.dump({'date': date_now, 'list': parse2.trs_dict, 'likes': analitic.models_info['likes'], 'comments': analitic.models_info['comments']}, file, indent=3)

    os.replace(f'{len(list_json)}.json', f'dates/{len(list_json)}.json')


def count_m(items):
    model_sum = [0] * len(parse2.links_text)
    model_average = []

    days_sum = len(items)

    for i in items:
        j = 0
        while j < len(i['models']):
            model_sum[j] += int(i['models'][j]['sum'])
            j+=1
    
    for m in model_sum:
        model_average.append(int(m / days_sum))

    return {'model_sum': model_sum, 'model_average': model_average, 'days_sum': days_sum}


def difference_active(jsons): 
    empty_list = [0] * len(parse2.links_text)
    model_active = {'likes': empty_list, 'comments': empty_list}
    if(len(jsons) == 0):
        j=0
        likes_dif = []
        comments_dif = []
        while j < len(parse2.links_text):
            likes_dif.append(str(int(analitic.models_info['likes'][j])) + ' ( +0)')
            comments_dif.append(str(int(analitic.models_info['comments'][j])) + ' ( +0)')
            j+=1
        model_active['likes'] = likes_dif
        model_active['comments'] = comments_dif
        return model_active
        
    else: 
        with open(f'dates/{(len(jsons)-1)}.json') as file:
            data = json.load(file)
            likes_b = data['likes']
            comments_b = data['comments']
            
            likes_dif = []
            comments_dif = []

            j=0
            while j < len(likes_b):

                likes_dif.append(str(int(analitic.models_info['likes'][j])) + f' ( +{str(int(analitic.models_info["likes"][j]) - int(likes_b[j]))})')
                comments_dif.append(str(int(analitic.models_info['comments'][j])) + f' ( +{str(int(analitic.models_info["comments"][j]) - int(comments_b[j]))})')

                j+=1
            
            model_active['likes'] = likes_dif
            model_active['comments'] = comments_dif
    return model_active

dif_active = 'delete'

count_models = count_m(parse2.trs_dict + list_before)

dif_active = difference_active(list_json)

parse2.make_csv(parse2.trs_dict, list_before, f'{date_now}.csv', parse2.money_average('https://3ddd.ru/user/sell_rating', count_models))

if(len(trs) == 0):
    os.remove(f'dates/{len(list_json)}.json')
