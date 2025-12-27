from setuptools import find_packages, setup

setup(
    name='djx',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
    ],
    extras_require={
        'example': [
            'ipdb',
            'jupyter',
            'jupyter-client',
            'jupyter-console',
            'ipython',
            'scikit-learn',
            'pylint',
            'flake8',
            'matplotlib',
            'seaborn']
    },
)
