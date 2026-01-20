from engine.scraper import Scraper


class Supervisor:
    def __init__(self, commands, wiki_url):
        self.commands = commands
        self.wiki_url = wiki_url
        if commands["summary"] is not None:
            scraper = Scraper(wiki_url=wiki_url, phrase=commands["summary"])
            scraper.summary()
        if commands["table"] is not None:
            scraper = Scraper(wiki_url=wiki_url, phrase=commands["table"]["phrase"])
            scraper.table()




