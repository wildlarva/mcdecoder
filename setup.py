from setuptools import setup, find_packages


setup(
    name='MC parser generator',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'':'src'},
    install_requires=['pyyaml', 'jinja2'],
    tests_require=['pytest'],
)
