"""
projekt_3.py: Third project, web scraping

author: Jakub Rubes
email: rubes.jakub@email.cz
"""
import csv
import re
import sys
#These are part of the Python Standard Library and are available immediately in any environment.

import requests
from bs4 import BeautifulSoup
#The other two are third-party libraries, installed in VE.

URL = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
#Web page we are working with.

def scrape_data(url):
    soup = requests.get(url)
    soup.encoding = "utf 8"
    return BeautifulSoup(soup.text, )