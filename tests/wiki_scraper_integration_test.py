from engine.scraper import Scraper
local_file_path_rocket = 'strona.html'
local_file_path_table = 'types.html'



if __name__ == "__main__":
    scraper = Scraper(True, local_file_path=local_file_path_rocket)
    scraper.summary()
    assert(scraper.data.title.text.split()[0] == 'Team')
    text_len = len(scraper.data.title.text.split())
    assert(scraper.data.title.text.split()[text_len - 1] == 'encyclopedia')
    print("Integration test passed")




