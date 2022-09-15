from setuptools import setup, find_packages

setup(
    name='pytentiostat',
    version='1.0.0',
    author='Oliver Rodriguez',
    author_email='oliver.rdz@softpotato.xyz',
    packages=find_packages('src'),
    package_dir={'':'src'},
    url='https://github.com/jrlLAB/pytentiostat',
    keywords='Electrochemistry',
    install_requires=[
    'numpy',
	'scipy',
	'matplotlib',
	'softpotato',
    ],
)
