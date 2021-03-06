Внутреннее устройство
=====================

Устройство триплетной строки
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Согласно принципам ВСПТД триплетная строка имеет следующие свойства:

    * уникальность триплетов в триплетной строке должна обеспечиваться парой значений префикса триплета и имени триплета;
    * триплеты в строке упорядочены.

Для этого используется следующее решение:

    * для хранения триплета используется класс ``OrderedDict`` из стандартной библиотеки, который аналогичен обычному ``dict``, но при этом обеспечивает упорядоченность элементов;
    * в качестве значений используются триплеты (экземпляры класса ``Trp``), а ключом служит hash-значение, высчитанное для пары префикса и имени триплета.

.. code-block:: python

    # примерная инициализация класса TrpStr
    def __init__(self, *trps):
        self.__trps = OrderedDict({hash((trp.prefix, trp.name)): trp for trp in trps})

.. note::

    Hash-значение высчитывается c помощью встроенной функции ``hash``. Результатом данной функции является некоторое число, уникальное для переданных значений.

    В качестве ключа можно было бы использовать кортеж (``tuple``), где его элементами являлись бы префикс и имя триплета, но в этом случае могли бы возникнуть следующие проблемы:

    * потенциально размер в памяти полученного кортежа может быть намного больше, чем размер hash-значения;
    * поиск среди ключений-чисел будет осуществляться намного быстрее, что особо будет заметно при большом количестве триплетов в триплетной строке.


Валидация ВСПТД-параметров
^^^^^^^^^^^^^^^^^^^^^^^^^^

При инициализации модуля поле ``settings`` каждого ВСПТД-класса инициализируется экземпляром класса :class:`vsptd.vsptd.VSPTDSettings` с его стандартными настройками. В дальнейшем вся валидация параметров производится через параметры записанные по данному полю.

Валидация проводится, например, при создании объекта (``Trp``), изменении полей ВСПТД-структур, вызове их методов, принимающих параметры. Для этого используется метод ``validate``, которому необходимо передать параметр для проверки. В данном методе проводится проверка на корректность согласно заданным ВСПТД-параметрам. В том случае, если параметр некорректен, будет вызвано соответствующее исключение.
