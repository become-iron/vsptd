# -*- coding: utf-8 -*-
from setuptools import setup
from vsptd import __version__

setup(
      name='vsptd',
      description='Работа с ВСПТД',
      version=__version__,
      url='https://github.com/become-iron/vsptd/',
      long_description=open('support_files/README.rst', encoding='utf-8').read(),
      classifiers=['Natural Language :: Russian'],
      py_modules=['vsptd'],
      data_files=[('unittests', ['unittests/ut_vsptd.py']),
                  ('help', ['README.md', 'CHANGES.md'])
                  ],
)
