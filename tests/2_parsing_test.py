from engine.parser import parse_input

#Parsing test
def test_parsing():
    input_data = ['/home/jarek/PycharmProjects/Zaliczenie/2_parsing_test.py',
         '--summary', 'Pies', '--table', 'kot', '--number', '5', '--count-words', 'Ryba',
         '--analyze-relative-word-frequency', '--mode', 'article', '--count', '3', '--chart', 'wykres']
    parsed_input = parse_input(input_data)
    assert parsed_input["summary"] == 'Pies'
    assert parsed_input["table"]["phrase"] == 'kot'
    assert parsed_input["table"]["number"] == '5'
    assert parsed_input["anal-relat-word-freq"]["mode"] == "article"
    assert parsed_input["anal-relat-word-freq"]["count"] == "3"
    assert parsed_input["auto-count"] is None
