from engine.scraper import Scraper
import pytest
import os

wiki_url = 'https://bulbapedia.bulbagarden.net/wiki/'
phrase = 'Team Rocket'
current_dir = os.path.dirname(os.path.abspath(__file__))
local_file_path = os.path.join(current_dir, 'strona.html')

# Test checks if downloading article was successful
def test_online_scraping():
    scraper_online = Scraper(False, wiki_url, phrase)
    assert(scraper_online.data.title.text == 'Team Rocket - Bulbapedia, the community-driven Pokémon encyclopedia')

def test_local_scraping():
    scraper_local = Scraper(True, local_file_path=local_file_path)
    assert (scraper_local.data.title.text == 'Team Rocket - Bulbapedia, the community-driven Pokémon encyclopedia')

