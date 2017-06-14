try:
    from setuptools import setup, Extension
except ImportError:
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")


setup(
    name='dedupe-variable-datetime',
    url='https://github.com/datamade/dedupe-variable-datetime',
    version='0.1.3',
    description='DateTime variable type for dedupe',
    packages=['dedupe.variables'],
    install_requires=['dedupe',
                      'datetime-distance',
                      'future'],
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php'
)
