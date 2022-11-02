from setuptools import setup, find_packages

setup(
    name='pypotato',
    version='1.2.3',
    author='Oliver Rodriguez',
    author_email='oliver.rdz@softpotato.xyz',
    packages=find_packages('src'),
    package_dir={'':'src'},
    url='https://github.com/jrlLAB/pypotato',
    keywords='Electrochemistry',
    install_requires=[
    'numpy',
	'scipy',
	'matplotlib',
	'softpotato',
    'pyserial'
    ],
)
