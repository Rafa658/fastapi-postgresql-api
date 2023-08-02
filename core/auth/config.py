from configparser import ConfigParser
from pathlib import Path

current_directory = Path(__file__).resolve().parent
def config(filename=f'{current_directory}/auth.ini', section='auth'):
    parser = ConfigParser()
    parser.read(filename)

    auth = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            auth[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file.')

    return auth