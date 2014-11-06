from setuptools import setup, find_packages

setup(
    name = 'getoverhere',
    version = '0.1',
    packages = find_packages(),
    scripts = ['scripts/goh'],
    install_requires = ['beautifulsoup4', 'requests'],
    author = 'jayess',
    description = 'Addon updater/installer for source engine games.',
    url = 'https://github.com/jsza/getoverhere'
)
