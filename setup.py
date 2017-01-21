from setuptools import setup
from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))


def read_file(path_segments):
    """Read a UTF-8 file from the package. Takes a list of strings to join to
    make the path"""
    file_path = os.path.join(here, *path_segments)
    with open(file_path, encoding="utf-8") as f:
        return f.read()


def exec_file(path_segments, name):
    """Extract a constant from a python file by looking for a line defining
    the constant and executing it."""
    result = {}
    code = read_file(path_segments)
    lines = [line for line in code.split('\n') if line.startswith(name)]
    exec("\n".join(lines), result)
    return result[name]


setup(
    name="matrix-synapse-smf",
    version=exec_file(("smf_auth_provider.py",), "__version__"),
    py_modules=["smf_auth_provider"],
    description="An SMF auth provider for Synapse",
    install_requires=[
        "Twisted>=15.1.0",
        "mysql-python",
        "bcrypt>=3.1.0",
    ],
    long_description=read_file(("README.rst",)),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
)
