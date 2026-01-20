from engine.scraper import Scraper
local_file_path = 'types.html'

scraper_local = Scraper(True, local_file_path=local_file_path)
scraper_local.table(2, False)