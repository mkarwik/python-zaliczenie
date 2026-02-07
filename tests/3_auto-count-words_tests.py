from engine.scraper import Scraper
from bs4 import BeautifulSoup
import os
import json
from collections import Counter
wiki_url = 'https://bulbapedia.bulbagarden.net/wiki/'
phrase = 'Team Rocket'


current_file_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_file_path)
json_path = os.path.join(project_root, 'word-counts.json')


def test_auto_word_count():
    if os.path.exists(json_path):
        os.remove(json_path)

    scraper_online = Scraper(False, wiki_url, phrase)
    scraper_online.auto_count_words(phrase, 0, 2)

    if not os.path.exists(json_path):
        print("Nie udało się wygenerować pliku")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)
        total_counts = Counter(data)
        assert len(total_counts) > 10
        print("Test passed")


def test_costam():
    file_path = os.path.join(project_root, 'polski.html')
    scraper_local = Scraper(use_local_file_instead=True, local_file_path=file_path)
    scraper_local.count_words()
