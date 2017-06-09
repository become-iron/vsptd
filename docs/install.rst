Установка, зависимости, сборка документации
===========================================


Зависимости
-----------

* Python 3.3+


Для сборки документации:

    * Sphinx == 1.5.5
    * sphinx_rtd_theme == 0.2.4



Установка
---------

.. code-block:: console

   pip install vsptd

Установка последней нестабильной версии (альфа, бета):

    .. code-block:: console

       pip install vsptd --pre

..
    С GitHub (позволит установить самую последнюю unreleased-версию):

        .. code-block:: console

           pip install https://github.com/become-iron/vsptd.git

..
   Если планируете внести вклад в разработку vsptd:

       .. code-block:: console

           git clone https://github.com/become-iron/vsptd.git
           cd vsptd
           python setup.py develop


Установка из файла:

    .. code-block:: console

       pip install <путь к файлу>

       Например:
       pip install vsptd-1.2.0-py3-none-any.whl



Обновление
----------

.. code-block:: console

   pip install --upgrade vsptd



Сборка документации
-------------------

1. Перейти в папку ``/docs``
2. В консоли ввести следующую команду:

    .. sourcecode:: console

        make html

3. Собранная документация окажется в папке ``/docs/_build/html``
