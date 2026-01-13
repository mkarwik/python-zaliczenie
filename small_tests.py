from wiki_scraper import parse_input
import sys



#Parsing test
input = ['/home/jarek/PycharmProjects/Zaliczenie/small_tests.py',
         '--summary', 'Pies', '--table', 'kot', '--number', '5']
parsed_input = parse_input(input)
print(parsed_input)