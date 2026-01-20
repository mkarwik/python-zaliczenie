from engine.scraper import Scraper
from bs4 import BeautifulSoup
wiki_url = 'https://bulbapedia.bulbagarden.net/wiki/'
phrase = 'Team Rocket'
local_file_path = 'strona.html'


scraper_local = Scraper(True, local_file_path=local_file_path)
scraper_local.analyze_relative_freq('article',5,True, 'wykres.png')