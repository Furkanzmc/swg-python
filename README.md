# swg-python

SwgParser is a simple parser that extracts the Swagger API documentation throughout the given folders. It works with both `Python2.7` and `Python 3.x`.
The Swagger documentation must be written in YAML format. The specification is the same as the Swagger specification except a few details.

## Exceptions

- A path definition **MUST** have the keys `method` and `path`. `method` key contains the standard HTTP methods and `path` is the path of the operation
- A definition **MUST** have the `definition` key. A block that has the `definition` key will be treated as a definition. Obviously, the value for the key
  is the definition name.

Also, you need to wrap the YAML string between `@swg_begin` and `@swg_end`.
The documentation can be scattered throughout the project, `SwgParser` will walk thought the files and produce a single `swagger.json` or `swagger.yaml`
file. For an example on how to use it, check the `example` folder. Beware, although it has valid Swagger documentation the project itself does nothing and
doesn't work. `SwgParser` does not depend on any framework specific properties, so it can be used with any kind of project you want.

# Swagger Preview Support

`swg-python` supports preview of the Swagger Specification using the official Swagger Editor 3.0.1 release.
When you compile the Swagger Specification with the following code:

```
from swg_python.parser import SwgParser

swg_parser = SwgParser()
swg_parser.add_folder('./api')
swg_parser.add_folder('./arifname')
swg_parser.compile('docs/swagger.json', 'json')
```

When the preview is updated you can use the following the view it in your browser.

As of `v1.0.5`, Redoc is used as the default Open API renderer. To disable it while using Django, add the following to
your project settings file.

```
SWG_ENABLE_REDOC = False
```

## Django

```
from swg_python.views import render_swagger_view
urlpatterns = [
    url(r'^docs/', render_swagger_view),
]
```

When using Django, remember to add `swg_python` to the `INSTALLED_APPS`

```
INSTALLED_APPS = [
    'swg_python',
]
```

# How To Install

Install using `pip`

`pip install swg-python`

# Contributions

I'm open to any improvements. This is a really primitive work right now. It works, let me assure you, but it needs more improvements to work better.
Like a better error handling, static Swagger hosting etc.
