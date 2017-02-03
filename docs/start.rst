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

С комментарием:

    >>> print(Trp('A', 'B', 'C', 'D'))
    $A.B='C'"D";

Триплет-цель:

    .. note::

        В контексте данного пакета библиотек под триплетом-целью имеется в виду триплет, не имеющий значения.

        В строковом представлении он будет иметь следующий вид: ``$P.N`` или ``P.N``.

    >>> print(Trp('A', 'B'))
    $A.B
    >>> print(Trp('A', 'B', special=True))
    A.B

С заявкой (``bid=True``):

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
>>> print(Trp('A', 'B', TrpExpr(Trp('C', 'D'), '*', 42)))  # триплетное выражение
$A.B=$C.D*42;

Доступ к свойствам
^^^^^^^^^^^^^^^^^^

>>> my_trp = Trp('A', 'B', 'C', 'D')
>>> my_trp.prefix
'A'
>>> my_trp.name
'B'
>>> my_trp.value
'C'
>>> my_trp.value = 42  # изменение значения свойства
>>> my_trp.comment
'D'
>>> my_trp.special
False
>>> my_trp.bid
False

.. warning:: Свойства **prefix** и **name** недоступны для изменения — будет вызвано исключение :class:`AttributeError`.

Строковое представление
^^^^^^^^^^^^^^^^^^^^^^^

>>> str(Trp('A', 'B', 'C'))
"$A.B='C';"
>>> repr(Trp('A', 'B', 'C'))
"Trp(prefix='A', name='B', value='C')"

Сложение
^^^^^^^^

Триплет + триплет:

    >>> print(Trp('A', 'B', 'C') + Trp('D', 'E', 'F'))
    $A.B='C'; $D.E='F';

Триплет + триплетная строка:

    >>> print(Trp('A', 'B', 'C') + TrpStr(Trp('D', 'E', 'F'), Trp('G', 'H', 'I')))
    $A.B='C'; $D.E='F'; $G.H='I';

Сравнение
^^^^^^^^^

>>> Trp('A', 'B', 'C') == Trp('A', 'B', 'C')
True
>>> Trp('A', 'B', 'C') == Trp('D', 'E', 'F')
False

.. warning:: Свойства **comment**, **special**, **bid** не учитываются при сравнении.



Триплетная строка
-----------------

Триплетная строка состоит из множества триплетов.

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

.. warning:: В текущей версии в триплетной строке не гарантируется упорядоченность.

Строковое представление
^^^^^^^^^^^^^^^^^^^^^^^

>>> str(my_trp_str)
"$A.B='C'; $D.E='F';"
>>> repr(my_trp_str)
"TrpStr(Trp(prefix='A', name='B', value='C'), Trp(prefix='D', name='E', value='F'))"

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

Итерирование
^^^^^^^^^^^^

>>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'))
>>> for trp in my_trp_str:
...     print(trp)
$D.E='F';
$A.B='C';

Так же ``TrpStr`` можно представить в виде ``list`` или ``tuple``:

>>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'))
>>> list(my_trp_str)
[Trp(prefix='D', name='E', value='F'), Trp(prefix='A', name='B', value='C')]
>>> tuple(my_trp_str)
(Trp(prefix='D', name='E', value='F'), Trp(prefix='A', name='B', value='C'))

Сложение
^^^^^^^^

Триплетная строка + триплет:

    >>> print(TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F')) + Trp('G', 'H', 'I'))
    $D.E='F'; $G.H='I'; $A.B='C';

Триплетная строка + триплетная строка:

    >>> print(TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F')) + TrpStr(Trp('G', 'H', 'I'), Trp('J', 'K', 'L')))
    $D.E='F'; $G.H='I'; $A.B='C'; $J.K='L';

Сложение с помощью метода ``add`` отличается тем, что данный метод не возвращает новый экземпляр, а изменяет нынешний.

    Описание API: :meth:`vsptd.vsptd.TrpStr.add`.

    >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'))
    >>> my_trp_str.add(Trp('D', 'E', 'F'))
    >>> print(my_trp_str)
    $D.E='F'; $A.B='C';
    >>> my_trp_str.add(TrpStr(Trp('G', 'H', 'I'), Trp('J', 'K', 'L')))
    $D.E='F'; $G.H='I'; $A.B='C'; $J.K='L';

.. note::
    Если при создании/обновлении триплетной строки, окажется, что существуют триплеты
    с одинаковым сочетанием префикса и имени, то будут сохранены значения последнего.

Получение триплетов
^^^^^^^^^^^^^^^^^^^

Получить триплет по префиксу и имени:

    * ``<TrpStr>.get(prefix, name) -> <Trp>``

        Описание API: :meth:`vsptd.vsptd.TrpStr.get`

        >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'H', 'P'))
        >>> print(my_trp_str.get('A', 'B'))
        $A.B='C';

    * ``<TrpStr>[prefix, name] -> <Trp>``

        >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'H', 'P'))
        >>> print(my_trp_str['A', 'B'])
        $A.B='C';

Получить триплеты по префиксу:

    * ``<TrpStr>.getpr(prefix) -> <TrpStr>``

        Описание API: :meth:`vsptd.vsptd.TrpStr.getpr`

        >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'H', 'P'))
        >>> print(my_trp_str.getpr('A'))
        $A.B='C'; $A.H='P';

    * ``<TrpStr>[prefix] -> <TrpStr>``

        >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'H', 'P'))
        >>> print(my_trp_str['A'])
        $A.B='C'; $A.H='P';

Удаление триплетов
^^^^^^^^^^^^^^^^^^

Удалить триплет по префиксу и имени:

    * ``<TrpStr>.rem(prefix, name)``

        Описание API: :meth:`vsptd.vsptd.TrpStr.rem`

        >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'H', 'P'))
        >>> my_trp_str.rem('A', 'B')
        >>> print(my_trp_str)
        $D.E='F'; $A.H='P';

    * ``del <TrpStr>[prefix, name]``

        >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'H', 'P'))
        >>> del my_trp_str['D', 'E']
        >>> print(my_trp_str))
        $D.E='F'; $A.H='P';

Удалить триплеты по префиксу:

    * ``<TrpStr>.rempr(prefix)``

        Описание API: :meth:`vsptd.vsptd.TrpStr.rempr`

        >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'H', 'P'))
        >>> my_trp_str.rempr('A')
        >>> print(my_trp_str)
        $D.E='F';

    * ``del <TrpStr>[prefix]``

        >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'H', 'P'))
        >>> del my_trp_str['A']
        >>> print(my_trp_str)
        $D.E='F';



Триплетное выражение (фрейм-формула)
------------------------------------

Вспомогательный класс, упрощающий работу с выражениями, включающими в себя триплеты.
Может использоваться как значение триплета.

Описание API
^^^^^^^^^^^^

:class:`vsptd.vsptd.TrpExpr`

Создание
^^^^^^^^

>>> from vsptd import Trp, TrpExpr
>>> expr = TrpExpr(Trp('A', 'B'), '*', Trp('C', 'D'))
>>> print(expr)
$A.B*$C.D
>>> print(Trp('E', 'F', expr))
$E.F=$A.B*$C.D;

Строковое представление
^^^^^^^^^^^^^^^^^^^^^^^

>>> str(TrpExpr(Trp('A', 'B'), '*', Trp('C', 'D')))
'$A.B*$C.D'
>>> repr(TrpExpr(Trp('A', 'B'), '*', Trp('C', 'D')))
"TrpExpr(Trp(prefix='A', name='B'), '*', Trp(prefix='C', name='D'))"

Вычисление выражения
^^^^^^^^^^^^^^^^^^^^

Описание API: :meth:`vsptd.vsptd.TrpExpr.compute`.

.. warning::
    В текущей версии для вычисления выражения используется ``eval``, что потенциально опасно.

>>> expr = TrpExpr(Trp('A', 'B'), '*', Trp('C', 'D'))
>>> trp_str = TrpStr(Trp('A', 'B', 21), Trp('C', 'D', 2))
>>> expr.compute(trp_str)
42



Дополнительные ВСПТД-структуры и функции
----------------------------------------

О дополнительных ВСПТД-структурах и функциях можно узнать, изучив описание описание API модуля :mod:`vsptd.extra`.
