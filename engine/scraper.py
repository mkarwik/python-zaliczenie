from bs4 import BeautifulSoup
import requests

class Scraper:
    def get_url(self):
        if self.use_local_file_instead:
            return

        self.phrase = self.phrase.replace(" ", "_")
        self.wiki_url = self.wiki_url + self.phrase

    def scrape(self):
        html_file = None
        if self.use_local_file_instead:
            try:
                with open(self.local_file_path, 'r') as file:
                    html_file = file.read()
            except FileNotFoundError:
                print("File to open has not been found!")

        else:
            html_file = requests.get(self.wiki_url).text

        soup = BeautifulSoup(html_file, 'html.parser')
        self.data = soup


    def __init__(self, use_local_file_instead, wiki_url=None, phrase=None, local_file_path=None):
        self.wiki_url = wiki_url
        self.phrase = phrase
        self.use_local_file_instead = use_local_file_instead
        self.local_file_path = local_file_path
        self.data = None

        self.get_url()
        self.scrape()



