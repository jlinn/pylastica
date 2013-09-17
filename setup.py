from setuptools import setup, find_packages

long_description = open('README.rst').read()

packages = find_packages(exclude=["tests", "tests.*"])

setup(
    name='pylastica',
    version='0.1.3',
    packages=packages,
    url='https://github.com/jlinn/pylastica',
    license='LICENSE.txt',
    author='Joe Linn',
    author_email='',
    description="Python port of Nicolas Ruflin's Elastica PHP library",
    long_description=long_description,
    install_requires=['dateutils', 'urllib3'],
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
    ]
)
