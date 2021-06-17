import requests
import json
import os

class rj_handler():

    def parse_locations(dest_url):
        return requests.get(dest_url).json()

    def get_countries(locations):
        country_list = []
        for location in locations:
            country_list.append(location['country'])
        return country_list

    def get_pairs(city_id, city_pairs_url):
        pairs = requests.get(city_pairs_url).json()
        arrival= []
        for pair in pairs:
            if(pair['departureCityId'] == city_id):
                arrival.append(pair['arrivalCityId'])
        return arrival
    
    def get_cities_all(locations):
        cities_list = []

        for country in locations:
            for city in country['cities']:    
                cities_list.append((city['id'], city['name']))
        return cities_list

    def get_route(from_dest, to_dest, date):
        route_url = "https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple?fromLocationId="+str(from_dest)+"&fromLocationType=CITY&toLocationId="+str(to_dest)+"&toLocationType=CITY&departureDate="+date+"&tariffs=CZECH_STUDENT_PASS_26"
        print(f"[DEBUG] {route_url}")
        return requests.get(route_url).json()