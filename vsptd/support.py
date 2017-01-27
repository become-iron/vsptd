# -*- coding: utf-8 -*-
def isfloat(value: str) -> bool:
    """
    Определяет, является ли строка числом с плавающей запятой

    :param str value: строка для определения
    :rtype: bool
    :Пример:
        >>> isfloat('word')
        False
        >>> isfloat('12')
        False
        >>> isfloat('1.2.3')
        False
        >>> isfloat('.05')
        True
        >>> isfloat('42.42')
        True
    """
    try:
        if '.' in value:
            float(value)
            return True
    except ValueError:
        pass
    return False


def type_name(value) -> str:
    """
    Возвращает строковое представление названия класса принимаемого объекта

    :param Any value: объект
    :rtype: str
    :Примеры:
        >>> type_name('abcd')
        'str'
        >>> type_name(4.5)
        'float'
    """
    return value.__class__.__name__


def group(value: str) -> str:
    """
    Обособляет принятую строку скобками для последующего составления RegExp

    :param str value: строка для обособления
    :rtype: str
    """
    return '(' + value + ')'
