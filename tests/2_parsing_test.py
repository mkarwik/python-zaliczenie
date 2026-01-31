from engine.parser import parse_input

#Parsing test
input_data = ['/home/jarek/PycharmProjects/Zaliczenie/2_parsing_test.py',
         '--summary', 'Pies', '--table', 'kot', '--number', '5']
parsed_input = parse_input(input_data)
print(parsed_input)