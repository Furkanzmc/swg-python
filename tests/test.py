from swg_python import SwgParser

swg_parser = SwgParser()
swg_parser.add_folder('./example')
swg_parser.compile('swagger.json', 'json')

# Test without the output path
swg_parser.add_folder('./example')
swg_parser.compile()
swg_parser.write_to_file('swagger.yaml', 'yaml')
