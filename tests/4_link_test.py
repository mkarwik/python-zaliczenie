from engine.scraper import is_a_wiki_link

def test_link():
    link = 'www.mimuw.edu.pl'
    assert not is_a_wiki_link(link)

    wiki_link = '/wiki/Giovani'
    assert is_a_wiki_link(wiki_link)
