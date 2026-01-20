import parser
import sys

from engine.supervisor import Supervisor
wiki = 'https://bulbapedia.bulbagarden.net/wiki/'

if __name__ == "__main__":
    commands = parser.parse_input(sys.argv)
    supervisor = Supervisor(commands, wiki)

