from setuptools import setup, find_packages


setup(
    name='mcparser-gen',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'mcparser_gen': ['py.typed'],
    },
    install_requires=['pyyaml', 'jinja2'],
)
