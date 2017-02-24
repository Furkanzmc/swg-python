import json
import yaml
import io
import os

"""

"""


class SwgParser:
    """
    This is the last end position of the swg block. This index is after the `@swg_end`
    """
    _last_swg_block_position = 0
    _swagger_dictionary = {}

    def compile_folder(self, directory):
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".py"):
                    print(filepath)
                    self.compile_swagger_json(filepath)

    def compile_swagger_json(self, file_path):
        """
        @brief
        """

        self._last_swg_block_position = 0

        file_content = open(file_path).read()

        while self.has_next():
            block = self.get_swg_block(file_content)
            print(block)
            if block is None:
                break

            if self.is_swg_definition(block):
                self.put_definitions(block)
            elif self.is_swg_info(block):
                self.put_swg_info(block)
            elif self.is_swg_path(block):
                self.put_swg_path(block)

        return self._swagger_dictionary

    def write_to_file(self, file_path, format='yaml'):
        """
        @brief      Write the generated swagger to a file. JSON and YAML formats are supported
        @param      file_path - The absolute file path
        @param      format Options are json and yaml
        @return     void
        """

        if len(self._swagger_dictionary) > 0:
            file = io.open(file_path, 'w', encoding='utf8')
            if format == 'yaml':
                file.write(yaml.dump(self._swagger_dictionary))
            else:
                file.write(json.dumps(self._swagger_dictionary))
            file.close()

    def put_definitions(self, block):
        definition_name = block.get('definition')
        block.pop('definition')
        block = {definition_name: block}
        if self._swagger_dictionary.get('definitions') is not None and self._swagger_dictionary.get('definitions').get(definition_name) is None:
            self._swagger_dictionary['definitions'].update(block)
        elif self._swagger_dictionary.get('definitions') is not None:
            self._swagger_dictionary['definitions'][definition_name] = block.get(definition_name)
        else:
            self._swagger_dictionary.update({'definitions': block})

    def put_swg_info(self, block):
        self._swagger_dictionary.update(block)

    def put_swg_path(self, block):
        method_name = self.get_path_method(block)
        path_name = block.get('path')
        block.pop('path')
        block = block.get(method_name)

        if self._swagger_dictionary.get('paths') is not None and self._swagger_dictionary['paths'].get(path_name) is not None:
            block = {method_name: block}
            self._swagger_dictionary['paths'][path_name] = block
        elif self._swagger_dictionary.get('paths') is not None:
            block = {path_name: {method_name: block}}
            self._swagger_dictionary['paths'].update(block)
        else:
            block = {'paths': {path_name: {method_name: block}}}
            self._swagger_dictionary.update(block)

    def get_path_method(self, block):
        is_get = block.get('get') is not None
        is_delete = block.get('delete') is not None
        is_post = block.get('post') is not None
        is_put = block.get('put') is not None
        method = ""

        if is_get:
            method = 'get'
        elif is_delete:
            method = 'delete'
        elif is_post:
            method = 'post'
        elif is_put:
            method = 'put'

        return method

    def has_next(self):
        return self._last_swg_block_position > -1

    def get_swg_block(self, content):
        """
        @brief      Finds the block that starts with `@swg_begin` and ends with `@swg_end`
                    and returns the block within.
        @param      content  The original content
        @return     The swagger block as a dictionary. If there is not a swagger block, returns None
        """

        swg_begin = "@swg_begin"
        swg_end = "@swg_end"
        block_dict = None

        if self._last_swg_block_position > -1:
            local_content = content[self._last_swg_block_position:]
            start = local_content.find(swg_begin)
            end = local_content.find(swg_end)
            self._last_swg_block_position += end + len(swg_end)

            if self._last_swg_block_position >= len(content) or start == -1 or end == -1:
                self._last_swg_block_position = -1
            else:
                block = local_content[start + len(swg_begin):end]
                block_dict = yaml.load(block)

        return block_dict

    def is_swg_definition(self, swg_block):
        """
        @brief      A definition block begins with a `definition` key at the top of the document.
        @param      swg_block  The swg block
        @return     True if swg definition, False otherwise.
        """

        return swg_block.get('definition') is not None

    def is_swg_path(self, swg_block):
        """
        @brief      A path block begins with a `method` key at the top of the document.
        @param      swg_block  The swg block
        @return     True if swg path, False otherwise.
        """

        is_get = swg_block.get('get') is not None
        is_delete = swg_block.get('delete') is not None
        is_post = swg_block.get('post') is not None
        is_put = swg_block.get('put') is not None

        return is_get or is_put or is_delete or is_post

    def is_swg_info(self, swg_block):
        """
        @brief      This is the block that describes the whole API. If an `info` key is present, it is treated as an info block.
        @param      swg_block  The swg block
        @return     True if swg root
        """

        return swg_block.get('info') is not None


swg_parser = SwgParser()
swg_parser.compile_folder('E:/Development/Playground/swagger_test')
swg_parser.write_to_file("swagger.yaml")
