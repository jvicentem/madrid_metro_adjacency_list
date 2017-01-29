from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re
import time
import unicodedata
import random

''' 
This module aims to get travel times between stations using Selenium and Chrome Webdriver.
'''

''' 
This is the most important method of this module. The time between stations is 
given in seconds.

FAQ: 

Why do you need a browser as an argument?:

Because it's very reasonable to have only one browser object and use it
over and over again in order not to open and close lots of Chrome windows
every time this function is called.


Why do you add time.sleeps?
Sometimes the site is slow and it's not loaded yet. If we don't wait some time
Selenium will raise an exception claiming it wasn't able to find the wanted element.


Why do you randomize the time in those time.sleeps?
I do this in order to avoid being detected as a bot. The server might block our requests.


Why do you clean all cookies every time this function is called?
Read the previous question answer.


Why do you the date is 2017/01/30 at 12:00?
Okay, this is very important. If you take a look at the calendary, January 30 falls on Monday, that is
a weekday. The metro is slower during the weekend. However, the metro is faster on the first hours of the day and 
is slower at the end of the day.

In order to get normal times (we don't want fast ones nor slow ones) the date is set on a Monday at 12:00 PM.
'''
def get_travel_time_between_stations(origin_name, destination_name, browser):
    browser.delete_all_cookies()

    browser.get('https://www.metromadrid.es/es/viaja_en_metro/trayecto_recomendado/index.html') 

    origin_name = _normalize_string(origin_name).upper()
    destination_name = _normalize_string(destination_name).upper()

    try:
        time.sleep(0.5 + random.random())
        for option in browser.find_element_by_name('idOrigen').find_elements_by_tag_name('option'):
            if _normalize_string(option.text).upper() == origin_name:            
                option.click()
                break

        for option in browser.find_element_by_name('idDestino').find_elements_by_tag_name('option'):      
            if _normalize_string(option.text).upper() == destination_name:
                option.click()
                break

        date = browser.find_element_by_name('fechBuscar')
        date.clear()
        date.send_keys('2017/01/30')

        for option in browser.find_element_by_name('cmbHora').find_elements_by_tag_name('option'):
            if option.get_attribute('value') == '12':
                option.click()
                break

        browser.find_element_by_name('buscar').click()

        time.sleep(1 + random.random())

        travel_time = browser.find_element_by_xpath('//*[@id="contenido"]/div[1]/ul/li[1]/div/div/dl/dt[3]/strong').text

        times = re.findall('Tiempo Estimado: (\d+) h. (\d+) min. (\d+) sg.', travel_time)[0]

        hours = int(times[0])
        mins = int(times[1])
        segs = int(times[2])

        total_time = hours*3600 + mins*60 + segs
    except NoSuchElementException:
        total_time = -1

    return total_time

def get_browser():
    return webdriver.Chrome()

def close_browser(browser):
    browser.close()

''' 
This function is necessary in order to compare the station names on the site and
those received as arguments in get_travel_time_between_stations function
'''
def _normalize_string(string):
    pre_clean = string.strip().replace('-', '').replace(' ', '').replace('AVDA.', 'AVENIDA')

    return (''.join((c for c in unicodedata.normalize('NFD', pre_clean) if unicodedata.category(c) != 'Mn')))


