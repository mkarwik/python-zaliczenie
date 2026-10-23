# Wiki scraper

Final project for a university Python course: a command-line tool that scrapes articles from a MediaWiki site ([Bulbapedia](https://bulbapedia.bulbagarden.net) by default) and analyses the words in them.

## What it can do

| Command | What it does |
|---|---|
| `--summary "Team Rocket"` | Prints the first paragraph of the article. |
| `--table "Type" --number 2 --first-row-is-header` | Saves the n-th table from the article to a CSV file (with pandas). |
| `--count-words "Pikachu"` | Counts words in the article and adds them to a running total in `word-counts.json`. |
| `--auto-count-words "Pikachu" --depth 2 --time 1` | Crawls the wiki breadth-first from one article, following links up to the given depth and waiting between requests, and counts words on every page. |
| `--analyze-relative-word-frequency --mode language --count 20 --chart chart.png` | Compares how often words appear in the scraped articles with how often they appear in English overall ([wordfreq](https://github.com/rspeer/wordfreq)), as a table and an optional bar chart. Mode `language` starts from the most common English words, mode `article` from the most common words in the articles. |

The notebook [`analysis/analysis.ipynb`](analysis/analysis.ipynb) uses these counts to compare word frequencies across different sets of articles (long and short English articles, a non-wiki English text, Polish and Spanish).

## Running it

```bash
pip install -r requirements.txt
cd engine
python wiki_scraper.py --summary "Team Rocket"
```

Tests (scraping from a saved page and online, argument parsing, crawling and link detection):

```bash
PYTHONPATH=. pytest tests/*.py
PYTHONPATH=. python tests/wiki_scraper_integration_test.py
```

## How it's built

- `engine/parser.py` reads the command-line arguments into a dictionary of commands.
- `engine/supervisor.py` runs each requested command.
- `engine/scraper.py` downloads and parses pages with requests and BeautifulSoup, and does the counting, crawling and analysis.

Tech: Python, requests, BeautifulSoup, pandas, NumPy, Matplotlib, wordfreq, pytest.
