from swg_python import SwgParser

swg_parser = SwgParser()
swg_parser.add_folder('./example')
swg_parser.compile()
swg_parser.write_to_file('swagger.json', 'json')
swg_parser.write_to_file('swagger.yaml', 'yaml')
