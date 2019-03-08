from setuptools import find_packages, setup

setup(
    name='djx',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'pyyaml==3.13',
        'toolz==0.9.0',
        'pandas==0.23.3',
        'docopt==0.6.2',
        'structlog==19.1.0',
        'google-cloud-storage==1.14.0',
        'psycopg2-binary==2.7.7'
    ],
    extras_require={
        'dev': ['ipdb',
                'jupyter',
                'jupyter-client',
                'jupyter-console',
                'ipython',
                'sklearn',
                'pylint',
                'flake8']
    },
    scripts=[
        'scripts/djx'
    ]
)
