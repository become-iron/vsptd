# -*- coding: utf-8 -*-
"""Дополнительные функции и ВСПТД-объекты."""

from collections import OrderedDict

from vsptd.vsptd import Trp, TrpStr
from vsptd.support import type_name

__all__ = ('satisfy_bid', 'eq_with_order', 'VSPTDTechProcTable',)


def satisfy_bid(bid, source):
    """
    Возвращает триплет/триплетную строку из триплетной строки согласно заявке

    Данная функция представляет собой более высокоуровневый
    инструмент, чем методы ``get``, ``getpr`` класса ``TrpStr``.

    :Примечания:
        * Свойство ``bid`` триплета, используемого в качестве
          параметра ``bid``, должно быть равно ``True``.

    :param Trp bid: триплет с заявкой
    :param TrpStr source: триплетная строка, где будет производиться поиск
    :return: ``Trp`` или ``TrpStr``

    :Пример работы:
        >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'R', 'H'))
        >>> print(satisfy_bid(Trp('A', bid=True), my_trp_str))
        $A.B='C'; $A.R='H';
        >>> print(satisfy_bid(Trp('A', 'B', bid=True), my_trp_str))
        $A.B='C';
    """
    if not isinstance(bid, Trp):
        raise TypeError
    if not isinstance(source, TrpStr):
        raise TypeError

    # TODO: использовать параметр по умолчанию
    if bid.bid:
        if bid.name is None:
            # по префиксу
            return source.getpr(bid.prefix)
        else:
            # по префиксу и имени
            return source.get(bid.prefix, bid.name)
    else:
        raise ValueError


def eq_with_order(first, second) -> bool:
    """
    Проверяет на равенство триплетные строки с учётом порядка триплетов

    :param TrpStr first:
    :param TrpStr second:
    :rtype: bool
    """
    if not isinstance(first, TrpStr) or not isinstance(second, TrpStr):
        raise TypeError

    return len(first) == len(second) and all(trp == trp2 for trp, trp2 in zip(first, second))


class VSPTDTechProcTable:
    """
    Таблица для хранения триплексных строк, содержащих информацию по технологическим процессам.
    Для каждой строки высчитывается первичный ключ

    Принимает:
        - `*trp_strs` (TrpStr): триплексные строки
    """
    #: Настройки для вычисления первичного ключа, (префикс, имя, длина)
    primary_key_setts = (
        # (prefix, name, length),
        ('A', 'N', 4),
        ('P', 'N', 3),
        ('P', 'KWO', 3),
        ('Q', 'DI', 2),
    )

    def __init__(self, *trp_strs):
        def check_type(trp):
            # для проверки, все ли аргументы — триплетные строки
            if isinstance(trp, TrpStr):
                return True
            else:
                raise TypeError('Должен быть TrpStr, не ' + type_name(trp), trp)
        self._items = OrderedDict(
            {self.calc_primary_key(trp_str): trp_str for trp_str in trp_strs if check_type(trp_str)}
        )

    def add(self, trp_str):
        """Добавляет триплексную строку в """
        if not isinstance(trp_str, TrpStr):
                raise TypeError

        self._items.update({self.calc_primary_key(trp_str): trp_str})

    def calc_primary_key(self, trp_str):
        """Вычисляет первичный ключ для принятой триплексной строки"""
        # TODO: если значение триплета - None, можно использовать просто заполненную нулями строку
        return ''.join(
            str(trp_str.get(prefix, name).value).zfill(len_)
            for prefix, name, len_ in self.primary_key_setts
        )

    def __str__(self):
        # TODO: определить формат
        return ' || '.join('{0}: {1}'.format(key, trp_str) for key, trp_str in self._items.items())

    def __repr__(self):
        return 'VSPTDTechProcTable(' + \
               ', '.join('{0!r}'.format(trp_str) for trp_str in self._items.values()) + \
               ')'

    def __getitem__(self, key):
        """Возвращает по первичному ключу триплексную строку"""
        return self._items[key]

    def __delitem__(self, key):
        """Удаляет по первичному ключу триплексную строку"""
        del self._items[key]

    def __iter__(self):
        yield from self._items.items()

    def __len__(self):
        return len(self._items)
