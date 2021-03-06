﻿[![PyPI](https://img.shields.io/pypi/v/vsptd.svg)](https://pypi.python.org/pypi?name=vsptd&:action=display) [![Documentation Status](https://readthedocs.org/projects/vsptd/badge/?version=latest)](http://vsptd.readthedocs.io/ru/latest/?badge=latest)



vsptd — пакет библиотек для работы с ВСПТД в Python
====================================================

Документация
------------

Примеры использования и описание API — в документации:
[https://vsptd.readthedocs.io](https://vsptd.readthedocs.io)

ВСПТД
-----

ВСПТД — виртуальное строковое пространство технологических данных — описывает специальный способ организации баз знаний и баз данных.

Подробнее узнать о спецификации можно в следующих пособиях:

* _Виртуальное строковое пространство технологических данных и знаний. Методы представления данных. Филиппов А. Н._
* _Применение методов виртуального строкового пространства технологических данных и знаний в САПР ТП. Филиппов А.Н., Путинцева А.А._

Особенности пакета библиотек
----------------------------

* максимальная поддержка спецификации ВСПТД;
* возможность изменения параметров ВСПТД;
* подробная онлайн-документация и хорошо документированный код (docstrings);
* код библиотек покрыт тестами (unittests, doctests);
* подробные исключения, вызываемые в ходе работы с библиотеками;
* указание типов, где это возможно без потери совместимости с Python < 3.5;
* безопасное импортирование вида:

    ```python
    from vsptd import *
    from vsptd.parse import *
    ```

Состав пакета
-------------

* **vsptd**

    Основная библиотека. Позволяет работать с триплетами, триплетными строками, триплетными выражениями (фрейм-формулами). Также содержит функционал для настройки параметров ВСПТД.

* **parse**

    Разбор строк на ВСПТД-структуры, а также генерация соответствующих регулярных выражений.

* **extra**

    Дополнительные функции и ВСПТД-объекты.

* **support**

    Набор функций для использования во внутренней работе пакета.

Устройство проекта
------------------

* ``\vsptd`` — пакет библиотек
    - ``__init__.py``
    - ``vsptd.py``
    - ``extra.py``
    - ``parse.py``
    - ``support.py``

* ``\docs`` — исходные файлы документации

* ``\tests`` — юнит-тесты
    - ``test_Trp.py`` — тесты триплета
    - ``test_TrpStr.py`` — тесты триплетной строки
    - ``test_TrpExpr.py`` — тесты триплетного выражения
    - ``test_VSPTDSettings.py`` — тесты класса для настройки ВСПТД-параметров
    - ``test_extra.py`` — тесты дополнительных структур, функций
    - ``test_parse.py`` — тесты модуля разбора строк

* ``README.md`` — краткое описание пакета
* ``setup.py`` — setup script

Быстрый старт
-------------

Триплет

```python
>>> print(Trp('A', 'B', 'C'))  # str
$A.B='C';
>>> print(Trp('A', 'B', 42))  # int
$A.B=42;
>>> print(Trp('A', 'B', 3.14))  # float
$A.B=3.14;
```

```python
>>> my_trp = Trp('A', 'B', 'C', 'D')
>>> my_trp.prefix
'A'
>>> my_trp.name
'B'
>>> my_trp.value = 42  # изменение значения свойства
```

```python
>>> str(Trp('A', 'B', 'C'))
"$A.B='C';"
>>> print(Trp('A', 'B', 'C') + Trp('D', 'E', 'F'))
$A.B='C'; $D.E='F';
>>> Trp('A', 'B', 'C') == Trp('A', 'B', 'C')
True
```

Триплетная строка

```python
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
```

```python
>>> # доступ к триплету/триплетам
>>> my_trp_str.get('A', 'B')
>>> my_trp_str['A', 'B']
>>> my_trp_str.getpr('A')
>>> my_trp_str['A']
>>> my_trp_str[0]
>>> my_trp_str[:2]
```

```python
>>> # удаление триплета/триплетов
>>> my_trp_str.rem('A', 'B')
>>> del my_trp_str['D', 'E']
>>> my_trp_str.rempr('A')
>>> del my_trp_str['A']
>>> del my_trp_str[0]
>>> del my_trp_str[:2]
```

```python
>>> trp_str = TrpStr(Trp('D', 'E', 'F'), Trp('A', 'B', 'C'), Trp('A', 'H', 'P'))
>>> trp_str.sort()
>>> print(trp_str)
$A.B='C'; $A.H='P'; $D.E='F';
```



Зависимости
-----------

* Python 3.3+



Установка
---------

```
pip install vsptd
```

Установка последней нестабильной версии (альфа, бета):

```
pip install vsptd --pre
```

Установка из файла (можно получить, например, со страницы [релизов](https://github.com/become-iron/vsptd/releases)):

```
pip install <путь к файлу>

Например:
pip install vsptd-1.2.0-py3-none-any.whl
```



Обновление
----------

```
pip install --upgrade vsptd
```
