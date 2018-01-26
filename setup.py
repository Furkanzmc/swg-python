# Always prefer setuptools over distutils
from setuptools import setup
from os import path
from swg_python import __version__ as VERSION

here = path.abspath(path.dirname(__file__))

long_description = "For more information see https://github.com/Furkanzmc/swg-python"

setup(
    name='swg_python',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=VERSION,

    description='Framework agnostic Swagger parsing library in Python',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/Furkanzmc/swg-python',

    # Author details
    author='Furkan Uzumcu',
    author_email='furkanuzumcu@gmail.com',

    # Choose your license
    license='Public Domain',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: Public Domain',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='python swagger python-library python-script',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['swg_python'],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pyyaml==3.12'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'static': 'swg_python/static *',
        'templates': 'swg_python/templates *'
    },
    include_package_data=True,
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'swg_python = swg_python.parser:command_line_compile',
        ],
    },
)
