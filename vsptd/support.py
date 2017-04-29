# -*- coding: utf-8 -*-
"""Набор функций для использования во внутренней работе пакета."""


def type_name(value) -> str:
    """
    Возвращает строковое представление названия класса принимаемого объекта

    :param Any value: объект
    :rtype: str
    :Пример работы:
        >>> type_name('abcd')
        'str'
        >>> type_name(4.5)
        'float'
    """
    return value.__class__.__name__


def isfloat(value: str) -> bool:
    """
    Определяет, является ли строка числом с плавающей запятой

    :param str value: строка для определения
    :rtype: bool

    :Пример работы:
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
        >>> isfloat('42E-5')
        True
    """
    if any(_ in value for _ in ('.', 'E', 'e')):
        try:
            float(value)
            return True
        except ValueError:
            pass
    return False
