﻿[![PyPI](https://img.shields.io/pypi/v/vsptd.svg)](https://pypi.python.org/pypi?name=vsptd&:action=display)

# vsptd — библиотека для работы с ВСПТД в Python

**Модуль не поддерживает всю спецификацию ВСПТД!**

ВСПТД — виртуальное строковое пространство технологических данных — описывает специальный способ организации баз знаний и баз данных. Подробнее узнать о спецификации можно в следующих пособиях:

* _ВИРТУАЛЬНОЕ СТРОКОВОЕ ПРОСТРАНСТВО ТЕХНОЛОГИЧЕСКИХ ДАННЫХ И ЗНАНИЙ. Методы представления данных. Филиппов А. Н._
* _ПРИМЕНЕНИЕ МЕТОДОВ ВИРТУАЛЬНОГО СТРОКОВОГО ПРОСТРАНСТВА ТЕХНОЛОГИЧЕСКИХ ДАННЫХ И ЗНАНИЙ В САПР ТП. А.Н. Филиппов, А.А. Путинцева_

####Зависимости

* Python 3

####Установка
```
pip install vsptd
```

####Установка из файла
```
pip install <имя файла>

Например:
pip install vsptd-1.2.0-py3-none-any.whl
```

####Обновление
```
pip install vsptd -U
```

## Структура проекта

* ```README.md``` — документация
* ```CHANGES.md``` — описание изменений во всех версиях модуля
* ```setup.py``` — файл с настройками сборки модуля
* ```unittests/``` — юнит-тесты для библиотеки
* ```support_files/``` — вспомогательные файлы

Модуль состоит из следующих основных единиц:

* ```Trp``` — класс триплета
* ```TrpStr``` — класс триплексной строки
* ```parse_trp_str()``` — функция парсинга триплексной строки из str в TrpStr
* ```check_condition()``` — функция осуществляет проверку истинности условия, включающего в себя триплеты
* Различные регулярные выражения для проверки триплетов и их составляющих

_В процессе работы с модулем могут вызваны различные исключения, о которых можно почитать в описании соответствующих классов, методов, функций **в коде**._

## Trp

Класс триплета.

**Принимает:**

* ```prefix``` (str) - префикс триплета
* ```name``` (str) - имя триплета
* ```value``` (str, int, float) - значение триплета

### Примеры работы

####Создание
```python
my_trp = Trp('E', 'NM', 'Сверло')
my_trp2 = Trp('E1', 'NM', 'Зенкер')
```

####Обращение к свойствам
```python
>>> my_trp.prefix
'E'
>>> me_trp.name
'NM'
>>> my_trp.value
'Сверло'
```

####Перевод в строку, вывод
```
>>> str(my_trp)
"$E.NM='Сверло';"
>>> print(my_trp)
$E.NM='Сверло';
```

####Проверка на равенство
```python
>>> my_trp == my_trp2
False
>>> my_trp != my_trp2
True
```

####Сложение
```python
>>> str(my_trp + my_trp2)
"$E.NM='Сверло';$E1.NM='Зенкер';"  # объект класса TrpStr
```

## TrpStr

Класс триплексной строки

**Принимает:**

* ```*triplets``` (Triplet) - триплеты

### Примеры работы

####Создание
```python
>>> my_trp_str = TrpStr(Trp('E', 'NM', 'Сверло'),  Trp('E1', 'NM', 'Зенкер'))
>>> triplets = [Trp('E2', 'NM', 'Отвёртка'),  Trp('E3', 'NM', 'Топор')]
>>> my_trp_str2 = TrpStr(*triplets)
```

####Длина триплексной строки
```python
>>> len(my_trp_str)
2
```

####Перевод в строку, вывод
```
>>> str(my_trp_str)
"$E.NM='Сверло';$E1.NM='Зенкер';"
>>> print(my_trp_str)
$E.NM='Сверло';$E1.NM='Зенкер';
```

####Сложение
```
>>> my_trp = Trp('E4', 'NM', 'Развёртка')
>>> print(my_trp + my_trp_str)
$E4.NM='Развёртка';$E.NM='Сверло';$E1.NM='Зенкер';  # объект класса TrpStr
>>> print(my_trp_str + my_trp)
$E.NM='Сверло';$E1.NM='Зенкер';$E4.NM='Развёртка';  # объект класса TrpStr
>>> print(my_trp_str + my_trp_str2)
$E.NM='Сверло';$E1.NM='Зенкер';$E2.NM='Отвёртка';$E3.NM='Топор';  # объект класса TrpStr
```
Существует метод ```add``` практически эквивалентный сложению через оператор "+". Отличие в том, что данный метод не возвращает новый изменённый объект, а только изменяет нынешний.
```
>>> my_trp_str.add(my_trp_str2)
>>> print(my_trp_str)
$E.NM='Сверло';$E1.NM='Зенкер';$E2.NM='Отвёртка';$E3.NM='Топор';
```

####Проверка на равенство
```python
>>> my_trp_str == my_trp_str2
False
```

####Проверка вхождения триплета в триплексную строку
```python
>>> my_trp = Trp('E4', 'NM', 'Развёртка')
>>> my_trp_str = TrpStr(Trp('E', 'NM', 'Сверло'),  Trp('E1', 'NM', 'Зенкер'))
>>> my_trp in my_trp_str
False
>>> Trp('E', 'NM', 'Сверло') in my_trp_str
True
```

####Итерация, распаковка
```
>>> for trp in my_trp_str:
	    print(trp)
$E.NM='Сверло';
$E1.NM='Зенкер';
>>> TrpStr(*my_trp_str) == my_trp_str
True
```

####Доступ к элементам триплексной строки по индексу/срезу или по ключу
_Принимает:_

* (str) - ключ

   * ключ формата 'префикс' -> TrpStr с триплетами, имеющими данный префикс
   * ключ формата 'префикс.имя' или '$префикс.имя' -> значение триплета

* (list/tuple)

   * префикс и имя в кортеже (prefix, name) или в списке [prefix, name] -> значение триплета

* иначе - индекс/срез

   * -> TrpStr по заданному индексу/срезу

_Примеры:_
```python
trpStr[2]
trpStr[1:5]
trpStr['E']
trpStr['E.NM']
trpStr['$E.NM']
TrpStr[('E', 'NM')]
TrpStr[['E', 'NM']]
```

####Удалить триплет из триплексной строки по значениям префикса и имени
```
>>> my_trp_str = TrpStr(Trp('E', 'NM', 'Сверло'), Trp('E1', 'NM', 'Зенкер'), Trp('E2', 'NM', 'Отвёртка'))
>>> my_trp_str.del_trp('E', 'NM')
>>> print(my_trp_str)
$E1.NM='Зенкер';$E2.NM='Отвёртка';
```

####Удалить из триплексной строки все триплеты с заданным префиксом
```
>>> my_trp_str = TrpStr(Trp('E', 'NM', 'Сверло'), Trp('E1', 'NM', 'Зенкер'), Trp('Q', 'PI', 3.14))
>>> my_trp_str.del_trp_pref('E')
>>> print(my_trp_str)
$E1.NM='Зенкер';$Q.PI=3.14;
```

##parse_trp_str()
Парсинг триплексной строки из str в TrpStr
_Вернёт параметр str_to_parse без изменений, если он будет TrpStr_

_Принимает:_

* ```str_to_parse``` (str) - строка для парсинга

_Возвращает:_

* (TrpStr) - распарсенная строка

```python
>>> parse_trp_str("$E.NM='Сверло';$E1.NM='Зенкер';")
```

##check_condition()

Функция *check_condition* осуществляет проверку истинности условия, включающего в себя триплеты.

Алгоритм заменяет триплеты, указанные в условии соответствующими значениями, затем проверяет истинность условия. Триплеты, указанные без префикса "$", заменяются соответствующими значениями, указанными в параметре trp_str_from_db

**Принимает:**

* ```trp_str``` (str или TrpStr) - триплексная строка
* ```cond``` (str) - условие
* ```trp_str_from_db``` (str или TrpStr) необязательный - триплексная строка по данным из базы данных

**Возвращает:**

* (bool) - результат проверки условия

**Вызывает исключение TypeError, если:**

* триплескная строка/триплексная строка по данным из БД/условие не является строкой или TrpStr

**Вызывает исключение ValueError, если:**

* получена пустая строка вместо условия
* триплет из условия не найден в триплексной строке или в триплексной строке по данным из БД
* в условии не соблюден баланс скобок

### Примеры работы
**Исходная триплексная строка**
```
$E.NST=1;$E.KRM=1;$E.KTS='211051';$E.VI=35;$Е.NI=1;$L.D=3.5;$L.L=10;$L.KW=12;$L.WOB=27;$M.PGM=3;$O.GRO='20001';$P.SE='221440';$Q.PI=3.14159;$Q.X=0.973;$Q.Y=0.7854;
```

**Триплексная строка по данным из базы**
```
$E.NST=5;$E.KRM=3;$E.KTS=1;$E.VI=325;$Е.NI=1;
```

####Условие I
```
SIN($Q.PI/2)>COS($Q.PI/3)
```
**Результат: True**

####Условие II
```
(SIN($Q.X)*SIN($Q.X)+COS($Q.X)*COS($Q.X))>1
```
**Результат: False**

####Условие III
```
($L.WOB=25 ИЛИ $L.WOB=27) И НЕТ($L.TT)
```
**Результат: True**

####Условие IV
```
$E.KTS='21' И ($O.GRO<>'10000' И $O.GRO<>'10001')
```
**Результат: False**

####Условие V
```
E.NST > 2 И $E.KTS='211051'
```
**Результат: True**

#### Особенности работы

####Функции
_Названия данных функций в условии могут быть определены как в нижнем регистре, так и в верхнем._

* sin
* cos
* tan
* acos
* atan
* sinh
* cosh
* tanh
* sqrt
* exp
* ln
* log
* strcat
* min
* max
* abs
* есть
* нет

####Операторы

* Операторы сравнения: `=`, `==`, `<>`, `!=`, `>`, `<`, `>=`, `<=`
* Логические операторы: `и`, `или`, `and`, `or`
* Математические операторы: `^`, `**`, `*`, `/`, `+`, `-`

_Логические операторы могут быть определены как в нижнем регистре, так и в верхнем. Также они **обязательно** должны быть обособлены пробелами._

##Регулярные выражения

_WODS - without dollar sign ('$')_
_NI - not isolated by '^' and '$'_

* RE_PREFIX - префикс
* RE_NAME - имя
* RE_VALUE - значение
* RE_PREFIX_NAME_WODS_NI - префикс.имя
* RE_PREFIX_NAME_WODS - префикс.имя
* RE_PREFIX_NAME_NI - $префикс.имя
* RE_PREFIX_NAME - $префикс.имя
* RE_TRIPLET_WODS - префикс.имя=значение;
* RE_TRIPLET - $префикс.имя=значение;

_С помощью файла ```support_files\make_regexs.py```_ можно удобно создавать свои регулярные выражения.