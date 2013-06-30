#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='ccMonkey',
      version='0.1',
      description='Listener for jenkins cc.xml file suitable for Raspberry PI (or similar boards)',
      long_description='Parses and interprets projects statuses from Jenkins, when one project of intrest fails than it oscilate one of raspberry\'s GPIO, all the inputs and outputs are configurable from a basic settings file',
      author='Tiberiu Corbu',
      author_email='tiberiu.corbu@gmail.com',
      scripts=['mercurio/mercurio-run.py'],
      license='MIT',
      eurl='https://github.com/tiberiucorbu/ccMonkey',
      include_package_data=True,
      classifiers=[
        'Development Status :: 0.1 Alpha',
        'Intended Audience :: Makers',
        'License :: MIT License',
        'Operating System :: Linux ARM',
        'Programming Language :: Python',
        'Topic :: Utilities',
      ],
      packages=find_packages(exclude=['tests']),
      requires=['pyserial', 'clint'],
      install_requires=['pyserial', 'clint'],
      )
