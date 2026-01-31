from engine.scraper import Scraper
local_file_path_rocket = 'strona.html'
local_file_path_table = 'types.html'



if __name__ == "__main__":
    scraper = Scraper(True, local_file_path=local_file_path_rocket)
    scraper.summary()
    scraper.analyze_relative_freq('article',5,True, 'wykres.png')
    scraper.count_words()

    table_scraper = Scraper(True, local_file_path=local_file_path_table)
    table_scraper.table(1)




