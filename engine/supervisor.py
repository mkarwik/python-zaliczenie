from scraper import Scraper


class Supervisor:
    def __init__(self, commands, wiki_url):
        self.commands = commands
        self.wiki_url = wiki_url
        if commands["summary"] is not None:
            scraper = Scraper(wiki_url=wiki_url, phrase=commands["summary"])
            scraper.summary()
        if commands["table"] is not None:
            scraper = Scraper(wiki_url=wiki_url, phrase=commands["table"]["phrase"])
            scraper.table(commands["table"]["number"],
                          commands["table"]["first-row-is-header"])
        if commands["count-words"] is not None:
            scraper = Scraper(wiki_url=wiki_url, phrase=commands["count-words"])
            scraper.count_words()
        if commands["anal-relat-word-freq"] is not None:
            scraper = Scraper()
            scraper.analyze_relative_freq(commands["anal-relat-word-freq"]["mode"],
                                          commands["anal-relat-word-freq"]["count"],
                                          commands["anal-relat-word-freq"]["chart"],
                                          commands["anal-relat-word-freq"]["directory"])
        if commands["auto-count"] is not None:
            scraper = Scraper(wiki_url=wiki_url, phrase=commands["auto-count"]["phrase"])
            scraper.auto_count_words(commands["auto-count"]["phrase"],
                                     commands["auto-count"]["depth"],
                                     commands["auto-count"]["time"])




