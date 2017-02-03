# -*- coding: utf-8 -*-
"""Дополнительные функции и ВСПТД-объекты."""

from vsptd.vsptd import Trp, TrpStr

__all__ = ('satisfy_bid', 'ordered_trp_str')


def satisfy_bid(bid, source):
    """
    Возвращает триплеты из триплетной строки согласно заявке

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

    if bid.bid:
        if bid.name is None:
            # по префиксу
            return source.getpr(bid.prefix)
        else:
            # по префиксу и имени
            return source.get(bid.prefix, bid.name)
    else:
        raise ValueError


def ordered_trp_str(trp_str):
    """
    Возвращает строковое представление триплетной строки,
    где триплеты лексиграфически упорядочены по префиксу и имени

    :param TrpStr trp_str: триплетная строка
    :rtype: str

    :Пример работы:
        >>> trp_str = TrpStr(Trp('L', 'C', 1), Trp('E', 'T', 'G'), Trp('E', 'A', 42), Trp('Y', 'U', '8'))
        >>> print(ordered_trp_str(trp_str))
        $E.A=42; $E.T='G'; $L.C=1; $Y.U='8';
    """
    if not isinstance(trp_str, TrpStr):
        raise TypeError

    trps_sprtr = TrpStr.settings.trps_sprtr  # разделитель триплетов
    return trps_sprtr.join(str(trp) for trp in sorted(trp_str, key=lambda trp: (trp.prefix, trp.name)))


# def применить настройки ко всем классам

# def expr_to_sql(expr):
#     """
#     Возвращает триплетное выражение в виде sql запроса
#     """
#     pass
