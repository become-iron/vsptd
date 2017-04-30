# -*- coding: utf-8 -*-
"""Разбор строк на ВСПТД-структуры, а также генерация соответствующих регулярных выражений."""

import re

from vsptd.vsptd import Trp, TrpStr, VSPTDSettings
from vsptd.support import isfloat, type_name

__all__ = ('VSPTDParse', 'parse_trp_str'
           # , 'parse_trp_expr'
           )


# noinspection SpellCheckingInspection
class VSPTDParse:
    """
    **Регулярные выражения для разбора строк**

    Класс обеспечивает удобный интерфейс генерации регулярных выражений для разбора строк.

    .. note::
        * представленные выражения не обеспечивают валидацию,
        * свойства недоступны для изменений;
        * для пересчёта выражений необходимо заново создать экземпляр класса.

    :param settings:  настройки конфигурации ВСПТД; по умолчанию используются стандартные
    :type settings: VSPTDSettings, необяз.
    """
    _word = '(\w+)'  # Буквенный или цифровой символ или знак подчёркивания, >= 1 раз, группированный
    _any = '(.*?)'  # Любой символ, >= 0 раз, группированный, ленивый

    def __init__(self, settings=VSPTDSettings()):
        self._settings = settings  #: настройки конфигурации ВСПТД :class:`VSPTDSettings`

        self.__re_trp_ref_special = None
        self.__re_trp_ref = None
        self.__re_trp_special = None
        self.__re_trp = None
        self.__re_trps = None

        self.__re_func_present = None

        # TODO
        # self.__re_trp_expr =

    @property
    def re_trp_ref_special(self):
        """"Особенный" триплет-ссылка — P.N"""
        if self.__re_trp_ref_special is None:
            trp_pn_sprtr = re.escape(self._settings.trp_pn_sprtr)
            self.__re_trp_ref_special = VSPTDParse._word + trp_pn_sprtr + VSPTDParse._word
        return self.__re_trp_ref_special

    @property
    def re_trp_ref(self):
        """Триплет-ссылка — $P.N"""
        if self.__re_trp_ref is None:
            trp_start = re.escape(self._settings.trp_start)
            self.__re_trp_ref = trp_start + self.re_trp_ref_special
        return self.__re_trp_ref

    @property
    def re_trp_special(self):
        """Особенный" триплет — P.N=V;"""
        if self.__re_trp_special is None:
            trp_nv_sprtr = re.escape(self._settings.trp_nv_sprtr)
            trp_end = re.escape(self._settings.trp_end)
            self.__re_trp_special = self.re_trp_ref_special + trp_nv_sprtr + VSPTDParse._any + trp_end
        return self.__re_trp_special

    @property
    def re_trp(self):
        """Триплет — $P.N=V;, $P.N=V"C";, $P.N=:V"C"; и т.д."""
        if self.__re_trp is None:
            trp_start = re.escape(self._settings.trp_start)
            trp_pn_sprtr = re.escape(self._settings.trp_pn_sprtr)
            trp_nv_sprtr = re.escape(self._settings.trp_nv_sprtr)
            trp_comment_isltr = re.escape(self._settings.trp_comment_isltr)
            trp_end = re.escape(self._settings.trp_end)
            self.__re_trp = \
                trp_start + VSPTDParse._word + \
                trp_pn_sprtr + VSPTDParse._word + '??' +\
                trp_nv_sprtr + VSPTDParse._any +\
                '(?:' + trp_comment_isltr + VSPTDParse._any + trp_comment_isltr + ')??' +\
                trp_end
        return self.__re_trp

    # TODO
    # RE_FUNC_PRESENT = '(?:есть|ЕСТЬ)\(' + RE_PREFIX_NAME + '\)'
    # RE_FUNC_PRESENT_WODS = '(?:есть|ЕСТЬ)\(' + RE_PREFIX_NAME_WODS + '\)'
    # RE_FUNC_ABSENCE = '(?:нет|НЕТ)\(' + RE_PREFIX_NAME + '\)'
    # RE_FUNC_ABSENCE_WODS = '(?:нет|НЕТ)\(' + RE_PREFIX_NAME_WODS + '\)'
    # RE_SLICE = r'(\[(\d+),(\d+)\])'  # срез [n,n]

    # правило и действия
    # RE_RULE = 'ЕСЛИ (.+) ТО (.+);'  # правило
    # RE_ACT_FIND_IN_DB = r'НАЙТИ_В_БД\((.*)\)'  # искать в БД
    # RE_ACT_FIND_IN_DB_WO = r'НАЙТИ_В_БД\((.*)\\\\(.*)(\+|-)\\\\\)'  # искать в БД
    # RE_ACT_ADD_IN_DB = 'ДОБАВИТЬ_В_БД\((' + _RE_PREFIX + ')\)'  # добавить в БД
    # RE_ACT_DEL_FROM_DB = 'УДАЛИТЬ_В_БД\((' + _RE_PREFIX + ')\)'  # удалить из БД

    # реквизит
    # RE_RQST = '\$(' + _RE_PREFIX + ')\.(' + RE_NAME + ')(?:(\||:)(' + RE_VALUE + ')?)?'

    def __repr__(self):
        return '<{}>'.format(VSPTDParse.__name__)


# noinspection PyProtectedMember
def parse_trp_str(str_to_parse: str, parse_settings=VSPTDParse()):
    """
    Разбирает строку на триплеты и возвращает триплетную строку

    .. note::
        * не поддерживаются "особенные" триплеты;
        * функцией можно парсить и триплеты, но вернётся всё равно триплетная строка ``TrpStr``;
        * вернёт параметр ``str_to_parse`` без изменений, если он будет ``TrpStr``.

    .. warning:: Не гарантируется верный парсинг строк с ошибками.

    :param str str_to_parse: строка для парсинга
    :param parse_settings:  настройки конфигурации ВСПТД; по умолчанию используются стандартные
    :type parse_settings: VSPTDParse, используются стандартные по умолчанию
    :rtype: TrpStr

    :raises TypeError: если ``str_to_parse`` не ``str`` и не ``TrpStr``
    :raises ValueError: неверный формат значения триплета
    """
    # TODO: неверно работает с триплетами вида $A.B='[1, 2, 3, 'A']'
    # noinspection PyProtectedMember
    def _determine_value(value):
        """Определение типа значения триплета"""
        trp_val_str_isltr = parse_settings._settings.trp_val_str_isltr
        re_trp_ref = parse_settings.re_trp_ref

        # избавляемся от заявки
        if value.startswith(bid):
            value = value[len(bid):]

        # None
        if value == '':
            return None

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
        # триплет-ссылка
        _trp = re.fullmatch(re_trp_ref, value)
        if _trp is not None:
            trp_params = tuple(param for param in _trp.groups() if param != '')  # удаляем пустые параметры
            return Trp(*trp_params)
        # TODO триплетное выражение

        raise ValueError('Неверный формат значения триплета', value)

    if isinstance(str_to_parse, TrpStr):
        return TrpStr
    elif not isinstance(str_to_parse, str):
        raise TypeError('Строка для парсинга должна быть str, не ' + type_name(str_to_parse), str_to_parse)

    re_trp = parse_settings.re_trp
    parsed_str = re.findall(re_trp, str_to_parse)

    bid = parse_settings._settings.bid
    result = TrpStr(*(
        Trp(p, n, _determine_value(v), c, v.startswith(bid)) for p, n, v, c in parsed_str
    ))
    return result


# def parse_trp_expr():
#     # TODO
#     pass
