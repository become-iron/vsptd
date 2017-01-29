Быстрый старт
=============

Триплет
-------

Описание API
^^^^^^^^^^^^

:class:`vsptd.vsptd.Trp`

Создание
^^^^^^^^

    >>> from vsptd import Trp
    >>> my_trp = Trp('A', 'B', 'C')
    >>> my_trp
    Trp(prefix='A', name='B', value='C')
    >>> print(my_trp)
    $A.B='C';
    >>> str(my_trp)
    "$A.B='C';"

С комментарием:

    >>> print(Trp('A', 'B', 'C', 'D'))
    $A.B='C'"D";

Триплет-ссылка:

    >>> print(Trp('A', 'B'))
    $A.B
    >>> print(Trp('A', 'B', special=True))
    A.B

С заявкой:

    >>> print(Trp('A', bid=True))
    $A.=:;
    >>> print(Trp('A', 'B', bid=True))
    $A.B=:;
    >>> print(Trp('A', 'B', 'C', bid=True))
    $A.B=:'C';

Объекты различных типов в качестве значения триплета
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    >>> print(Trp('A', 'B', 'C'))  # str
    $A.B='C';
    >>> print(Trp('A', 'B', 42))  # int
    $A.B=42;
    >>> print(Trp('A', 'B', 3.14))  # float
    $A.B=3.14;
    >>> print(Trp('A', 'B', True))  # bool
    $A.B=True;
    >>> print(Trp('A', 'B', Trp('C', 'D')))  # триплет
    $A.B=$C.D;
    >>> print(Trp('A', 'B', TrpExpr(Trp('A', 'B'), '*', 42)))  # триплетное выражение
    $A.B=$A.B*42;

Доступ к свойствам
^^^^^^^^^^^^^^^^^^

    >>> my_trp.prefix
    'A'
    >>> my_trp.name
    'B'
    >>> my_trp.value
    'C'
    >>> my_trp.value = 42
    >>> print(my_trp)
    $A.B=42;
    >>> my_trp.special
    False
    >>> my_trp.bid
    False

.. warning:: Свойства **prefix** и **name** недоступны для изменения — будет вызвано исключение :class:`AttributeError`.

Сложение
^^^^^^^^

Триплет + триплет:

    >>> Trp('A', 'B', 'C') + Trp('D', 'E', 'F')
    TrpStr(Trp(prefix='A', name='B', value='C'), Trp(prefix='D', name='E', value='F'))

Триплет + триплетная строка:

    >>> Trp('A', 'B', 'C') + TrpStr(Trp('D', 'E', 'F'), Trp('G', 'H', 'I'))
    TrpStr(Trp(prefix='A', name='B', value='C'), Trp(prefix='D', name='E', value='F'), Trp(prefix='G', name='H', value='I'))


Сравнение
^^^^^^^^^

    >>> Trp('A', 'B', 'C') == Trp('A', 'B', 'C')
    True
    >>> Trp('A', 'B', 'C') == Trp('D', 'E', 'F')
    False

.. warning:: Параметры **comment**, **special**, **bid** не учитываются при сравнении.





Триплетная строка
-----------------

Описание API
^^^^^^^^^^^^

:class:`vsptd.vsptd.TrpStr`

Создание
^^^^^^^^

    >>> from vsptd import Trp, TrpStr
    >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'))

Из ``list`` или ``tuple``:

    >>> trps = [Trp('A', 'B', 'C'), Trp('D', 'E', 'F')]
    >>> my_trp_str = TrpStr(*trps)

    >>> my_trp_str
    TrpStr(Trp(prefix='A', name='B', value='C'), Trp(prefix='D', name='E', value='F'))
    >>> str(my_trp_str)
    "$A.B='C'; $D.E='F';"

Сравнение
^^^^^^^^^

    >>> TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F')) == TrpStr(Trp('A', 'B', 'C'))
    False

Длина триплетной строки
^^^^^^^^^^^^^^^^^^^^^^^

    >>> len(TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F')))
    2

Вхождение триплета(-ов) в триплетную строку
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'))
    >>> 'A' in my_trp_str  # по префиксу
    True
    >>> ('A', 'B') in my_trp_str  # по префиксу и имени
    True




Триплетное выражение
--------------------

Описание API
^^^^^^^^^^^^

:class:`vsptd.vsptd.TprExpr`

TODO