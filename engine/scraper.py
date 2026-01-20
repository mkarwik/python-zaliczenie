from bs4 import BeautifulSoup
import requests
import pandas as pd


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


    def __init__(self, use_local_file_instead=False, wiki_url=None, phrase=None, local_file_path=None):
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

    def table(self, n, first_row_is_header=False):

        tables = self.data.find_all('table')
        if not tables:
            print("Na stronie nie znaleziono żadnej tabeli.")
            return

        if n > len(tables):
            print("Nie ma tyle tabel na stronie")
            return

        table = tables[n - 1]

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