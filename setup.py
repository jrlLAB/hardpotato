from setuptools import setup, find_packages

setup(
    name='pytentiostat',
    version='0.0.1',
    author='Oliver Rodriguez',
    author_email='oliverrz@illinois.edu',
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
