from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re
import time

browser = webdriver.Chrome() 

browser.get('https://www.metromadrid.es/es/viaja_en_metro/trayecto_recomendado/index.html') 

time.sleep(0.5)
for option in browser.find_element_by_name('idOrigen').find_elements_by_tag_name('option'):
    if option.get_attribute('value') == '625':
        option.click()
        break

time.sleep(0.5)
for option in browser.find_element_by_name('idDestino').find_elements_by_tag_name('option'):
    if option.get_attribute('value') == '37':
        option.click()
        break

date = browser.find_element_by_name('fechBuscar')
date.clear()
date.send_keys('2017/01/30')

browser.find_element_by_name('buscar').click()

time.sleep(1)
try:
    travel_time = browser.find_element_by_xpath('//*[@id="contenido"]/div[1]/ul/li[1]/div/div/dl/dt[3]/strong').text

    browser.close()

    times = re.findall('Tiempo Estimado: (\d+) h. (\d+) min. (\d+) sg.', travel_time)[0]

    hours = int(times[0])
    mins = int(times[1])
    segs = int(times[2])

    total_time = hours*3600 + mins*60 + segs
except NoSuchElementException:
    travel_time = -1

print(total_time)


