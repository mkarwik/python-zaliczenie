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
            response = requests.get(self.wiki_url)
            if response.ok:
                html_file = requests.get(self.wiki_url).text
            else:
                # now we can be sure that if Scraper exists, it has properly loaded webpage
                raise ValueError(f"Artykuł '{self.phrase}' nie istnieje na wiki.")

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



    def summary(self):
        content_div = self.data.find('div', class_='mw-content-ltr')
        if content_div is not None:
            first_paragraph = content_div.find('p')

            if first_paragraph is not None:
                text = first_paragraph.get_text(strip=True)
                print(text)
            else:
                print("No paragraph has been found")
        else:
            print("No text container has been found")


