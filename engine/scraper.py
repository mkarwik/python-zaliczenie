from bs4 import BeautifulSoup
import requests
from collections import Counter
import pandas as pd
import numpy as np
import os
import json
import time
from collections import deque
import matplotlib.pyplot as plt
import wordfreq as wfq
from operator import itemgetter


def is_a_wiki_link(href):
    if href.startswith('/wiki/') and ':' not in href:
        return True
    return False

class Scraper:
    def get_url(self):
        if self.use_local_file_instead:
            return

        self.phrase = self.phrase.replace(" ", "_")
        self.article_url = self.wiki_url + self.phrase

    def scrape(self):
        html_file = None
        if self.use_local_file_instead:
            try:
                with open(self.local_file_path, 'r') as file:
                    html_file = file.read()
            except:
                print("File to open has not been found!")
                return

        else:
            response = requests.get(self.article_url)
            if response.ok:
                html_file = requests.get(self.article_url).text
            else:
                # now we can be sure that if Scraper exists, it has properly loaded webpage
                print(f"Artykuł '{self.phrase}' nie istnieje na wiki.")
                return

        soup = BeautifulSoup(html_file, 'html.parser')
        self.data = soup


    def __init__(self, use_local_file_instead=False, wiki_url=None, phrase=None, local_file_path=None):
        self.wiki_url = wiki_url
        self.article_url = wiki_url
        self.phrase = phrase
        self.use_local_file_instead = use_local_file_instead
        self.local_file_path = local_file_path
        self.data = None

        if phrase or use_local_file_instead:
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

    def table(self, n, first_row_is_header=False):
        table_n = int(n)
        tables = self.data.find_all('table')
        if not tables:
            print("Na stronie nie znaleziono żadnej tabeli.")
            return

        if table_n > len(tables):
            print("Nie ma tyle tabel na stronie")
            return

        table = tables[table_n - 1]

        # zbuduj listę wierszy jako list list tekstów komórek
        rows = table.find_all('tr')
        parsed_rows = []
        for tr in rows:
            cells = tr.find_all(['th', 'td'])
            row_texts = [cell.get_text(strip=True) for cell in cells]
            if row_texts:
                parsed_rows.append(row_texts)

        # wykrywanie, czy pierwszy wiersz jest nagłówkiem
        has_thead = table.find('thead') is not None
        use_header = first_row_is_header or has_thead

        # Ujednolicenie długości wierszy
        max_cols = max(len(r) for r in parsed_rows)
        for r in parsed_rows:
            if len(r) < max_cols:
                r.extend([''] * (max_cols - len(r)))

        if use_header:
            headers = parsed_rows[0]
            data_rows = parsed_rows[1:]

            if len(headers) < max_cols:
                headers = headers + [f"col_{i}" for i in range(len(headers) + 1, max_cols + 1)]
            df = pd.DataFrame(data_rows, columns=headers)

        else:
            cols = [f"col_{i}" for i in range(1, max_cols + 1)]
            df = pd.DataFrame([r for r in parsed_rows], columns=cols)

        filename = f"{self.phrase}.csv"
        df.to_csv(filename)

        flat_values = df.reset_index().values.flatten()
        flat_filtered = [str(v).strip() for v in flat_values if v is not None and str(v).strip() != ""]
        if flat_filtered:
            counts = pd.Series(flat_filtered).value_counts()
            print("\nWystąpienia wartości (bez pustych komórek i bez nagłówków):")
            print(counts.to_string())
        else:
            print("\nBrak wartości do zliczenia (wszystkie komórki były puste).")
        return

    def count_words(self):
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_file_path)
        json_path = os.path.join(project_root, 'word-counts.json')

        content_div = self.data.find('div', class_='mw-content-ltr')
        if content_div is None:
            print("Nie znaleziono treści artykułu.")
            return
        text = content_div.get_text(" ", strip=True)
        words = text.lower().split()

        current_counts = Counter(words)

        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as file:
                total_counts = Counter(json.load(file))
        else:
            total_counts = Counter()

        total_counts.update(current_counts)

        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(total_counts, file)

        print(f"Liczba unikalnych słów w tym artykule: {len(current_counts)}")

    def analyze_relative_freq(self, mode, n_words,  chart,  file_dir):
        #self.count_words()
        n = int(n_words)
        with open('word-counts.json', 'r') as plik:
            article_freq = json.load(plik)
            article_length = sum(article_freq.values())

        if mode == "language":
            top_words = wfq.top_n_list('en', n, 'small', False)
            words_in_lang = [article_length * wfq.word_frequency(top_word, 'en') for top_word in top_words]
            words_in_article = [article_freq.get(top_word, 0) for top_word in top_words]

            df = pd.DataFrame({
                "Słowo" : top_words,
                "Częstosliwość w języku" : words_in_lang,
                "Częstosliwość w Wiki" : words_in_article,
            })
            print(df)
            if chart:
                bar_width = 0.3

                # Ustaw pozycję słupka na osi X
                r1 = np.arange(len(words_in_lang))
                r2 = [x + bar_width for x in r1]

                # Narysuj słupki dla obu grup
                plt.bar(r1, words_in_lang, color='blue', width=bar_width, edgecolor='grey', label='Słowa w j. angielskim')
                plt.bar(r2, words_in_article, color='red', width=bar_width, edgecolor='grey', label='Słowa w Wiki')

                # Dodaj etykiety, tytuł i legendę
                plt.xlabel('Słowa', fontweight='bold')
                plt.xticks([r + 0.5 * bar_width for r in range(len(words_in_lang))], top_words)
                plt.ylabel('Wystąpienia')
                plt.title('Porównanie wystąpień słów ')
                plt.legend()
                if file_dir:
                    plt.savefig(file_dir)
                plt.show()

        elif mode == 'article':
            article_sorted = dict(Counter(article_freq).most_common(n))
            words = article_sorted.keys()

            words_article_freq = article_sorted.values()
            words_language_freq = [article_length * wfq.word_frequency(word, 'en', 'small') for word in words]

            df = pd.DataFrame({
                "Słowo": words,
                "Częstosliwość w języku": words_language_freq,
                "Częstosliwość w Wiki": words_article_freq,
            })
            print(df)

            if chart:
                bar_width = 0.3
                r1 = np.arange(len(words_article_freq))
                r2 = [x + bar_width for x in r1]

                # Narysuj słupki dla obu grup
                plt.bar(r1, words_language_freq, color='blue', width=bar_width, edgecolor='grey', label='Słowa w j. angielskim')
                plt.bar(r2, words_article_freq, color='red', width=bar_width, edgecolor='grey', label='Słowa w Wiki')

                # Dodaj etykiety, tytuł i legendę
                plt.xlabel('Słowa', fontweight='bold')
                plt.xticks([r + 0.5 * bar_width for r in range(len(words_language_freq))], words)
                plt.ylabel('Wystąpienia')
                plt.title('Porównanie wystąpień słów ')
                plt.legend()
                if file_dir:
                    plt.savefig(file_dir)
                plt.show()

    def auto_count_words(self, initial_phrase, max_depth_str, wait_time_str):

        queue = deque([(initial_phrase, 0)])
        visited = {initial_phrase}
        max_depth = int(max_depth_str)
        wait_time = int(wait_time_str)

        while queue:
            current_phrase, current_depth = queue.popleft()
            print(f"Przetwarzanie frazy: {current_phrase}")

            new_scraper = Scraper(False, self.wiki_url, current_phrase)
            if new_scraper.data is None:
                print("Nie udało się pobrać danych. Wykonywanie count-words przerwano")
                return
            new_scraper.count_words()

            if current_depth < max_depth:
                content_div = new_scraper.data.find('div', class_='mw-content-ltr')
                if content_div is not None:
                    links = content_div.find_all('a', href=True)

                    #search by BFS
                    for link in links:
                        href = link['href']
                        if is_a_wiki_link(href):
                            next_phrase = href.replace('/wiki/', '')
                            if next_phrase not in visited:
                                visited.add(next_phrase)
                                queue.append((next_phrase, current_depth + 1))
                time.sleep(wait_time)
            else:
                return