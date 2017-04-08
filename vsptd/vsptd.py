# -*- coding: utf-8 -*-
"""
Основная библиотека. Позволяет работать с триплетами, триплетными строками, триплетными выражениями (фрейм-формулами).
Также содержит функционал для настройки параметров ВСПТД.
"""

import re
from collections import OrderedDict

from vsptd.support import type_name

__all__ = ('VSPTDSettings', 'Trp', 'TrpStr', 'TrpExpr')


class VSPTDSettings:
    """
    **Хранение настроек параметров ВСПТД-объектов и правил валидации строковых значений**

    .. note::
        Правила валидации значений представлены в виде регулярных выражений (RegExp).

    :Пример работы:
        >>> my_settings = VSPTDSettings()
        >>> my_settings.prefix.min = 5
        >>> my_settings.prefix.max = 100
        >>> my_settings.prefix.regexp = '.*'
        >>> my_settings.trp_start = '~'
        >>> Trp.settings = my_settings  # применение настроек к классу триплета
    """
    # TODO добавить экспорт/импорт настроек в формате JSON?
    # TODO добавить ли и валидацию по типам?
    bid = ':'  #: Заявка. См. описание ВСПТД

    trp_start = '$'  #: Начало триплета
    trp_pn_sprtr = '.'  #: Разделитель префикса и имени триплета
    trp_nv_sprtr = '='  #: Разделитель имени и значения триплета
    trp_end = ';'  #: Конец триплета
    trp_val_str_isltr = '\''  #: Обособление значения-строки триплета
    trp_comment_isltr = '"'  #: Обособление комментария триплета

    trps_sprtr = ' '  #: Разделитель триплетов в триплетной строке :class:`TrpStr`

    trp_expr_items_sprtr = ''  #: Разделитель операторов и операндов в триплетном выражении :class:`TrpExp`

    # для удобного доступа к настройкам параметров триплетов
    class __TrpSettings:
        def __init__(self, min_len: int, max_len: int, regexp: str):
            self.min = min_len  #: Минимальная длина параметра
            self.max = max_len  #: Максимальная длина параметра
            self.regexp = re.compile(regexp)  #: RegExp для проверки параметра триплета
            # self.types = types  #: Разрешённые типы параметра

        def __repr__(self):
            return '<TrpSettings(min={!r}, max={!r}, regexp={!r})>'.format(self.min, self.max, self.regexp.pattern)

    #: Настройки префикса триплета
    prefix = __TrpSettings(1, 25, r'[A-Z]+\d*')
    #: Настройки имени триплета
    name = __TrpSettings(1, 25, r'[A-Z]+')
    # r'[\wА-Яа-яЁё ()-.:?–—−]*'
    #: Настройки значения-строки триплета
    value = __TrpSettings(0, 200, r'.*')
    #: Настройки комментария триплета
    comment = __TrpSettings(0, 200, r'.*')

    def __repr__(self):
        return '<{}>'.format(VSPTDSettings.__name__)

    def validate(self, prefix=None, name=None, value=None, comment=None):
        """
        Проверяет корректность параметра триплета

        :param prefix:
        :param name:
        :param value:
        :param comment:
        :return:
        """
        def _validation(trp_param, settings, param_name):
            msg_err_len = 'Длина {} должна быть от {} до {}, не {}'
            msg_err_regexp = '{} не удовлетворяет соответствующему формату'

            if not (settings.min <= len(trp_param) <= settings.max):
                raise ValueError(
                    msg_err_len.format(param_name[1], settings.min, settings.max, len(trp_param)),
                    trp_param
                )
            if re.fullmatch(settings.regexp, trp_param) is None:
                raise ValueError(
                    msg_err_regexp.format(param_name[0]),
                    trp_param
                )

        if prefix is not None:
            _validation(prefix, self.prefix, ('Префикс', 'префикса'))
        elif name is not None:
            _validation(name, self.name, ('Имя', 'имени'))
        elif value is not None:
            _validation(value, self.value, ('Значение', 'значения'))
        elif comment is not None:
            _validation(comment, self.comment, ('Комментарий', 'комментария'))
        else:
            raise ValueError

    # def validate_prefix(self, prefix: str) -> None:
    #     """
    #     Проверяет корректность префикса триплета
    #
    #     :param str prefix: префикс
    #     :raises ValueError: префикс несоответствующей длины
    #     :raises ValueError: префикс не удовлетворяет соответствующему формату
    #     """
    #     min_len, max_len, regexp = self.prefix.min, self.prefix.max, self.prefix.regexp
    #     if not (min_len <= len(prefix) <= max_len):
    #         raise ValueError(
    #             'Длина префикса должна быть от {} до {}, не {}'.format(min_len, max_len, len(prefix)), prefix
    #         )
    #     elif re.fullmatch(regexp, prefix) is None:
    #         raise ValueError('Префикс не удовлетворяет соответствующим требованиям', prefix)
    #
    # def validate_name(self, name: str) -> None:
    #     """
    #     Проверяет корректность имени триплета
    #
    #     :param str name: имя
    #     :raises ValueError: имя несоответствующей длины
    #     :raises ValueError: имя не удовлетворяет соответствующему формату
    #     """
    #     min_len, max_len, regexp = self.name.min, self.name.max, self.name.regexp
    #     if not (min_len <= len(name) <= max_len):
    #         raise ValueError(
    #             'Длина имени должна быть от {} до {}, не {}'.format(min_len, max_len, len(name)), name
    #         )
    #     elif re.fullmatch(regexp, name) is None:
    #         raise ValueError('Имя не удовлетворяет соответствующим требованиям', name)
    #
    # def validate_value(self, value_str) -> None:
    #     """
    #     Проверяет корректность значения-строки триплета
    #
    #     :param str value_str: значение-строка
    #     :raises ValueError: значение несоответствующей длины
    #     :raises ValueError: значение не удовлетворяет соответствующему формату
    #     """
    #     min_len, max_len, regexp = self.value.min, self.value.max, self.value.regexp
    #     if not (min_len <= len(value_str) <= max_len):
    #         raise ValueError(
    #             'Длина значения должна быть от {} до {}, не {}'.format(min_len, max_len, len(value_str)), value_str
    #         )
    #     elif re.fullmatch(regexp, value_str) is None:
    #         raise ValueError('Значение не удовлетворяет соответствующим требованиям', value_str)
    #
    # def validate_comment(self, comment) -> None:
    #     """
    #     Проверяет корректность комментария триплета
    #
    #     :param str comment: комментарий
    #     :raises ValueError: комментарий несоответствующей длины
    #     :raises ValueError: комментарий не удовлетворяет соответствующему формату
    #     """
    #     min_len, max_len, regexp = self.comment.min, self.comment.max, self.comment.regexp
    #     if not (min_len <= len(comment) <= max_len):
    #         raise ValueError(
    #             'Длина комментария должна быть от {} до {}, не {}'.format(min_len, max_len, len(comment)), comment
    #         )
    #     elif re.fullmatch(regexp, comment) is None:
    #         raise ValueError('Комментарий не удовлетворяет соответствующим требованиям', comment)


class Trp:
    """
    **Триплет**

    .. note::
        * при создании триплета и изменении его значений производится валидация, в результате чего могут вызваны
          различные исключения. См. дополнительно в спецификации ВСПТД требования к параметрам триплета, а также
          стандартную конфигурацию ВСПТД-параметров в описании API класса :class:`VSPTDSettings`.
        * свойства ``prefix`` и ``name`` недоступны для изменения после создания триплета;
        * если не указано значение триплета, то созданный триплет может использоваться
          как триплет-цель в значении другого триплета или в триплетном выражении :class:`TrpExpr`:

            >>> print(Trp('A', 'B', Trp('C', 'D')))
            $A.B=$C.D;

        * свойство ``special`` отвечает за "особенность" триплета, что проявляется отсутствием символа начала триплета
          в строковом представлении, а также приобретаемым дополнительным смыслом в контексте решаемой задачи:

            >>> print(Trp('A', 'B', special=True))
            A.B

    :param str prefix:  префикс триплета
    :param name: имя триплета
    :type name: str, необяз.
    :param value: значение триплета; None по умолчанию
    :type value: str, int, float, bool, Trp, TrpExpr, необяз.
    :param comment: комментарий; пустая строка по умолчанию
    :type comment: str, необяз.
    :param bid: заявка
    :type bid: bool, необяз.
    :param special: "особенность" триплета
    :type special: bool, необяз.

    :raises TypeError: если параметры не соответствующих типов
    :raises ValueError: если параметры не удовлетворяют соответствующим требованиям
    :raises ValueError: при попытке использовать в качестве значения триплет, не являющийся триплетом-целью
    :raises AttributeError: при попытке изменить свойства `prefix` и `name`

    :Пример работы:
        >>> Trp('A', 'B', 'C')
        Trp(prefix='A', name='B', value='C')
    """
    # TODO нужна ли проверка при различных сочетаниях параметров?
    #: `Свойство класса.` Настройки конфигурации ВСПТД :class:`VSPTDSettings`; по умолчанию используются стандартные
    settings = VSPTDSettings()

    __slots__ = ('__prefix', '__name', '__value', '__comment', '__bid', '__special')

    def __init__(self, prefix: str, name=None, value=None, comment=None, bid=False, special=False):
        if isinstance(prefix, str):
            self.settings.validate(prefix=prefix)
            self.__prefix = prefix
        else:
            raise TypeError('Префикс должен быть str, не ' + type_name(prefix), prefix)

        if isinstance(name, str):
            self.settings.validate(name=name)
            self.__name = name
        elif name is not None:
            raise TypeError('Имя должно быть str, не ' + type_name(name), name)

        # установка свойств value, comment, special, bind выполняется
        # таким образом с целью их валидации через setter'ы
        self.__value = None
        self.value = value
        self.__comment = None
        self.comment = comment
        self.__bid = False
        self.bid = bid
        self.__special = False
        self.special = special

    @property
    def prefix(self):
        """Префикс триплета"""
        return self.__prefix

    @property
    def name(self):
        """Имя триплета"""
        return self.__name

    @property
    def value(self):
        """Значение триплета"""
        return self.__value

    @value.setter
    def value(self, value):
        if isinstance(value, str):
            self.settings.validate(value=value)
        elif isinstance(value, Trp):
            if value.value is not None:
                raise ValueError('В качестве значения можно использовать только триплет-цель', value)
        elif not isinstance(value, (int, float, bool, TrpExpr)) and value is not None:
            raise TypeError(
                'Значение должно быть str, int, float, bool, Trp, TrpExpr, не ' + type_name(value),
                value
            )
        self.__value = value

    @property
    def comment(self):
        """Комментарий триплета"""
        return self.__comment

    @comment.setter
    def comment(self, value):
        if isinstance(value, str):
            self.settings.validate(value=value)
        elif value is not None:
            raise TypeError('Комментарий должен быть str, не ' + type_name(value), value)
        self.__comment = value

    @property
    def bid(self):
        """Заявка"""
        return self.__bid

    @bid.setter
    def bid(self, value):
        if not isinstance(value, bool):
            raise TypeError('Параметр заявки должен быть bool, не ' + type_name(value), value)
        self.__bid = value

    @property
    def special(self):
        """"Особенность" триплета"""
        return self.__special

    @special.setter
    def special(self, value):
        if not isinstance(value, bool):
            raise TypeError('Параметр special должен быть bool, не ' + type_name(value), value)
        self.__special = value

    def __add__(self, other):
        if isinstance(other, Trp):
            return TrpStr(self, other)
        elif isinstance(other, TrpStr):
            return TrpStr(self, *other)
        else:
            raise TypeError('Должен быть Trp или TrpStr, не ' + type_name(other), other)

    def __str__(self):
        bid = self.settings.bid
        trp_start = self.settings.trp_start
        trp_pn_sprtr = self.settings.trp_pn_sprtr
        trp_nv_sprtr = self.settings.trp_nv_sprtr
        trp_str_isltr = self.settings.trp_val_str_isltr
        trp_comment_isltr = self.settings.trp_comment_isltr
        trp_end = self.settings.trp_end

        result = ''
        if not self.special:
            result += trp_start
        result += self.prefix + trp_pn_sprtr
        if self.name is not None:
            result += self.name
        if self.value is None and not self.bid:
            # если не указано значение триплета и это не заявка, то считаем, что это триплет-цель
            return result
        result += trp_nv_sprtr
        if self.bid:
            result += bid
        if self.value is not None:
            if isinstance(self.value, str):
                result += trp_str_isltr + self.value + trp_str_isltr
            else:
                result += str(self.value)
        if self.comment is not None:
            result += trp_comment_isltr + self.comment + trp_comment_isltr
        result += trp_end
        return result

    def __repr__(self):
        result = 'Trp(prefix={!r}'.format(self.prefix)
        if self.name is not None:
            result += ', name={!r}'.format(self.name)
        if self.value is not None:
            result += ', value={!r}'.format(self.value)
        if self.comment is not None:
            result += ', comment={!r}'.format(self.comment)
        if self.special:
            result += ', special={!r}'.format(self.special)
        if self.bid:
            result += ', bid={!r}'.format(self.bid)
        result += ')'
        return result

    def __eq__(self, other):
        # TODO проверять ли и комментарий, special, bid?
        return isinstance(other, Trp) and \
               self.prefix == other.prefix and \
               self.name == other.name and \
               self.value == other.value


class TrpStr:
    """
    **Триплетная строка**

    .. note::
        Триплетная строка упорядочена. Новые триплеты добавляются в конец, старые обновляются и сохраняют свои позиции.

    :param `*trps`: триплеты :class:`Trp`
    :raises TypeError: если параметры не :class:`Trp`
    :Пример работы:
        >>> TrpStr(Trp('A', 'B', 'C'))
        TrpStr(Trp(prefix='A', name='B', value='C'))
    """
    # TODO добавить возможность инициализации из генератора?
    __slots__ = ('__trps',)

    #: `Свойство класса.` Настройки конфигурации ВСПТД :class:`VSPTDSettings`; по умолчанию используются стандартные
    settings = VSPTDSettings()

    def __init__(self, *trps):
        self.__trps = OrderedDict()
        for trp in trps:
            # все ли аргументы — триплеты
            if not isinstance(trp, Trp):
                raise TypeError('Должен быть Trp, не ' + type_name(trp), trp)
            self.__trps.update({hash((trp.prefix, trp.name)): trp})

    def __str__(self):
        trps_sprtr = self.settings.trps_sprtr
        return trps_sprtr.join(str(trp) for trp in self)

    def __repr__(self):
        return 'TrpStr({})'.format(', '.join(repr(trp) for trp in self))

    def __len__(self):
        return len(self.__trps)

    def __bool__(self):
        # приведение к типу bool
        # если в трипл. строке есть триплете, то True, иначе False
        return len(self) > 0

    def __getitem__(self, key):
        # TODO: добавить доступ по индексу, срезу?
        # TODO: должна использоваться строгая выборка?
        if isinstance(key, (tuple, list)):
            return self.get(*key)
        elif isinstance(key, str):
            return self.getpr(key)
        else:
            raise KeyError('Неверный формат ключа', key)

    def __delitem__(self, key):
        if isinstance(key, (tuple, list)):
            self.rem(*key)
        elif isinstance(key, str):
            self.rempr(key)
        else:
            raise KeyError('Неверный формат ключа', key)

    def __contains__(self, item):
        """
        Проверяет наличие в триплетной строке триплетов по заданным префиксу или префиксу и имени

        :raises TypeError: если параметр не `str`/`tuple`/`list`
        :Пример работы:
            >>> 'A' in  TrpStr(Trp('A', 'B', 'C'))
            True
            >>> ('A', 'B') in  TrpStr(Trp('A', 'B', 'C'))
            True
        """
        # префикс
        if isinstance(item, str):
            self.settings.validate(prefix=item)
            for trp in self:
                if trp.prefix == item:
                    return True
            return False
        # (префикс, имя)
        elif isinstance(item, (tuple, list)):
            prefix, name = item
            self.settings.validate(prefix=prefix)
            self.settings.validate(name=name)
            return hash((prefix, name)) in self.__trps
        else:
            raise TypeError('Должен быть str, tuple, list, не ' + type_name(item), item)

    def __eq__(self, other):
        # TODO: провести тесты на скорость работы
        if isinstance(other, TrpStr) and len(self) == len(other):
            for hash_, trp in self.__trps.items():
                if trp != other.__trps.get(hash_):
                    return False
        else:
            return False
        return True
        # return isinstance(other, TrpStr) and dict(self.__trps) == dict(other.__trps)

    def __add__(self, other):
        if isinstance(other, Trp):
            result = TrpStr()
            result.__trps.update(self.__trps)
            result.__trps.update({hash((other.prefix, other.name)): other})
            return result
        elif isinstance(other, TrpStr):
            result = TrpStr()
            result.__trps.update(self.__trps)
            result.__trps.update(other.__trps)
            return result
        else:
            raise TypeError('Должен быть Trp или TrpStr, не ' + type_name(other), other)

    def __iter__(self):
        yield from self.__trps.values()

    def add(self, other) -> None:
        """
        Добавляет в триплетную строку переданный триплет или триплеты переданной триплетной строки

        Практически эквивалентно сложению через оператор "+". Отличие в том,
        что данный метод не возвращает новый экземпляр, а изменяет нынешний.

        :param other: триплет или триплетная строка
        :type other: Trp, TrpStr

        :raises TypeError: если параметр не :class:`Trp` и не :class:`TrpStr`

        :Пример работы:
            >>> my_trp_str = TrpStr(Trp('A', 'B', 'C'))
            >>> my_trp_str.add(Trp('D', 'E', 'F'))
        """
        if isinstance(other, Trp):
            self.__trps.update({hash((other.prefix, other.name)): other})
        elif isinstance(other, TrpStr):
            self.__trps.update(other.__trps)
        else:
            raise TypeError('Должен быть Trp или TrpStr, не ' + type_name(other), other)

    def get(self, prefix: str, name):
        """
        Возвращает из триплетной строки триплет по заданным префиксу и имени

        Эквивалентно ``<TrpStr>[prefix, name]``

        :param str prefix: префикс
        :param str name: имя
        :rtype: Trp

        :raises TypeError: если префикс/имя не является ``str``
        :raises ValueError: если префикс/имя не удовлетворяет соответствующим требованиям
        :raises KeyError: если по заданным префиксу и имени триплет не найден
        """
        if not isinstance(prefix, str):
            raise TypeError('Префикс должен быть str, не ' + type_name(prefix), prefix)
        self.settings.validate(prefix=prefix)
        if isinstance(name, str):
            self.settings.validate(name=name)
        elif name is not None:
            raise TypeError('Имя должно быть str, не ' + type_name(name), name)

        try:
            return self.__trps[hash((prefix, name))]
        except KeyError:
            raise KeyError('По заданным префиксу и имени триплет не найден', (prefix, name))

    def getpr(self, prefix: str, strict=True):
        """
        Возвращает из триплетной строки триплеты по заданному префиксу

        Эквивалентно ``<TrpStr>[prefix]``

        :param str prefix: префикс
        :param bool strict: использовать строгий поиск (не включает префиксы вида E, E1, E2 и т.д.), True по умолчанию
        :rtype: TrpStr

        :raises TypeError: если префикс не является ``str``
        :raises ValueError: префикс не удовлетворяет соответствующим требованиям
        :raises KeyError: если по заданному префиксу триплетов не найдено
        """
        if not isinstance(prefix, str):
            raise TypeError('Префикс должен быть str, не ' + type_name(prefix), prefix)
        self.settings.validate(prefix=prefix)

        result = TrpStr()
        if strict:
            result.__trps.update({hash_: trp for hash_, trp in self.__trps.items() if trp.prefix == prefix})
        else:
            pattern = r'^([A-Z]+)(\d*)$'
            result.__trps.update({hash_: trp for hash_, trp in self.__trps.items()
                                  if re.findall(pattern, trp.prefix)[0][0] == prefix})
        if len(result.__trps) == 0:
            raise KeyError('По заданному префиксу триплетов не найдено', prefix)
        return result

    def rem(self, prefix: str, name) -> None:
        """
        Удаляет из триплетной строки триплет по заданным префиксу и имени

        Эквивалентно ``del <TrpStr>[prefix, name]``

        :param str prefix: префикс
        :param str name: имя параметра

        :raises TypeError: если префикс/имя не является ``str``
        :raises ValueError: если префикс/имя не удовлетворяет соответствующим требованиям
        :raises KeyError: если по заданным префиксу и имени триплет не найден
        """
        if not isinstance(prefix, str):
            raise TypeError('Префикс должен быть str, не ' + type_name(prefix), prefix)
        self.settings.validate(prefix=prefix)
        if isinstance(name, str):
            self.settings.validate(name=name)
        elif name is not None:
            raise TypeError('Имя должно быть str, не ' + type_name(name), name)

        try:
            del self.__trps[hash((prefix, name))]
        except KeyError:
            raise KeyError('По заданным префиксу и имени триплет не найден', (prefix, name))

    def rempr(self, prefix: str, strict=True) -> None:
        """
        Удаляет из триплетной строки все триплеты по заданному префиксу

        Эквивалентно ``del <TrpStr>[prefix]``

        :param str prefix: префикс
        :param bool strict: использовать строгий поиск (не включает префиксы вида E, E1, E2 и т.д.), True по умолчанию

        :raises TypeError: если префикс не является ``str``
        :raises ValueError: префикс не удовлетворяет соответствующим требованиям
        :raises KeyError: если по заданному префиксу триплетов не найдено
        """
        if not isinstance(prefix, str):
            raise TypeError('Префикс должен быть str, не ' + type_name(prefix), prefix)
        self.settings.validate(prefix=prefix)

        count = len(self.__trps)
        if strict:
            for hash_ in tuple(hash_ for hash_, trp in self.__trps.items() if trp.prefix == prefix):
                del self.__trps[hash_]
        else:
            pattern = r'^([A-Z]+)(\d*)$'
            for hash_ in tuple(hash_ for hash_, trp in self.__trps.items()
                               if re.findall(pattern, trp.prefix)[0][0] == prefix):
                del self.__trps[hash_]
        if count == len(self.__trps):
            raise KeyError('По заданному префиксу триплетов не найдено', prefix)

    def sort(self) -> None:
        """
        Сортирует триплетную строку в лексиграфическом порядке по префиксу и имени триплетов
        """
        # TODO: добавить параметр для функции-сортировки
        self.__trps = OrderedDict(sorted(self.__trps.items(), key=lambda item: (item[1].prefix, item[1].name)))


class TrpExpr:
    """
    **Триплетное выражение, или фрейм-формула**

    .. note::
        * операторы должны быть в виде строк ``str``;
        * используемые триплеты должны быть триплетами-целями.

    :param `*items`: параметры
    :type `*items`: str, int, float, bool, Trp

    :raises ValueError: если триплет не является триплетом-целью
    :raises TypeError: если элемент не str, int, float, bool или Trp

    :Пример работы:
        >>> expr = TrpExpr(Trp('A', 'B'), '*', Trp('C', 'D'))
        >>> print(expr)
        $A.B*$C.D
        >>> print(Trp('E', 'F', expr))
        $E.F=$A.B*$C.D;
    """
    __slots__ = ('items',)

    #: `Свойство класса.` Настройки конфигурации ВСПТД :class:`VSPTDSettings`; по умолчанию используются стандартные
    settings = VSPTDSettings()

    def __init__(self, *items):
        for item in items:
            if isinstance(item, Trp):
                if item.value is not None:
                    raise ValueError('Триплет должен быть триплетом-целью', item)
            elif not isinstance(item, (str, int, float, bool)):
                raise TypeError(
                    'Элемент должен быть str, int, float, bool, Trp, не ' + type_name(item),
                    item
                )
        self.items = items  #: Операнды и операторы в триплетном выражении

    def __str__(self):
        items_trp_expr_sprtr = TrpExpr.settings.trp_expr_items_sprtr
        return items_trp_expr_sprtr.join(str(item) for item in self.items)

    def __repr__(self):
        return 'TrpExpr({})'.format(', '.join(repr(item) for item in self.items))

    def compute(self, source=None, special_source=None):
        """
        Вычисляет выражение

        .. warning::
            В текущей версии для вычисления выражения используется ``eval``,
            что потенциально опасно.

        :param source: триплетная строка, откуда будут браться значения
        :type source: TrpStr, необяз.
        :param special_source: триплетная строка, откуда будут браться значения,
            соответствующие "специальным" триплетам
        :type special_source: TrpStr, необяз.

        :return: результат вычисления выражения

        :Пример работы:
            >>> expr = TrpExpr(Trp('A', 'B'), '*', Trp('C', 'D'))
            >>> trp_str = TrpStr(Trp('A', 'B', 21), Trp('C', 'D', 2))
            >>> expr.compute(trp_str)
            42
        """
        result = []
        for item in self.items:
            if isinstance(item, Trp):
                if item.special:
                    value = special_source.get(item.prefix, item.name).value
                    result.append(str(value))
                else:
                    value = source.get(item.prefix, item.name).value
                    result.append(str(value))
            elif isinstance(item, TrpExpr):
                result.append(str(item.compute()))
            else:
                result.append(str(item))

        # TODO переписать с использованием модуля operator
        # TODO: "обезапасить" eval
        return eval(''.join(result))
