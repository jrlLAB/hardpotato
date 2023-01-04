from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pypotato',
    version='1.3.2',
    description='Python API to control programmable potentiostats.',
    long_description=readme(),
    long_description_content_type="text/markdown",
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
