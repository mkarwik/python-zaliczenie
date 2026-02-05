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
    scraper_online.auto_count_words(phrase, 1, 2)

    with open(json_path, 'r') as f:
        data = json.load(f)
        total_counts = Counter(data)
        assert len(total_counts) > 10
