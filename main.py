import requests
import json
import os
from rj_handler import rj_handler

locations_url = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/locations'
city_pairs_url = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/cityPairs'
seat_classes_url = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/seatClasses'
tariffs_url = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/tariffs'


# Get all locations and countries
location_list = rj_handler.parse_locations(locations_url)
countries = rj_handler.get_countries(location_list)
cities_list = rj_handler.get_cities_all(location_list)

# Write out all countries and select
for i in range(len(countries)):
    print(f"{i+1}: {countries[i]}")
print(f"Select country 1 - {len(countries)}:")


selected = 11# int(input())-1

# Get all cities from selected country
cities = location_list[selected]['cities']

# Write out all cities
for i in range(len(cities)):
    print(f"{i+1}: {cities[i]['name'] }")
print(f"Depart from 1 - {len(cities)}:")

selected = 1#int(input())-1

# save selected city id
city_id = cities[selected]['id']
print(f"[DEBUG] {cities[selected]['name']}: {city_id}")

possible_ids = rj_handler.get_pairs(city_id, city_pairs_url)

for i in range(len(possible_ids)):
    for city in cities_list:
        if(city[0] == possible_ids[i]):
            print(f"{i+1} {city}")
print(f"Arrive to:")

selected = 14#int(input())-1
test = rj_handler.get_route(city_id, possible_ids[selected], "2021-06-18")
print(test['routes'][2]['id'])
