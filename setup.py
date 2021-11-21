import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="metamenus",
    version="0.14.3",
    author='E.A. Tacao',
    author_email='mailto@tacao.com.br',
    maintainer='Humberto Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='wxPython Menu Maker',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/metamenus",
    packages=[
        'metamenus',
        'metamenus.internal'
    ],
    package_data={'metamenus.resources': ['loggingConfiguration.json', 'loggingConfiguration.json']},
    include_package_data=True,
    install_requires=['wxPython', 'click'],
    entry_points='''
        [console_scripts]
        mmprep=metamenus.mmprep:commandHandler
    ''',
)
