# -*- coding: utf-8 -*-
import re

from vsptd.vsptd import Trp, TrpStr, TrpExpr, VSPTDSettings
from vsptd.support import isfloat, type_name, group

__all__ = ('VSPTDParse', 'parse_trp', 'parse_trp_str', 'parse_trp_expr')


# noinspection SpellCheckingInspection
class VSPTDParse:
    """
    **Регулярные выражения для разбора строк**

    Класс обеспечивает удобный интерфейс генерации регулярных выражений для разбора строк.

    :Примечания:
        * представленные выражения не обеспечивают валидацию,
        * свойства недоступны для изменений;
        * для пересчёта выражений необходимо заново создать экземпляр класса.
    :param settings:  настройки конфигурации ВСПТД; по умолчанию используются стандартные
    :type settings: VSPTDSettings, необяз.
    """
    def __init__(self, settings=VSPTDSettings()):
        self.settings = settings  #: настройки конфигурации ВСПТД :class:`VSPTDSettings`

        __word = group('\w+')  # Буквенный или цифровой символ или знак подчёркивания, >= 1 раз, группированный
        __any = group('.*?')  # Любой символ, >= 0 раз, группированный, ленивый

        trp_start = settings.trp_start
        trp_pn_sprtr = settings.trp_pn_sprtr
        trp_nv_sprtr = settings.trp_nv_sprtr
        trp_comment_isltr = settings.trp_comment_isltr
        trp_end = settings.trp_end
        trps_sprtr = settings.trps_sprtr

        self.__re_trp_ref_special = __word + re.escape(trp_pn_sprtr) + __word

        self.__re_trp_ref = re.escape(trp_start) + self.re_trp_ref_special

        # WARN попадут и комментарии
        self.__re_trp_special = self.re_trp_ref_special + re.escape(trp_nv_sprtr) + __any + re.escape(trp_end)

        self.__re_trp = self.__re_trp_ref \
            + re.escape(trp_nv_sprtr) + __any \
            + group('?:' + re.escape(trp_comment_isltr) + __any + re.escape(trp_comment_isltr)) + '?' \
            + re.escape(trp_end)

        self.__re_trps = self.__re_trp + re.escape(trps_sprtr) + '?'

        # TODO
        # self.__re_trp_expr =

    re_trp_ref_special = property(lambda self: self.__re_trp_ref_special)  #: RegExp для разбора строки: ``P.N``
    re_trp_ref = property(lambda self: self.__re_trp_ref)  #: RegExp для разбора строки: ``$P.N``
    re_trp_special = property(lambda self: self.__re_trp_special)  #: RegExp для разбора строки: ``P.N=V;``
    re_trp = property(lambda self: self.__re_trp)  #: RegExp для разбора строки: ``$P.N=V"C";``
    re_trps = property(lambda self: self.__re_trps)  #: RegExp для разбора строки на триплетную строку

    def __repr__(self):
        return '<%s>' % VSPTDParse.__name__


def parse_trp():
    # TODO
    pass


# noinspection SpellCheckingInspection
def parse_trp_str(str_to_parse: str, parse_settings=VSPTDParse()):
    """
    Разбирает строку на триплеты и возвращает триплетную строку

    :Примечания:
        * функцией можно парсить и триплеты, но вернётся всё равно триплетная строка :class:`TrpStr`;
        * вернёт параметр `str_to_parse` без изменений, если он будет :class:`TrpStr`.
    :param str str_to_parse: строка для парсинга
    :param parse_settings:  настройки конфигурации ВСПТД; по умолчанию используются стандартные
    :type parse_settings: VSPTDParse, необяз.
    :rtype: TrpStr
    :raises TypeError: если `str_to_parse` не `str` и не :class:`TrpStr`
    :raises ValueError: неверный формат значения триплета
    """
    # noinspection SpellCheckingInspection
    def _determine_value(value):
        """Определение типа значения триплета"""
        trp_val_str_isltr = parse_settings.settings.trp_val_str_isltr
        bid = parse_settings.settings.bid

        # булево значение
        if value == 'True':
            return True
        if value == 'False':
            return False
        # заявка
        if value == bid:
            return value
        # строка
        if value.startswith(trp_val_str_isltr) and value.endswith(trp_val_str_isltr):
            sprtr_len = len(trp_val_str_isltr)
            value = value[sprtr_len: -sprtr_len]
            return value
        # число
        if value.isdigit():
            return int(value)
        # число с плавающей запятой
        if isfloat(value):
            return float(value)
        # триплетная строка
        if len(re.findall(re_trps, value)) != 0:
            return parse_trp_str(value)
        # триплет
        _trp = re.fullmatch(re_trp, value)
        if _trp is not None:
            return Trp(*_trp.groups())
        # TODO триплетное выражение

        raise ValueError('Неверный формат значения триплета', value)

    if isinstance(str_to_parse, TrpStr):
        return TrpStr
    elif not isinstance(str_to_parse, str):
        raise TypeError('Строка для парсинга должна быть str, не ' + type_name(str_to_parse), str_to_parse)

    re_trp = parse_settings.re_trp
    re_trps = parse_settings.re_trps
    parsed_str = re.findall(re_trp, str_to_parse)

    result = TrpStr(*(
        Trp(prefix, name, _determine_value(value), comment) for prefix, name, value, comment in parsed_str
    ))
    return result


def parse_trp_expr():
    # TODO
    pass
