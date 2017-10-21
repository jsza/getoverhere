from setuptools import find_packages, setup

setup(
    name = 'getoverhere',
    version = '0.1',
    packages = find_packages(),
    scripts = ['scripts/goh'],
    install_requires = ['beautifulsoup4', 'html5lib', 'requests[security] >= 2.6.0'],
    author = 'jayess',
    description = 'Addon updater/installer for source engine games.',
    url = 'https://github.com/jsza/getoverhere'
)
