# -*- coding: utf-8 -*-
""" Работа с ВСПТД в ООП-стиле """

import re

__version__ = '1.4.0'

# для реализации функции check_condition
from math import sin, cos, tan, acos, atan, sinh, cosh, tanh, sqrt, exp
from math import log as ln
from math import log10 as log


# WODS - without dollar sign ('$')
# NI - not isolated by '^' and '$'
# TODO проверить целесообразность необособленных выражений
RE_PREFIX = re.compile(r"^[A-Za-z]+\d*$")  # префикс
RE_NAME = re.compile(r"^[A-Za-z]+$")  # имя
RE_VALUE = re.compile(r"^\'?[A-Za-zА-Яа-яЁё0-9 :?.()]*\'?$")  # значение
RE_PREFIX_NAME_WODS_NI = re.compile(r"[A-Za-z]+\d*\.[A-Za-z]+")  # префикс.имя
RE_PREFIX_NAME_WODS = re.compile(r"^[A-Za-z]+\d*\.[A-Za-z]+$")  # префикс.имя
RE_PREFIX_NAME_NI = re.compile(r"\$[A-Za-z]+\d*\.[A-Za-z]+")  # $префикс.имя
RE_PREFIX_NAME = re.compile(r"^\$[A-Za-z]+\d*\.[A-Za-z]+$")  # $префикс.имя
RE_TRIPLET_WODS = re.compile(r"([A-Za-z]+\d*)\.([A-Za-z]+)=(\'?[A-Za-zА-Яа-яЁё0-9 :?.()]*\'?);")  # префикс.имя=значение;
RE_TRIPLET = re.compile(r"\$([A-Za-z]+\d*)\.([A-Za-z]+)=(\'?[A-Za-zА-Яа-яЁё0-9 :?.()]*\'?);")  # $префикс.имя=значение;


class Trp:
    """
    ТРИПЛЕТ
    Принимает:
        prefix (str) - префикс триплета
        name (str) - имя триплета
        value (str, int, float) - значение триплета
    """
    # WARN не реализованы случаи, когда значение является триплетом или трипл. строкой
    def __init__(self, prefix, name, value=''):
        if not isinstance(prefix, str):
            raise TypeError('Префикс должен быть строкой: ' + str(prefix))
        if not isinstance(name, str):
            raise TypeError('Имя должно быть строкой: ' + str(name))
        if not isinstance(value, (str, int, float)):
            raise TypeError('Значение должно быть строкой или числом: ' + str(value))
        if re.match(RE_PREFIX, prefix) is None:
            raise ValueError('Неверный формат префикса: ' + prefix)
        if re.match(RE_NAME, name) is None:
            raise ValueError('Неверный формат имени: ' + name)
        if isinstance(value, str) and re.match(RE_VALUE, value) is None:
            raise ValueError('Неверный формат значения: ' + value)

        # префикс и имя приводятся к верхнему регистру
        self.prefix = prefix.upper()
        self.name = name.upper()
        self.value = value

    def __str__(self):
        _ = '$' + self.prefix + '.' + self.name + '='
        if isinstance(self.value, str):
            _ += "'" + self.value + "'"
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
            raise TypeError('Должен быть триплет или триплексная строка')

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
        for trp in triplets:  # CHECK проверить скорость работы через filter
            if not isinstance(trp, Trp):
                raise TypeError('Должны быть триплеты')
        self.triplets = list(triplets)

        # удаление повторов триплетов (по префиксам и именам)
        for trp in self.triplets.copy():
            triplets_to_remove = [_trp for _trp in self.triplets if trp.prefix == _trp.prefix and trp.name == _trp.name]
            # исключение из списка на удаление последнего найденного триплета, который и останется в трипл. строке
            triplets_to_remove = triplets_to_remove[:-1]
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
            raise TypeError('Должен быть триплет или триплексная строка')

    def __str__(self):
        return ''.join(tuple(str(trp) for trp in self.triplets))

    def __contains__(self, item):
        """
        ПРОВЕРКА ВХОЖДЕНИЯ ТРИПЛЕТА В ТРИПЛ. СТРОКУ
        Пример:
            Trp in TrpStr
        """
        # TODO возможно, стоит включить возможность проверки включения по префиксу и имени
        if not isinstance(item, Trp):
            raise TypeError('Должен быть триплет')

        for trp in self.triplets:
            if trp.prefix == item.prefix and \
               trp.name == item.name and \
               trp.value == item.value:
                return True
        return False

    def __getitem__(self, key):
        """
        ДОСТУП К ЭЛЕМЕНТАМ ТРИПЛ. СТРОКИ ПО КЛЮЧУ ИЛИ СРЕЗУ
        Принимает:
            (str) - ключ
                ключ формата 'префикс' -> TrpStr с триплетами, имеющими данный префикс
                ключ формата 'префикс.имя' или '$префикс.имя' -> значение триплета
            (list/tuple)
                префикс и имя в кортеже (prefix, name) или в списке [prefix, name] -> значение триплета
            иначе - индекс/срез
                -> TrpStr по заданному индексу/срезу

        Примеры:
            TrpStr[2]
            TrpStr[1:5]
            TrpStr['E']
            TrpStr['E.NM'] или trpStr['$E.NM']
            TrpStr[('E', 'NM')] или TrpStr[['E', 'NM']]
        """
        # TODO CHECK
        # TODO добавить возможность приема ключа в виде списка и триплета
        if isinstance(key, str):  # элемент по ключу
            key = key.upper()
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

        # получить значение триплета по префиксу и имени, записанным в списке/кортеже: (prefix, name)
        elif isinstance(key, (tuple, list)):
            prefix, name = key
            prefix = prefix.upper()
            name = name.upper()
            for trp in self.triplets:
                if trp.prefix == prefix and trp.name == name:
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
            return False

        if len(self.triplets) != len(other):
            return False
        # WARN не обрабатывается случай, когда вторая трипл. строка является подмножеством первой
        for triplet in other:
            if triplet not in self.triplets:
                return False
        return True

    def __iter__(self):
        return iter(self.triplets)

    def add(self, other):
        """СЛОЖЕНИЕ ТРИПЛЕКСНОЙ СТРОКИ С ТРИПЛЕКСНОЙ СТРОКОЙ ИЛИ ТРИПЛЕТОМ
        Практически эквивалентно сложению через оператор "+". Отличие в том, что данный метод не возвращает новый
        изменённый объект, а только изменяет нынешний.
        Принимает:
            other (TrpStr или Trp) - триплексная строка или триплет
        Примеры:
            TtpStr + Trp
            TrpStr + TrpStr
        """
        self.triplets = self.__add__(other).triplets

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
            raise TypeError('Префикс должен быть строкой')
        if not isinstance(name, str):
            raise TypeError('Имя должно быть строкой')
        if re.match(RE_PREFIX, prefix) is None:
            raise ValueError('Неверный формат префикса')
        if re.match(RE_NAME, name) is None:
            raise ValueError('Неверный формат имени')

        prefix = prefix.upper()
        name = name.upper()

        for trp in self.triplets:
            if trp.prefix == prefix and trp.name == name:
                self.triplets.remove(trp)
                return
        raise ValueError('Триплет не найден')

    def del_trp_pref(self, prefix):
        # CHECK
        """
        УДАЛИТЬ ИЗ ТРИПЛЕКСНОЙ СТРОКИ ВСЕ ТРИПЛЕТЫ С ЗАДАННЫМ ПРЕФИКСОМ
        Принимает:
            prefix (str) - префикс
        """
        if not isinstance(prefix, str):
            raise TypeError('Должен быть триплет')

        prefix = prefix.upper()

        for trp in self.triplets:
            if trp.prefix == prefix:
                self.triplets.remove(trp)


def parse_trp_str(str_to_parse):
    """
    ПАРСИНГ ТРИПЛЕКСНОЙ СТРОКИ ИЗ str В TrpStr
    Вернёт параметр str_to_parse без изменений, если он будет TrpStr
    Принимает:
        str_to_parse (str) - строка для парсинга
    Возвращает:
        (TrpStr) - распарсенная строка
    """
    if isinstance(str_to_parse, TrpStr):
        return TrpStr

    str_to_parse = re.findall(RE_TRIPLET, str_to_parse)
    tmp_trp_str = []
    for trp in str_to_parse:
        value = _determine_value(trp[2])
        tmp_trp_str += [Trp(trp[0], trp[1], value)]
    return TrpStr(*tmp_trp_str)


def _determine_value(value):
    """ОПРЕДЕЛЕНИЕ ТИПА ЗНАЧЕНИЯ ТРИПЛЕТА"""
    # TODO определение триплета, трипл. строки
    # булево значение
    if value == 'True':
        return True
    elif value == 'False':
        return False
    # строка
    elif value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    # число
    else:
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            raise ValueError('Неверное значение триплета: ' + value)


# ======= РЕАЛИЗАЦИЯ ФУНКЦИИ ВЫЧИСЛЕНИЯ УСЛОВИЯ В ПРАВИЛЕ ВЫВОДА =======

RE_FUNC_PRESENT = re.compile(r'(?:есть|ЕСТЬ)\(\$[A-Za-z]+\d*\.[A-Za-z]+\)')  # функция ЕСТЬ
RE_FUNC_PRESENT_WODS = re.compile(r'(?:есть|ЕСТЬ)\([A-Za-z]+\d*\.[A-Za-z]+\)')  # функция ЕСТЬ без $
RE_FUNC_ABSENCE = re.compile(r'(?:нет|НЕТ)\([A-Za-z]+\d*\.[A-Za-z]+\)')  # функция НЕТ
RE_FUNC_ABSENCE_WODS = re.compile(r'(?:нет|НЕТ)\([A-Za-z]+\d*\.[A-Za-z]+\)')  # функция НЕТ без $
RE_SLICE = re.compile(r'(\[(\d+),(\d+)\])')  # срез [n,n]


# функция, определённая в ВСПТД
def strcat(a, b):
    return a + b


def check_condition(cond, trp_str='', trp_str_from_db=''):
    # WARN используется небезопасный алгоритм, который также может не всегда верно работать
    # WARN потенциальная опасность заключена в использовании функции eval
    """
    ПРОВЕРКА ИСТИННОСТИ УСЛОВИЯ, ВКЛЮЧАЮЩЕГО В СЕБЯ ТРИПЛЕТЫ
    Алгоритм заменяет триплеты, указанные в условии соответствующими значениями, затем
    проверяет истинность условия. Триплеты, указанные без префикса "$", заменяются
    соответствующими значениями, указанными в параметре trp_str_from_db
    Принимает:
        cond (str) - условие
        trp_str (str или TrpStr) необяз.- триплексная строка
        trp_str_from_db (str или TrpStr) необяз. - триплексная строка по данным из БД
    Возвращает:
        (bool) - результат проверки условия
    Вызывает исключение TypeError, если:
        триплескная строка/триплексная строка по данным из БД/условие не является строкой или TrpStr
    Вызывает исключение ValueError, если:
        получена пустая строка вместо условия
        триплет из условия не найден в триплексной строке или в триплексной строке по данным из БД
        в условии не соблюден баланс скобок
    """
    if not isinstance(trp_str, (str, TrpStr)):
        raise TypeError('Триплексная строка должна быть строкой или TrpStr')
    if not isinstance(trp_str_from_db, (str, TrpStr)):
        raise TypeError('Триплексная строка должна быть строкой или TrpStr')
    if not isinstance(cond, str):
        raise TypeError('Условие должно быть строкой')
    if len(cond) == 0:
        raise ValueError('Пустое условие')

    # проверка баланса скобок
    if cond.count('(') != cond.count(')'):
        raise ValueError('Не соблюден баланс скобок')

    # замена операторов
    # WARN возможна неверная замена
    # WARN например, замена слов произойдёт, даже если в условии происходит
    # WARN сравнение со строкой, содержащей слово на замену
    # WARN $W.B = ' или '
    replacements = [[' или ', ' or '],
                    [' и ', ' and '],
                    [' ИЛИ ', ' or '],
                    [' И ', ' and '],
                    ['=', '=='],
                    ['<>', '!='],
                    ['^', '**']]
    for rplc in replacements:
        cond = cond.replace(rplc[0], rplc[1])

    # переводим названия функций в нижний регистр
    func_replacements = ('sin', 'cos', 'tan', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
                         'sqrt', 'exp', 'ln', 'log', 'strcat', 'min', 'max', 'abs')
    for rplc in func_replacements:
        cond = cond.replace(rplc.upper(), rplc)

    if isinstance(trp_str, str):
        trp_str = parse_trp_str(trp_str)
    if isinstance(trp_str_from_db, str):
        trp_str_from_db = parse_trp_str(trp_str_from_db)

    # замены для функций ЕСТЬ и НЕТ
    # TODO оптимизировать
    for trp in re.findall(RE_FUNC_PRESENT, cond):  # функция ЕСТЬ
        item = trp[6:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
        value = False
        for triplet in trp_str.triplets:
            if [triplet.prefix, triplet.name] == item:
                value = True
                break
        cond = cond.replace(trp, str(value))
    for trp in re.findall(RE_FUNC_ABSENCE, cond):  # функция НЕТ
        item = trp[5:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
        value = False
        for triplet in trp_str.triplets:
            if [triplet.prefix, triplet.name] == item:
                value = True
                break
        cond = cond.replace(trp, str(not value))
    if len(trp_str_from_db) > 0:
        for trp in re.findall(RE_FUNC_PRESENT_WODS, cond):  # функция ЕСТЬ
            item = trp[5:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
            value = False
            for triplet in trp_str_from_db.triplets:
                if [triplet.prefix, triplet.name] == item:
                    value = True
                    break
            cond = cond.replace(trp, str(value))
        for trp in re.findall(RE_FUNC_ABSENCE_WODS, cond):  # функция НЕТ
            item = trp[4:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
            value = False
            for triplet in trp_str_from_db.triplets:
                if [triplet.prefix, triplet.name] == item:
                    value = True
                    break
            cond = cond.replace(trp, str(not value))

    # поиск триплетов
    for trp in re.findall(RE_PREFIX_NAME_NI, cond):  # замена триплетов на их значения
        value = trp_str[trp[1:]]  # получаем значение триплета
        if value is None:
            raise ValueError('Триплет {} не найден в триплексной строке'.format(trp))
        value = "'" + value + "'" if isinstance(value, str) else str(value)  # приводим к формату значений триплета
        cond = cond.replace(trp, value)

    # поиск триплетов в строке по данным из базы
    for trp in re.findall(RE_PREFIX_NAME_WODS_NI, cond):  # замена триплетов на их значения
        value = trp_str_from_db[trp]  # получаем значение триплета
        if value is None:
            raise ValueError('Триплет {} не найден в триплескной строке по данным из БД'.format(trp))
        value = "'" + value + "'" if isinstance(value, str) else str(value)  # приводим к формату значений триплета
        cond = cond.replace(trp, value)

    # поиск срезов
    # CHECK
    for rplc in re.findall(RE_SLICE, cond):
        # перевод индексов среза из формата ВСПТД
        i = str(int(rplc[1]) - 1)
        j = str(int(rplc[1]) + int(rplc[2]))
        cond.replace(rplc[0], '[{}:{}]'.format(i, j))

    return eval(cond)
