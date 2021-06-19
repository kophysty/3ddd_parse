import login as l
import analitic as a
import json_save
import json

from bs4 import BeautifulSoup
import copy
import csv
import os
# from datetime import datetime
import datetime

date_now = datetime.datetime.now().strftime('%d.%m.%y')
url_table = 'https://3ddd.ru/user/income_new'
url_module = 'https://3ddd.ru/user/sell_rating'

def get_count_page(url):
    html_file = l.session.get(url).text
    soup = BeautifulSoup(html_file, "html.parser")
    count_text = soup.find('div', attrs={'class': 'count'}).text
    count = str() # Check words in string
    
    for c in count_text:
        if c.isdigit():
            count += c
    return int(count)

def table_url(url): # Parse income table
    trs = []
    pages_count = get_count_page(url)
    for page in range(1, pages_count + 1):
        # print(f'Парсинг страницы {page} из {pages_count}...')
        html = l.session.get(url, params={'page': page}).text
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find('tbody')
        trs_one = table.find_all('tr')
        trs.extend(trs_one)
    return trs

trs = table_url(url_table)

def module_parse(url): # Read module info
    html_file2 = l.session.get(url).text
    soup2 = BeautifulSoup(html_file2, "html.parser")
    table_sell = soup2.find('tbody')
    links = table_sell.find_all('a')
    links_text = []
    for link in links:
        links_text.append(link.text.replace('\n', '').strip())
    return links_text

links_text = module_parse(url_module)


def default_array(links): # Make default models array

    def_array = []
    for m in links:
        def_array.append({
            'name': m,
            'sum': 0, 
            'multi': 0
        })
    return def_array

def_array = default_array(links_text)

def trs_dicts(trs_write):
    dict_info = [] # All dicts tr

    for tr in trs_write: # Run to all trs
        tds = tr.find_all('td') # Finding tds in tr
        date_in = tds[0].text #find date
        model = tds[1].text #find model
        money = tds[2].text #find money

        b = str() # Check words in string
        for c in money:
            if c == ' ':
                money = b
                break
            if c.isdigit() or c == '.':
                b += c

    
        date_have = {'nohave': True}

        i = 0
        j = 0

        while i < len(dict_info):
            if(dict_info[i]['data'] == date_in): 
                date_have['nohave'] = False
                while j < len(dict_info[i]['models']):
                    if(dict_info[i]['models'][j]['name'] == model):
                        dict_info[i]['models'][j]['sum'] += float(money)
                        dict_info[i]['models'][j]['multi'] += 1
                    j+=1
            i+=1

        if(date_have['nohave'] == True):
            dict_tr = {
                'data': date_in,
                'models': copy.deepcopy(def_array)
            }

            for d in dict_tr['models']:
                if(d['name'] == model):
                    d['sum'] += float(money)
                    d['multi'] += 1
            
            dict_info.append(dict_tr)

    return dict_info

trs_dict = trs_dicts(trs)

trs_dict_nt = trs_dicts(trs)

def money_average(url, model_sum): # Find money_average
    html_file = l.session.get(url).text
    soup = BeautifulSoup(html_file, "html.parser")
    table_sell = soup.find('tbody')
    trs = table_sell.find_all('tr')
    model_m = {'model_sells': [], 'money_average': [], 'sum_day': [], 'total_sells': [], 'grand_total': [0]}
    for s in trs:
        model_m['model_sells'].append(int(s.find_all('td')[2].text))
    
    html_file2 = l.session.get('https://3ddd.ru/user/withdraw_history').text
    soup2 = BeautifulSoup(html_file2, "html.parser")
    money = soup2.find('div', attrs={'class': 'total_price'}).text
    money_int = ''

    with open('__pycache__/earlier_sells.json') as file:
        data = json.load(file)
        earlier_sells = data['earlier_sells']

        if(len(earlier_sells) == 0):
            for c in money:
                if c.isdigit() or c=='.':
                    money_int += c

            money_int = money_int[0:-1]
            
            money_int = float(money_int)
            sells_sum = 0

            for m in model_m['model_sells']: 
                sells_sum += m
            
            average_money = 0
            
            average_money = money_int / sells_sum
            
            for m in range(len(model_m['model_sells'])): 
                num = int(model_m['model_sells'][m] * average_money)

                if(num < 0):
                    model_m['money_average'].append(0)
                else:
                    model_m['money_average'].append(int(model_m['model_sells'][m] * average_money))

            with open('__pycache__/earlier_sells.json', 'w') as file:
                json.dump({'earlier_sells': model_m['money_average']}, file, indent=3)
        else: 
            model_m['money_average'] = data['earlier_sells']

        days_dif = []

        for d in range(len(a.models_info['make_data'])):

            make_date = a.models_info['make_data'][d]
            last_date = trs_dict_nt[0]

            f_date = datetime.date(int(make_date[1:5]), int(make_date[6:8]), int(make_date[9:11]))
            l_date = datetime.date(int(last_date['data'][6:10]), int(last_date['data'][3:5]), int(last_date['data'][0:2]))
            
            days = l_date - f_date
            days_str = str(days)

            days_dif.append(days_str.split()[0])
        
        for d in range(len(days_dif)):
            if(d >= len(data['earlier_sells'])):
                mon_average[d] = int((0 + int(model_sum['model_sum'][d])) / int(days_dif[d]))
                model_m['sum_day'].append(mon_average)
            else:
                mon_average = int(((int(earlier_sells[d]) + int(model_sum['model_sum'][d]))) / int(days_dif[d]))
                model_m['sum_day'].append(mon_average)
        
        for d in range(len(model_m['model_sells'])):
            if(d >= len(data['earlier_sells'])):
                model_m['total_sells'].append(0 + model_sum['model_sum'][d])
            else: 
                model_m['total_sells'].append(earlier_sells[d] + model_sum['model_sum'][d])

        for s in model_m['total_sells']:
            model_m['grand_total'][0] += int(s)

    return model_m


def make_csv(new_items, old_items, path, model_m ):
    items = new_items + old_items
    items.reverse()

    with open(path, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['names'] + links_text)
        writer.writerow(['make_data'] + a.models_info['make_data'])
        writer.writerow(['sells'] + model_m['model_sells'])
        writer.writerow(['earlier sells (average)'] + model_m['money_average'])
        
        if(json_save.dif_active != 'delete'):
            writer.writerow(['likes'] + json_save.dif_active['likes'])
            writer.writerow(['comments'] + json_save.dif_active['comments'])
        else: 
            writer.writerow(['likes'])
            writer.writerow(['comments'])
        
        writer.writerow(['render'] + a.models_info['render'])
        writer.writerow(['size'] + a.models_info['size'])
        writer.writerow(['date\/'])
        
        for item in items:
            list_write = [f" {str(item['data'])} "]
            for d in item['models']:
                list_write.append(str(d["sum"])) #f'={str(d["sum"])}+Ч(X{str(d["multi"])})'
            writer.writerow(list_write)
        
        writer.writerow([''])
        writer.writerow(['money_stat'] + json_save.count_models['model_sum'])
        writer.writerow(['money_average'] + model_m['sum_day'])
        writer.writerow([''])
        writer.writerow(['total sells'] + model_m['total_sells'])
        writer.writerow([''])
        writer.writerow(['GRAND_TOTAL'] + model_m['grand_total'])
    
    if(os.path.isfile(f'result/{date_now}.csv')):
        os.remove(f'result/{date_now}.csv')

    os.replace(f'{date_now}.csv', f'result/{date_now}.csv')
