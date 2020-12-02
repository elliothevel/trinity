from setuptools import setup, find_packages


setup(
    name='trinity',
    description='Retirement calculator based on the Trinity study',
    version='0.0.1',
    packages=find_packages(),
    package_data={
        '': ['data/*.csv'],
    },
    entry_points={
        'console_scripts': [
            'trinity = trinity.simulation:main',
        ]
    }
)
