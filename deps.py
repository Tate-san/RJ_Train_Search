from bs4 import BeautifulSoup
import requests
import json
import math


route_url = 'https://brn-ybus-pubapi.sa.cz/restapi/routes/4908347258/simple?routeId=4908347258&fromStationId=3398241000&toStationId=372825000&tariffs=CZECH_STUDENT_PASS_26'
dest_url = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/locations'
#dest_url = 'https://www.studentagency.cz/shared/wc/ybus-form/destinations-cs.json'
possible_routes_url = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/cityPairs'

dest_list = requests.get(dest_url).json()

ids_list = []
travels = []
countries = []
stations = []
stations_id = []
tarrifs = [ [ 'REGULAR', 'CZECH_STUDENT_PASS_15', 'CZECH_STUDENT_PASS_26', 'ISIC', 'ATTENDED_CHILD', 'DISABLED', 'DISABLED_ATTENDANCE', 'EURO26', 'CHILD'],
            [ 'Dospělý 18-64 let', 'Děti a mládež 6 - <18let', 'Student <26 let (žák. průkaz/ISIC)', 'Senior >65 let', 'Doprovázené dítě <6 let', 'ZTP(ZTP/P)', 'Průvodce ZTP/P', 'ISIC >26 let/EYCA/ALIVE', 'Dítě >6-14 let (mez.autobus)', ]]


def edit_time(dt):
    dt = str(dt).split(".", -1)
    dt = dt[0].split("T", -1)
    
    return [dt[0], dt[1]]

def get_ids(url):
    routes = requests.get(url).json()
    
    for route in routes['routes']:
        if route['transfersCount'] == 0:
            ids_list.append(route['id'])

def get_trains(from_s, to_s):
    
    for id in ids_list:
        travels.append(requests.get(f'https://brn-ybus-pubapi.sa.cz/restapi/routes/{id}/simple?routeId={id}&fromStationId={from_s}&toStationId={to_s}&tariffs=CZECH_STUDENT_PASS_26').json())

            
def print_data(date):

    seatcount = []
    
    curr = requests.get('https://api.exchangeratesapi.io/latest').json()
    curr = (curr['rates']['CZK'])
    for t in travels:
        seatcount = ['0','0','0','0']
        prices = ['0','0','0','0']   
        if 'priceClasses' in t:

            for seats in t['priceClasses']:

                if 'TRAIN_LOW_COST' in seats['seatClassKey']:
                    seatcount[0] = seats['freeSeatsCount']
                    prices[0] = round(seats['price']*curr)

                if 'C0' in seats['seatClassKey']:
                    seatcount[1] = seats['freeSeatsCount']
                    prices[1] = round(seats['price']*curr)
                    
                if 'C1' in seats['seatClassKey']:
                    seatcount[2] = seats['freeSeatsCount'] 
                    prices[2] = round(seats['price']*curr)

                if 'C2' in seats['seatClassKey']:
                    seatcount[3] = seats['freeSeatsCount']
                    prices[3] = round(seats['price']*curr)
                    
                

            print( '\n __________________________________________________\n {} \n\n  {}\n\n{} -> {} | {}\n {} - {}  ->  {} - {}\n\n    {} = {}CZK   FREE SEATS {}\n    {} = {}CZK   FREE SEATS {}\n    {} = {}CZK      FREE SEATS {}\n    {} = {}CZK  FREE SEATS {}\n __________________________________________________'.format(
                t['sections'][0]['line']['code'],
                '.'.join(date),
                str((edit_time(t['sections'][0]['departureTime'])[1])).rjust(17),
                edit_time(t['sections'][0]['arrivalTime'])[1],
                t['sections'][0]['travelTime'],
                t['sections'][0]['departureCityName'],
                t['sections'][0]['departureStationName'],
                t['sections'][0]['arrivalCityName'],
                t['sections'][0]['arrivalStationName'],
                'Low cost', prices[0], seatcount[0],
                'Standart', prices[1], seatcount[1],
                'Relax', prices[2], seatcount[2],
                'Business', prices[3], seatcount[3]
                
                ))
            seatcount.clear()
            prices.clear()

def prettify(jf):
    print(json.dumps(jf, indent = 4))

        
def get_dest():
    
    try:
        # Get country list if array empty
        #if len(countries) == 0:
        #    for de in dest_list['destinations']:
        #        countries.append(de['country'])
            
        # Print countries & select
        #for i in range(len(countries)):
        #    print(i+1,') ', countries[i])
        #cis_c = input('Zadej číslo země: ')
        #sel_country = countries[int(cis_c)-1]

        # Purge and get city list
        stations.clear()
        stations_id.clear()

        for de in dest_list[11]['cities']:
            
            for stats in de['stations']:
                if stats['stationsTypes'][0] == 'TRAIN_STATION':
                    stations.append(stats['fullname'])
                    stations_id.append(stats['id'])

        

        # Print stations & select
        for i in range(len(stations)):
            print(i+1,') ', stations[i])
            
        cis_m = input('Enter city num: ')
        sel_city = stations[int(cis_m)-1]   
        sel_id = stations_id[int(cis_m)-1]

        for city in dest_list[11]['cities']:
            for stats in city['stations']:
                if stats['id'] == sel_id:
                    city_id = city['id']

        return([sel_city, sel_id, city_id])

    # If runs out of array
    except IndexError:
        print('Invalid list index')

def poss_routes(dep_city):
    possible = []
    stations.clear()
    stations_id.clear()

    pos = requests.get(possible_routes_url).json()
    for poss in pos:
        for i in range(len(poss['transportTypes'])):
            if poss['transportTypes'][i] == 'TRAIN':
                if poss['departureCityId'] == dep_city:
                    possible.append(poss['arrivalCityId'])
                    
    for poss in possible:
        for city in dest_list[11]['cities']:
            if poss == city['id']:
                for stats in city['stations']:
                    if stats['stationsTypes'][0] == 'TRAIN_STATION':
                        stations.append(city['name'] +' - '+ stats['name'])
                        stations_id.append(stats['id'])

    for i in range(len(stations)):
            print(i+1,') ', stations[i])
            
    cis = input('Enter city num: ')
    
    sel_id = stations_id[int(cis)-1]
    sel_stat = stations[int(cis)-1]   
    return [sel_stat, sel_id]

if __name__ == '__main__':
    if requests.get(route_url).status_code == 200:
        print('From: ')
        selected_from = get_dest()       
        #print(selected_from)
        #selected_from = ['Brno - Židenice', '3398241000', '10202002']
        #print(selected_from)
        print('To: ')
        selected_to = poss_routes(selected_from[2])
        #selected_to = ['','372825000'] 
        #print(selected_to)
        dep_date = (input('[DD.MM.YY] When to departure?: ')).split(".", -1)
        #dep_date = ['05','10','2019']

        for i in range(2):
            dep_date[i] = "{:02d}".format(int(dep_date[i]))
        
          
        #print(dep_date)
        
        url = (f'https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple?locale=cs&departureDate={dep_date[2]}-{dep_date[1]}-{dep_date[0]}&fromLocationId={selected_from[1]}&toLocationId={selected_to[1]}&fromLocationType=STATION&toLocationType=STATION&tariffs={tarrifs[0][2]}')
        get_ids(url)
        get_trains(selected_from[1],selected_to[1])

        # check if route exists
        print_data(dep_date)
         
    else:
        print('Page is not responding')