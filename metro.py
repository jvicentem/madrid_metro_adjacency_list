import requests
import ujson
import logging
import sys

__author__ = "José Vicente"
__copyright__ = "Copyright (c) 2017 José Vicente"
__credits__ = ["José Vicente"]
__license__ = "MIT"
__version__ = "1.0.0"

''' 
The purpose of this module is to generate an adjacency list from the metro system serving the city of Madrid, capital of Spain. 
https://en.wikipedia.org/wiki/Madrid_Metro

If you run this script, it will save all metro stations in a csv file with ';' as a separator.
'''

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def _get_codLines():
    metro_lines_response = requests.get('http://www.crtm.es/widgets/api/GetLines.php?mode=4')

    metro_response = metro_lines_response.json()

    codLines = []

    for line in metro_response['lines']['Line']:
        codLines.append(line['codLine'])    

    return codLines

''' 
The adjacency list is return as a dictionary:

{'name_of_station': [list_of_neighbour_stations]}
'''
def generate_stations_adjacency_list(codLines):
    stations_adjacency_list = {}

    for codLine in codLines:
        logging.info('Processing line %s' % codLine)

        line_stations_response = requests.get('http://www.crtm.es/widgets/api/GetLinesInformation.php?activeItinerary=1&codLine=%s' % codLine)

        stations_response = line_stations_response.json()

        stations_in_line = stations_response['lines']['LineInformation']['itinerary']['Itinerary'][0]['stops']['StopInformation']

        for i in range(0, len(stations_in_line)):
            station = {'codStop': stations_in_line[i]['codStop'], 'name': stations_in_line[i]['name']}

            if station['name'] not in stations_adjacency_list:
                stations_adjacency_list[station['name']] = []

            if i > 0:
                prev_station = {'codStop': stations_in_line[i-1]['codStop'], 'name': stations_in_line[i-1]['name']}

                if prev_station['name'] not in stations_adjacency_list[station['name']]:
                    stations_adjacency_list[station['name']].append(prev_station['name'])    

            if i < len(stations_in_line) - 1:
                next_station = {'codStop': stations_in_line[i+1]['codStop'], 'name': stations_in_line[i+1]['name']}

                if next_station['name'] not in stations_adjacency_list[station['name']]:
                    stations_adjacency_list[station['name']].append(next_station['name']) 

    return stations_adjacency_list

def save_adjacency_list_as_csv(adjacency_list, separator=',', output_csv_path='metro.csv'):
    f = open(output_csv_path, 'w+')

    for k, v in adjacency_list.items():
        adjacent_nodes = v

        for node in adjacent_nodes:
            f.write('%s%s%s\n' % (k, separator, node))

    f.close()


if __name__ == '__main__':
    metro_lines_response = requests.get('http://www.crtm.es/widgets/api/GetLines.php?mode=4')

    metro_response = metro_lines_response.json()

    codLines = get_codLines()

    stations_adjacency_list = generate_stations_adjacency_list(codLines)              

    save_adjacency_list_as_csv(stations_adjacency_list, ';')



