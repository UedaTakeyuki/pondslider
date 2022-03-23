#from distutils.core import setup
from setuptools import setup

with open("README.md") as f:
  long_description = f.read()

setup(
  name = 'pondslider',
  packages = ['pondslider'], # this must be the same as the name above
  version = '0.4.8',
  description = 'Multipurpose sensor handler, read sensor & do somethings (send, save, trigger, ...) with the value.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Takeyuki UEDA',
  author_email = 'gde00107@nifty.com',
  license='MIT',
  url = 'https://github.com/UedaTakeyuki/pondslider', # use the URL to the github repo
  keywords = ['sensor', 'IoT'], # arbitrary keywords
  classifiers = ['Development Status :: 4 - Beta',
                 'Programming Language :: Python',
                 'Topic :: Terminals'
  ],
  install_requires=[
    "pytoml"
  ]
)
