from setuptools import setup, find_packages

setup(
    name='DarkTowerPy',
    version='1.0',
    packages=find_packages(),
    package_data={'': ['*.jpg', '*.ttf', '*.wav']},
    url='',
    license='',
    author='David Niquette',
    author_email='',
    description='DarkTowerPy',
    install_requires=[
        'pygame',
    ]
)
