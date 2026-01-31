from engine.scraper import Scraper
from bs4 import BeautifulSoup
wiki_url = 'https://bulbapedia.bulbagarden.net/wiki/'
phrase = 'Team Rocket'
local_file_path = 'strona.html'

scraper_online = Scraper(False, wiki_url, phrase)
print(scraper_online.data.prettify())

#scraper_local = Scraper(True, local_file_path=local_file_path)
#print(scraper_local.data.prettify())
