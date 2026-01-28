from engine.scraper import Scraper
from bs4 import BeautifulSoup
wiki_url = 'https://bulbapedia.bulbagarden.net/wiki/'
phrase = 'Team Rocket'
local_file_path = 'strona.html'


scraper_online = Scraper(False, wiki_url, phrase)
scraper_online.auto_count_words(phrase, 2, 2);