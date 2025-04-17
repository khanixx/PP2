from configparser import ConfigParser
parser = ConfigParser()
parser.read('C:\\PP2\\11Lab\\database.ini')
print(parser.sections())
