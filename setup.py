try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools"
    )


setup(
    name="dedupe-variable-datetime",
    url="https://github.com/datamade/dedupe-variable-datetime",
    version="1.0.0",
    description="DateTime variable type for dedupe",
    packages=["datetimetype"],
    install_requires=["dedupe", "datetime-distance"],
    entry_points={"dedupe": ["datetimetype = datetimetype"]},
    license="The MIT License: http://www.opensource.org/licenses/mit-license.php",
)
