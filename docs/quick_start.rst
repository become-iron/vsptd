Быстрый старт
=============

Триплет
-------

>>> print(Trp('A', 'B', 'C'))  # str
$A.B='C';
>>> print(Trp('A', 'B', 42))  # int
$A.B=42;
>>> print(Trp('A', 'B', 3.14))  # float
$A.B=3.14;

>>> my_trp = Trp('A', 'B', 'C', 'D')
>>> my_trp.prefix
'A'
>>> my_trp.name
'B'
>>> my_trp.value = 42  # изменение значения свойства

>>> str(Trp('A', 'B', 'C'))
"$A.B='C';"
>>> print(Trp('A', 'B', 'C') + Trp('D', 'E', 'F'))
$A.B='C'; $D.E='F';
>>> Trp('A', 'B', 'C') == Trp('A', 'B', 'C')
True

Триплетная строка
-----------------

>>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'))
>>> str(my_trp_str)
"$A.B='C'; $D.E='F';"
>>> TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F')) == TrpStr(Trp('A', 'B', 'C'))
False
>>> len(TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F')))
2
>>> 'A' in my_trp_str  # по префиксу
True
>>> for trp in my_trp_str:
...     print(trp)
$D.E='F';
$A.B='C';
>>> print(TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F')) + Trp('G', 'H', 'I'))
$D.E='F'; $G.H='I'; $A.B='C';

>>> # доступ к триплету/триплетам
>>> my_trp_str.get('A', 'B')
>>> my_trp_str['A', 'B']
>>> my_trp_str.getpr('A')
>>> my_trp_str['A']
>>> my_trp_str[0]
>>> my_trp_str[:2]

>>> # удаление триплета/триплетов
>>> my_trp_str.rem('A', 'B')
>>> del my_trp_str['D', 'E']
>>> my_trp_str.rempr('A')
>>> del my_trp_str['A']
>>> del my_trp_str[0]
>>> del my_trp_str[:2]

>>> trp_str = TrpStr(Trp('D', 'E', 'F'), Trp('A', 'B', 'C'), Trp('A', 'H', 'P'))
>>> trp_str.sort()
>>> print(trp_str)
$A.B='C'; $A.H='P'; $D.E='F';
