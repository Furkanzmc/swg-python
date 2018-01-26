import json
import yaml
import io
import os
import sys
if sys.version_info[0] < 3:
    import codecs


swg_python_version = "1.0.5"


class SwgParser:
    """
    SwgParser is a simple parser that extracts the Swagger API documentation throughout the given folders. It works
    with both `Python2.7` and `Python 3.x`. The Swagger documentation must be written in YAML format. The specification
    is the same as the Swagger specification except a few details.

    **Exceptions**
    - A path definition **MUST** have the keys `method` and `path`. `method` key contains the standard HTTP methods and
      `path` is the path of the operation
    - A definition **MUST** have the `definition` key. A block that has the `definition` key will be treated as a
      definition. Obviously, the value for the key is the definition name.

    Also, you need to wrap the YAML string between `@swg_begin` and `@swg_end`.
    The documentation can be scattered throughout the project, `SwgParser` will walk thought the files and produce a
    single `swagger.json` or `swagger.yaml`
    file. For an example on how to use it, check the `example` folder. Beware, although it has valid Swagger
    documentation the project itself does nothing and doesn't work. `SwgParser` does not depend on any framework
    specific properties, so it can be used with any kind of project you want.

    `SwgParser` depends only on `PyYAML` package. And you can install it with the following
    command: `pip install pyyaml`

    **Example Usage**

    ```
    swg_parser = SwgParser()
    swg_parser.add_folder('./api')
    swg_parser.add_folder('./project')
    swg_parser.compile('docs/swagger.json', 'json')
    ```

    # Swagger Preview Support

    With the release of 1.0.4 `swg-python` supports preview of the Swagger Specification using the official Swagger
    Editor 3.0.1 release.

    # v1.0.5

    Redoc is now used as the default Open API renderer.

    """

    # This is the last end position of the swg block. This index is after the `@swg_end`
    _last_swg_block_position = 0

    # This is the main dictionary. It will stay the same unless @ref reset() method is called
    _swagger_dictionary = {}
    _folders = []
    _ingore_errors = False

    swagger_dump_yaml = ""
    swagger_dump_json = ""
    is_preview_enabled = False

    def __init__(self, enable_preview=True):
        self.is_preview_enabled = enable_preview

    def reset(self):
        """
        @brief      Resets all the parsing information. After this is called, you need to add folders to call the @ref compile() method
        """
        self._last_swg_block_position = 0
        self._swagger_dictionary = {}
        self._folders = []

        self.swagger_dump_yaml = ""
        self.swagger_dump_json = ""

    def add_folder(self, folder_path):
        """
        @brief      Adds the given folder_path to the list of folders to check for Swagger documentation.
                    If the folder already exists in the list, it is not added again.
        """

        if self._folders.count(folder_path) == 0:
            self._folders.append(folder_path)

    def compile(self, output_path='', format='yaml', ignore_errors=False):
        """
        @brief      Uses the _folders list to compile the Swagger documentation. If the output_path is provided after compiling the result is written.
        """

        self._ingore_errors = ignore_errors
        for folder in self._folders:
            self.compile_folder(folder)

        self.generate_spec()
        # Now write to the output_path if it's given
        if len(output_path) > 0 and os.path.exists(output_path):
            swagger_dump = ""
            if format == 'yaml':
                swagger_dump = self.swagger_dump_yaml
            else:
                swagger_dump = self.swagger_dump_json

            self.write_file(output_path, swagger_dump)

        # Now write to the js file
        dump = self.swagger_dump_json

        if self.is_preview_enabled is True:
            real_path = os.path.realpath(__file__)
            dir_path = os.path.dirname(real_path)
            js_content = "var SwaggerSpec = %s;" % (dump)
            self.write_file("%s/static/swg_python/specification.js" % (dir_path), js_content)
            self.write_file("%s/static/swg_python/specification.json" % (dir_path), dump)

    def compile_folder(self, directory):
        """
        @brief      Compiles a single directory. Only the files with the `py` extension is used.
        """

        for subdir, dirs, files in os.walk(directory):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".py"):
                    self.compile_swagger_json(filepath)

    def compile_swagger_json(self, file_path):
        """
        @brief      Compile a single file
        """

        self._last_swg_block_position = 0

        file_content = ""

        if sys.version_info[0] > 2:
            file_content = io.open(file_path, 'r', encoding='utf-8').read()
        else:
            file_content = codecs.open(filename=file_path, mode='r', encoding='utf-8').read()

        while self.has_next():
            block = self.get_swg_block(file_content)
            if block is None:
                break

            self.put_definitions(block)
            self.put_swg_info(block)
            self.put_swg_path(block)

        return self._swagger_dictionary

    def get_swg_block(self, content):
        """
        @brief      Finds the block that starts with `@swg_begin` and ends with `@swg_end`
                    and returns the block within.
        @param      content  The original content
        @return     The swagger block as a dictionary. If there is not a swagger block, returns None
        """

        SWG_BEGIN = "@swg_begin"
        SWG_END = "@swg_end"
        block_dict = None

        if self._last_swg_block_position > -1:
            local_content = content[self._last_swg_block_position:]
            start = local_content.find(SWG_BEGIN)
            end = local_content.find(SWG_END)
            self._last_swg_block_position += end + len(SWG_END)

            if self._last_swg_block_position >= len(content) or start == -1 or end == -1:
                self._last_swg_block_position = -1
            else:
                block = local_content[start + len(SWG_BEGIN):end]
                if self._ingore_errors:
                    try:
                        block_dict = yaml.load(block)
                    except:
                        pass
                else:
                    block_dict = yaml.load(block)

        return block_dict

    def put_definitions(self, block):
        """
        @brief      Checks if the block is a definition block and if it is, constructs a definition block and updates the swagger dictionary
        """

        if self.is_swg_definition(block) is False:
            return

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
        """
        @brief      If the block is an info block, updates the swagger dictionary. It does NOT check for duplicate input
        """

        if self.is_swg_info(block):
            self._swagger_dictionary.update(block)

    def put_swg_path(self, block):
        """
        @brief      If the block is a path block, updates the swagger dictionary.
        """

        if self.is_swg_path(block) is False:
            return

        method_name = block.get('method')
        path_name = block.get('path')
        block.pop('path')
        block.pop('method')

        if self._swagger_dictionary.get('paths') is not None and self._swagger_dictionary['paths'].get(path_name) is not None:
            block = {method_name: block}
            self._swagger_dictionary['paths'][path_name].update(block)
        elif self._swagger_dictionary.get('paths') is not None:
            # If the `paths` key exists, but the HTTP method is not yet put here
            block = {path_name: {method_name: block}}
            self._swagger_dictionary['paths'].update(block)
        else:
            block = {'paths': {path_name: {method_name: block}}}
            self._swagger_dictionary.update(block)

    def is_swg_definition(self, swg_block):
        """
        @brief      A block is treated as a definition block If it has the `definition` key. The value of the `definition` key is the name of the definition.
        @param      swg_block  The swg block
        @return     True if swg definition, False otherwise.
        """

        return swg_block.get('definition') is not None

    def is_swg_path(self, swg_block):
        """
        @brief      If the block has a `method` key, it is treated as a path.
        @param      swg_block  The swg block
        @return     True if swg path, False otherwise.
        """

        return swg_block.get('method') is not None

    def is_swg_info(self, swg_block):
        """
        @brief      This is the block that describes the whole API. If an `info` key is present, it is treated as an info block.
        @param      swg_block  The swg block
        @return     True if swg root
        """

        return swg_block.get('info') is not None

    def has_next(self):
        return self._last_swg_block_position > -1

    def generate_spec(self):
        """
        @brief      Generates the specs.
        @return     void
        """

        if len(self._swagger_dictionary) > 0:
            self.swagger_dump_yaml = yaml.dump(self._swagger_dictionary)
            self.swagger_dump_json = json.dumps(self._swagger_dictionary, ensure_ascii=False)

    def write_file(self, file_path, content, encoding='utf8'):
        if sys.version_info[0] > 2:
            file = io.open(file_path, 'w', encoding=encoding)
            file.write(content)
            file.close()
        else:
            file = codecs.open(filename=file_path, mode='w', encoding=encoding)
            file.write(content)
            file.close()


def command_line_compile(args=None):
    """
    @brief      Generate Swagger documentation.

    @param      args
                -f: Folder list, separated with space
                -t: Output type. Default is json. Options are `json` and `yaml`
                -o: Output full path
                -h: Print help message

    @return     void
    """

    if args is None:
        args = sys.argv[1:]

    folders = []
    output = ""
    output_type = 'json'
    is_f_param = False
    is_o_param = False
    is_t_param = False
    for arg in args:
        if arg == '-h':
            print("""
swg-python (v%s) is a simple parser that extracts the Swagger API documentation throughout the given folders.swg-python is a framework
    -f: Folder list, separated with space
    -t: Output type. Default is json. Options are `json` and `yaml`
    -o: Output full path
    -h: Print help message
            """ % (swg_python_version))
            break
        elif arg == '-f':
            is_f_param = True
            is_o_param = False
            is_t_param = False
        elif arg == '-o':
            is_f_param = False
            is_o_param = True
            is_t_param = False
        elif arg == '-t':
            is_f_param = False
            is_o_param = False
            is_t_param = True
        elif is_f_param:
            folders.append(arg)
        elif is_t_param:
            output_type = arg
        elif is_o_param:
            output = arg
            is_o_param = False

    swg_parser = SwgParser(False)

    for folder in folders:
        swg_parser.add_folder(folder)

    swg_parser.compile(output, output_type)
