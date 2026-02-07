from engine.scraper import Scraper
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
local_file_path = os.path.join(current_dir, 'strona.html')

if __name__ == "__main__":
    scraper = Scraper(True, local_file_path=local_file_path)
    scraper.summary()
    assert(scraper.data.title.text.split()[0] == 'Team')
    text_len = len(scraper.data.title.text.split())
    assert(scraper.data.title.text.split()[text_len - 1] == 'encyclopedia')
    print("Integration test passed")




