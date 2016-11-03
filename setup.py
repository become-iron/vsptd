# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='vsptd',
    description='Работа с ВСПТД',
    version='1.1.0',
    url='https://github.com/become-iron/vsptd/',
    long_description=open('README.rst', encoding='utf-8').read(),
    classifiers=['Natural Language :: Russian'],
    py_modules=['vsptd'],
    data_files=[('unittests', ['unittests/ut_vsptd.py']),
                ('help', ['README.rst'])
                ],
)
