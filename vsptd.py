# -*- coding: utf-8 -*-
""" Работа с ВСПТД в ООП-стиле """

import re

# для реализации функции check_condition
from math import sin, cos, tan, acos, atan, sinh, cosh, tanh, sqrt, exp
from math import log as ln
from math import log10 as log


# обособление рег. выражения знаками начала и конца слова ('^', '$')
def islt_re(x):
    return '^' + x + '$'

_BID = ':'  # заявка (запрос полной информации по заданному объекту, определяемому префиксом)

# WODS - without dollar sign
_RE_PREFIX = '[A-Za-z]+\d*'
_RE_NAME = '[A-Za-z]+'
_RE_VALUE = r'\'?[A-Za-zА-Яа-я0-9 :?\.]*\'?'
_RE_PREFIX_NAME_WODS = _RE_PREFIX + '\.' + _RE_NAME
_RE_PREFIX_NAME = '\$' + _RE_PREFIX_NAME_WODS
_RE_TRIPLET_WODS = '(' + _RE_PREFIX + ')\.(' + _RE_NAME + ')=(' + _RE_VALUE + ');'
_RE_TRIPLET = '\$' + _RE_TRIPLET_WODS

RE_PREFIX = re.compile(islt_re(_RE_PREFIX))  # префикс: 1 латинский символ
RE_NAME = re.compile(islt_re(_RE_NAME))  # имя: латинские символы и, возможно, число
RE_VALUE = re.compile(islt_re(_RE_VALUE))  # значение
RE_PREFIX_NAME_WODS = re.compile(islt_re(_RE_PREFIX_NAME_WODS))  # префикс.имя
RE_PREFIX_NAME = re.compile(islt_re(_RE_PREFIX_NAME))  # $префикс.имя
RE_TRIPLET = re.compile(_RE_TRIPLET)  # триплет


class Trp:
    """
    ТРИПЛЕТ
    Принимает:
        prefix (str) - префикс (1 латинский символ)
        name (str) - имя параметра (латинские символы)
        value - значение параметра
    """
    def __init__(self, prefix, name, value=''):
        if not isinstance(prefix, str):
            raise ValueError('Префикс должен быть строкой')
        if not isinstance(name, str):
            raise ValueError('Имя должно быть строкой')
        if not isinstance(value, (str, int, float, Trp, TrpStr)):
            raise ValueError('Значение должно быть строкой, числом, триплетом или триплексной строкой')
        if re.match(RE_PREFIX, prefix) is None:
            raise ValueError('Неверный формат префикса: ' + prefix)
        if re.match(RE_NAME, name) is None:
            raise ValueError('Неверный формат имени: ' + name)
        # TODO может быть и не строкой (следует уточнить)
        # if isinstance(value, str) and value != _BID and re.match(RE_VALUE, value) is None:
        #     raise ValueError

        # префикс и имя приводятся к верхнему регистру
        self.prefix = prefix.upper()
        self.name = name.upper()
        self.value = value

    def __str__(self):
        _ = '${}.{}='.format(self.prefix, self.name)
        if self.value == _BID:
            _ += _BID
        elif isinstance(self.value, str):
            _ += '\'{}\''.format(self.value)
        else:
            _ += str(self.value)
        _ += ';'
        return _

    def __add__(self, other):
        if isinstance(other, Trp):
            return TrpStr(self, other)
        if isinstance(other, TrpStr):
            return TrpStr(self, *other)
        else:
            raise ValueError

    def __eq__(self, other):
        return isinstance(other, Trp) and \
               self.name == other.name and \
               self.prefix == other.prefix and \
               self.value == other.value


class TrpStr:
    """
    ТРИПЛЕКСНАЯ СТРОКА
    Принимает:
        *triplets (Triplet) - триплеты
    """
    def __init__(self, *triplets):
        # TODO добавить возможность создания строки по списку/кортежу
        for _ in triplets:  # CHECK проверить скорость работы через filter
            if not isinstance(_, Trp):
                raise ValueError('Аргументы должны быть триплетами')
        self.triplets = list(triplets)

        # удаление повторов триплетов (по префиксам и именам)
        for trp in self.triplets.copy():
            # триплеты с данными префиксами и именами
            triplets_to_remove = [_trp for _trp in self.triplets if trp.prefix == _trp.prefix and trp.name == _trp.name]
            triplets_to_remove = triplets_to_remove[:-1]  # исключение последнего найденного триплета
            for rem_trp in triplets_to_remove:
                self.triplets.remove(rem_trp)

    def __len__(self):
        return len(self.triplets)

    def __add__(self, other):
        if isinstance(other, Trp):
            return TrpStr(*(self.triplets + [other]))
        elif isinstance(other, TrpStr):
            return TrpStr(*(self.triplets + other.triplets))
        else:
            raise ValueError('Должен быть триплет или триплексная строка')

    def __str__(self):
        return ''.join(tuple(str(trp) for trp in self.triplets))

    def __contains__(self, item):
        # TODO возможно, стоит включить возможность проверки включения по префиксу и имени
        if not isinstance(item, Trp):
            raise ValueError('Должен быть триплет')

        for trp in self.triplets:
            if trp.prefix == item.prefix and \
               trp.name == item.name and \
               trp.value == item.value:
                return True
        return False

    def __getitem__(self, key):
        """
        ДОСТУП К ЭЛЕМЕНТАМ ТРИПЛ. СТРОКИ ПО КЛЮЧУ ИЛИ СРЕЗУ
        (str) - ключ
            ключ формата префикса -> TripletString из триплетов с данным префиксом
            ключ формата 'префикс.имя' или '$префикс.имя' -> значение триплета
        иначе - индекс/срез

        Примеры:
            trpStr[1:5]
            trpStr['E']
            trpStr['E.NM'] или trpStr['$E.NM']
        """
        # TODO CHECK
        # TODO добавить возможность приема ключа в виде списка и триплета
        if isinstance(key, str):  # элемент по ключу
            # получить триплеты по префиксу в виде триплесной строки
            if re.match(RE_PREFIX, key) is not None:
                return TrpStr(*[trp for trp in self.triplets if trp.prefix == key])
            # получить значение триплета по префиксу и имени
            elif (re.match(RE_PREFIX_NAME_WODS, key) is not None) or (re.match(RE_PREFIX_NAME, key) is not None):
                if key.startswith('$'):
                    key = key[1:]
                key = key.upper().split('.')
                for trp in self.triplets:
                    if trp.prefix == key[0] and trp.name == key[1]:
                        return trp.value
                return None  # если ничего не найдено
        # получить триплексную строку по срезу/индексу
        # CHECK
        # WARN не противоречит ли ВСПТД?
        else:
            return TrpStr(*self.triplets[key])

    def __eq__(self, other):
        # CHECK возможно, стоит замерить скорость работы
        if not isinstance(other, TrpStr):
            raise ValueError

        if len(self.triplets) != len(other):
            return False
        for triplet in other:
            if triplet not in self.triplets:
                return False
        return True

    def __iter__(self):
        return iter(self.triplets)

    def add(self, other):
        """
        СЛОЖЕНИЕ ТРИПЛЕКСНОЙ СТРОКИ С ТРИПЛЕКСНОЙ СТРОКОЙ ИЛИ ТРИПЛЕТОМ
        Эквивалентно сложению через оператор "+"
        Принимает:
            other (TriplexString или Triplet) - триплексная строка или триплет
        Возвращает:
            (TriplexString)
        """
        return self.__add__(other)

    def del_trp(self, prefix, name):
        # CHECK
        """
        УДАЛИТЬ ТРИПЛЕТ ИЗ ТРИПЛЕКСНОЙ СТРОКИ
        Принимает:
            prefix (str) - префикс (1 латинский символ)
            name (str) - имя параметра (латинские символы)
        Вызывает исключение ValueError, если триплет не найден
        """
        if not isinstance(prefix, str):
            raise ValueError('Префикс должен быть строкой')
        if not isinstance(name, str):
            raise ValueError('Имя должно быть строкой')
        if re.match(RE_PREFIX, prefix) is None:
            raise ValueError('Неверный формат префикса')
        if re.match(RE_NAME, name) is None:
            raise ValueError('Неверный формат имени')

        for trp in self.triplets:
            if trp.prefix == prefix and trp.name == name:
                self.triplets.remove(trp)
                return
        raise ValueError('Триплет не найден')

    def del_trp_pref(self, prefix):
        # CHECK
        """
        УДАЛИТЬ ВСЕ ТРИПЛЕТЫ С ЗАДАННЫМ ПРЕФИКСОМ ИЗ ТРИПЛЕКСНОЙ СТРОКИ
        Принимает:
            prefix (str) - префикс
        """
        if not isinstance(prefix, str):
            raise ValueError('Должен быть триплет')

        for trp in self.triplets:
            if trp.prefix == prefix:
                self.triplets.remove(trp)


def _determine_value(value):
    """ОПРЕДЕЛЕНИЕ ТИПА ЗНАЧЕНИЯ"""
    if value in ('True', 'False'):  # булево значение
        return bool(value)
    elif value.startswith('\'') and value.endswith('\''):  # строка
        return value[1:-1]
    # elif val.startswith('$') and val.endswith(';'):  # TODO триплет
    #     pass
    elif value == _BID:  # заявка
        return _BID
    else:  # число
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            raise ValueError('Неверное значение триплета')


def parse_triplex_string(trp_str):
    """ПАРСИНГ ТРИПЛЕКСНОЙ СТРОКИ ИЗ str В TriplexString"""
    trp_str = re.findall(RE_TRIPLET, trp_str)
    tmp_trp_str = []
    for trp in trp_str:
        value = _determine_value(trp[2])
        tmp_trp_str += [Trp(trp[0], trp[1], value)]
    return TrpStr(*tmp_trp_str)


# ======= РЕАЛИЗАЦИЯ ФУНКЦИИ ВЫЧИСЛЕНИЯ УСЛОВИЯ В ПРАВИЛЕ ВЫВОДА =======

RE_PREFIX_NAME_WODS_NI = re.compile(_RE_PREFIX_NAME_WODS)  # префикс.имя
RE_PREFIX_NAME_NI = re.compile(_RE_PREFIX_NAME)  # $префикс.имя
RE_TRIPLET_WODS = re.compile(_RE_TRIPLET_WODS)  # триплет без $
RE_FUNC_PRESENT = re.compile('(?:есть|ЕСТЬ)\(\$[A-Za-z]\.[A-Za-z]+\)')  # функция ЕСТЬ
RE_FUNC_PRESENT_WODS = re.compile('(?:есть|ЕСТЬ)\([A-Za-z]\.[A-Za-z]+\)')  # функция ЕСТЬ без $
RE_FUNC_ABSENCE = re.compile('(?:нет|НЕТ)\(\$[A-Za-z]\.[A-Za-z]+\)')  # функция НЕТ
RE_FUNC_ABSENCE_WODS = re.compile('(?:нет|НЕТ)\([A-Za-z]\.[A-Za-z]+\)')  # функция НЕТ без $
RE_SLICE = re.compile('(\[(\d+),(\d+)\])')  # срез [n,n]


def strcat(a, b):
    return a + b


def check_condition(trp_str, condition, trp_str_from_db=''):
    # WARN используется небезопасный алгоритм, который также может не всегда верно работать
    """
    ПРОВЕРКА ТРИПЛЕКСНОЙ СТРОКИ НА УСЛОВИЕ
    Алгоритм заменяет триплеты, указанные в условии соответствующими значениями, затем
    проверяет истинность условия. Триплеты, указанные без префикса "$", заменяются
    соответствующими значениями, указанными в параметре trpStringFromDB
    Принимает:
        trpString (str) - триплексная строка
        condition (str) - условие
        trpStringFromDB (str) необязательный - триплексная строка по данным из базы данных
    Возвращает:
        (bool) - результат проверки условия
    Вызывает исключение ValueError, если:
        триплескная строка или условие не является строкой
        получена пустая строка вместо триплексной строки или условия
        триплет из условия не найден в триплексной строке
        в условии не соблюден баланс скобок
    """
    if not isinstance(trp_str, str) or not isinstance(trp_str_from_db, str):
        raise ValueError('Триплексная строка должна быть строкой')
    if not isinstance(condition, str):
        raise ValueError('Условие должно быть строкой')
    if len(trp_str) == 0:
        raise ValueError('Пустая строка')
    if len(condition) == 0:
        raise ValueError('Пустое условие')

    trp_str = parse_triplex_string(trp_str)
    trp_str_from_db = parse_triplex_string(trp_str_from_db)

    # замена операторов
    # WARN возможна неверная замена
    # например, замена слов произойдёт, даже если в условии происходит
    # сравнение со строкой, содержащей слово на замену
    # $W.B = ' или '
    replacements = [[' или ', ' or '],
                    [' и ', ' and '],
                    [' ИЛИ ', ' or '],
                    [' И ', ' and '],
                    ['=', '=='],
                    ['<>', '!='],
                    ['^', '**']]
    for rplc in replacements:
        condition = condition.replace(rplc[0], rplc[1])

    # переводим названия функций в нижний регистр
    func_replacements = ('sin', 'cos', 'tan', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
                         'sqrt', 'exp', 'ln', 'log', 'strcat', 'min', 'max', 'abs')
    for rplc in func_replacements:
        condition = condition.replace(rplc.upper(), rplc)

    # замены для функций ЕСТЬ и НЕТ
    # TODO
    # поиск триплетов в трипл. строке
    for trp in re.findall(RE_FUNC_PRESENT, condition):  # функция ЕСТЬ
        item = trp[6:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
        value = False
        for triplet in trp_str.triplets:
            if [triplet.prefix, triplet.name] == item:
                value = True
                break
        condition = condition.replace(trp, str(value))
    for trp in re.findall(RE_FUNC_ABSENCE, condition):  # функция НЕТ
        item = trp[5:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
        value = False
        for triplet in trp_str.triplets:
            if [triplet.prefix, triplet.name] == item:
                value = True
                break
        condition = condition.replace(trp, str(not value))

    # поиск триплетов в трипл. строке по данным из базы
    if len(trp_str_from_db) > 0:
        for trp in re.findall(RE_FUNC_PRESENT_WODS, condition):  # функция ЕСТЬ
            item = trp[5:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
            value = False
            for triplet in trp_str_from_db.triplets:
                if [triplet.prefix, triplet.name] == item:
                    value = True
                    break
            condition = condition.replace(trp, str(value))
        for trp in re.findall(RE_FUNC_ABSENCE_WODS, condition):  # функция НЕТ
            item = trp[4:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
            value = False
            for triplet in trp_str_from_db.triplets:
                if [triplet.prefix, triplet.name] == item:
                    value = True
                    break
            condition = condition.replace(trp, str(not value))

    # поиск триплетов
    for trp in re.findall(RE_PREFIX_NAME_NI, condition):  # замена триплетов на их значения
        value = trp_str.__getitem__(trp[1:])  # получаем значение триплета
        if value is None:
            raise ValueError('Триплет {} не найден в триплексной строке'.format(trp))
        value = '\'' + value + '\'' if isinstance(value, str) else str(value)  # приводим к формату значений триплета
        condition = condition.replace(trp, value)

    # поиск триплетов в строке по данным из базы
    for trp in re.findall(RE_PREFIX_NAME_WODS_NI, condition):  # замена триплетов на их значения
        value = trp_str_from_db.__getitem__(trp)  # получаем значение триплета
        if value is None:
            raise ValueError('Триплет {} не найден в триплескной строке из базы'.format(trp))
        value = '\'' + value + '\'' if isinstance(value, str) else str(value)  # приводим к формату значений триплета
        condition = condition.replace(trp, value)

    # поиск срезов
    # CHECK
    for rplc in re.findall(RE_SLICE, condition):
        _ = str(int(rplc[1]) - 1)
        __ = str(int(rplc[1]) + int(rplc[2]))
        condition.replace(rplc[0], '[{}:{}]'.format(_, __))

    # проверка баланса скобок
    if condition.count('(') != condition.count(')'):
        raise ValueError('Не соблюден баланс скобок')

    # print('Конечное выражение: ', condition, sep='')
    return eval(condition)
