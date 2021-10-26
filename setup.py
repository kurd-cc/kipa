from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.7'
DESCRIPTION = 'Convert Kurdish text to IPA phonetics'
LONG_DESCRIPTION = 'A package that convert Kurdish texts to phonetics, and other related tools'

# Setting up
setup(
    name="kipa",
    version=VERSION,
    author="Jagar Yousef",
    author_email="<jagar.yousef@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    setup_requires=['wheel'],
    url='https://github.com/kurd-cc/kipa',
    keywords=['kurdish', 'language', 'language-processing', 'kurmanji', 'ipa', 'phonetics'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

# 1. python setup.py sdist bdist_wheel
# 2. twine upload --skip-existing dist/*