import requests
import logging
import sys
import scrapper_form
import csv

__author__ = "José Vicente"
__copyright__ = "Copyright (c) 2017 José Vicente"
__credits__ = ["José Vicente"]
__license__ = "MIT"
__version__ = "3.2.0"

''' 
The purpose of this module is to generate an adjacency list from the metro system serving the city of Madrid, capital of Spain. 
https://en.wikipedia.org/wiki/Madrid_Metro

If you run this script, it will save all metro stations in a csv file with ',' as a separator.
'''

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

'''
This methods gives information about a neighbour station
'''
def _collect_neighbour_info(station, neighbour_station, line_info, browser):
    logging.info('Retrieving travel time between %s and %s' % (station['name'], neighbour_station['name']))

    time = scrapper_form.get_travel_time_between_stations(station['name'], neighbour_station['name'], browser)

    logging.info('Travel time retrieved!')

    return {'codStop': neighbour_station['codStop'], 
            'name': neighbour_station['name'], 
            'line': line_info['shortDescription'], 
            'colorLine': line_info['colorLine'],
            'time': 'NA' if time == -1 else str(time)}    


'''
Returns a dictionary with Metro lines info
'''
def get_lines():
    metro_lines_response = requests.get('http://www.crtm.es/widgets/api/GetLines.php?mode=4')

    metro_response = metro_lines_response.json()

    codLines = {}

    for line in metro_response['lines']['Line']:
        codLines[line['codLine']] = {
                                     'shortDescription': line['shortDescription'], #Line number/short name
                                     'colorLine': line['colorLine']
                                    }    

    return codLines

''' 
The adjacency list is return as a dictionary:

{'name_of_station': [list_of_neighbour_stations]}
'''
def generate_stations_adjacency_list(lines):
    stations_adjacency_list = {}

    logging.info('A Web Browser window will open. Don\'t be scared! It will be closed automatically')
    browser = scrapper_form.get_browser()

    for key, value in lines.items():
        codLine = key

        logging.info('Processing line %s' % codLine)

        line_stations_response = requests.get('http://www.crtm.es/widgets/api/GetLinesInformation.php?activeItinerary=1&codLine=%s' % codLine)

        stations_response = line_stations_response.json()

        stations_in_line = stations_response['lines']['LineInformation']['itinerary']['Itinerary'][0]['stops']['StopInformation']

        for i in range(0, len(stations_in_line)):
            station = {'codStop': stations_in_line[i]['codStop'], 
                       'name': stations_in_line[i]['name']}

            if station['name'] not in stations_adjacency_list:
                stations_adjacency_list[station['name']] = []

            if i > 0:
                prev_station = stations_in_line[i-1]

                prev_station_obj = _collect_neighbour_info(station, prev_station, value, browser)

                if prev_station_obj['name'] not in stations_adjacency_list[station['name']]:
                    stations_adjacency_list[station['name']].append(prev_station_obj)    

            if i < len(stations_in_line) - 1:
                next_station = stations_in_line[i+1]

                next_station_obj = _collect_neighbour_info(station, next_station, value, browser)

                if next_station_obj['name'] not in stations_adjacency_list[station['name']]:
                    stations_adjacency_list[station['name']].append(next_station_obj) 

    scrapper_form.close_browser(browser)

    return stations_adjacency_list

''' 
It stores every pair of stations and its info in a csv file
'''
def save_adjacency_list_as_csv(adjacency_list, separator=',', output_csv_path='metro.csv'):
    header = ['v1', 'v2', 'edge_name', 'edge_color', 'travel_seconds']

    with open(output_csv_path, 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, dialect='excel', lineterminator='\n', fieldnames=header)

        writer.writeheader()

        for k, v in adjacency_list.items():
            adjacent_nodes = v

            for node in adjacent_nodes:
                row = {
                    header[0]: k,
                    header[1]: node['name'],
                    header[2]: node['line'],
                    header[3]: node['colorLine'],
                    header[4]: node['time']
                }

                writer.writerow(row)


if __name__ == '__main__':
    metro_lines_response = requests.get('http://www.crtm.es/widgets/api/GetLines.php?mode=4')

    metro_response = metro_lines_response.json()

    lines = get_lines()

    stations_adjacency_list = generate_stations_adjacency_list(lines)

    save_adjacency_list_as_csv(stations_adjacency_list)



