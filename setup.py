from setuptools import setup

setup(
    name="AirCodea",
    version="0.0.1",
    package_dir={'': 'src'},
    scripts=[
        'scripts/codea',
    ]
    requirements=['requests'],
)
