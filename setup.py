# -*- coding: utf-8 -*-
from setuptools import setup
from vsptd import __version__

setup(
    name='vsptd',
    version=__version__,
    url='https://github.com/become-iron/vsptd/',
    description='vsptd — пакет библиотек для работы с ВСПТД в Python.',
    # long_description='',
    keywords=('vsptd', 'ВСПТД', 'ВСПТДЗ'),
    classifiers=(
        'Operating System :: OS Independent',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ),
    packages=('vsptd',),
    # data_files=(
    #     ('help', ('README.md',))
    # ),
)
