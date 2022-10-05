from setuptools import setup, find_packages


setup(
    name='zoe',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'zoe = zoe.cli:entry',
            'zoe! = zoe.challenge:entry'
        ]
    }
)
