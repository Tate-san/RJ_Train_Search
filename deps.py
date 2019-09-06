from bs4 import BeautifulSoup
import requests
import json
import math


route_url = 'https://brn-ybus-pubapi.sa.cz/restapi/routes/4908347258/simple?routeId=4908347258&fromStationId=3398241000&toStationId=372825000&tariffs=CZECH_STUDENT_PASS_26'
dest_url = 'https://www.studentagency.cz/shared/wc/ybus-form/destinations-cs.json'

dest_list = requests.get(dest_url).json()

ids_list = []
travels = []
countries = []
cities = []
cities_id = []


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

            
def print_data():

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
                    
                

            print( '\n __________________________________________________\n {} \n\n   {} | {} -> {} | {}\n\n {} - {}  ->  {} - {}\n\n    Low cost = {}CZK   FREE SEATS {}\n    Standart = {}CZK   FREE SEATS {}\n    Relax = {}CZK      FREE SEATS {}\n    Business = {}CZK  FREE SEATS {}\n __________________________________________________'.format(
                t['sections'][0]['line']['code'],
                edit_time(t['sections'][0]['departureTime'])[0],
                edit_time(t['sections'][0]['departureTime'])[1],
                edit_time(t['sections'][0]['arrivalTime'])[1],
                t['sections'][0]['travelTime'],
                t['sections'][0]['departureCityName'],
                t['sections'][0]['departureStationName'],
                t['sections'][0]['arrivalCityName'],
                t['sections'][0]['arrivalStationName'],
                prices[0], seatcount[0],
                prices[1], seatcount[1],
                prices[2], seatcount[2],
                prices[3], seatcount[3]
                
                ))
            seatcount.clear()
            prices.clear()

        
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
        cities.clear()
        cities_id.clear()
        for de in dest_list['destinations'][3]['cities']:
            for stats in de['stations']:
                cities.append(stats['fullname'])
                cities_id.append(stats['id'])

        # Print cities & select
        for i in range(len(cities)):
            print(i+1,') ', cities[i])
            
        cis_m = input('Enter city num: ')
        sel_city = cities[int(cis_m)-1]   
        sel_id = cities_id[int(cis_m)-1]  
        return([sel_city, sel_id])

    # If runs out of array
    except IndexError:
        print('Invalid list index')



if __name__ == '__main__':
    if requests.get(route_url).status_code == 200:
        print('From: ')
        selected_from = get_dest()
        print('To: ')
        selected_to = get_dest()
        dep_date = (input('[DD.MM.YY] When to departure?: ')).split(".", -1)
        url = (f'https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple?locale=cs&departureDate={dep_date[2]}-{dep_date[1]}-{dep_date[0]}&fromLocationId=3398241000&toLocationId=372825000&fromLocationType=STATION&toLocationType=STATION&tariffs=REGULAR')
        get_ids(url)
        get_trains(selected_from[1],selected_to[1])
        # check if route exists
        print_data()
         
    else:
        print('Page is not responding')