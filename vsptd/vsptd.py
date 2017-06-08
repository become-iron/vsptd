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
        * Правила валидации значений представлены в виде регулярных выражений (RegExp).
        * Подразумевается, что типы данных для параметров триплета не будут изменяться.

    :Пример работы:
        >>> my_settings = VSPTDSettings()
        >>> my_settings.prefix_min = 5
        >>> my_settings.prefix_max = 100
        >>> my_settings.prefix_regexp = '.*'
        >>> my_settings.trp_start = '~'
        >>> Trp.settings = my_settings  # применение настроек к классу триплета
    """
    bid = ':'  #: Заявка. См. описание ВСПТД

    trp_start = '$'  #: Начало триплета
    trp_pn_sprtr = '.'  #: Разделитель префикса и имени триплета
    trp_nv_sprtr = '='  #: Разделитель имени и значения триплета
    trp_end = ';'  #: Конец триплета
    trp_val_str_isltr = '\''  #: Обособление значения-строки триплета
    trp_comment_isltr = '"'  #: Обособление комментария триплета

    trps_sprtr = ' '  #: Разделитель триплетов в триплетной строке :class:`TrpStr`

    trp_expr_items_sprtr = ''  #: Разделитель операторов и операндов в триплетном выражении :class:`TrpExp`

    prefix_min = 1  #: Мин. длина префикса триплета
    prefix_max = 32  #: Макс. длина префикса триплета
    prefix_regexp = r'[A-Z]+\d*'  #: Формат префикса триплета (RegExp)
    prefix_types = (str,)  #: Типы данных префикса триплета

    name_min = 1  #: Мин. длина имени триплета
    name_max = 32  #: Макс. длина имени триплета
    name_regexp = r'[A-Z]+'  #: Формат имени триплета (RegExp)
    name_types = (str,)  #: Типы данных имени триплета

    value_str_min = 0  #: Мин. длина значения-строки триплета
    value_str_max = 256  #: Макс. длина значения-строки триплета
    value_str_regexp = None  #: Формат значения-строки триплета (RegExp)
    # реальное значение для типов устанавливается в конце скрипта
    value_types = None  #: Типы данных значения триплета

    comment_min = 0  #: Мин. длина комментария триплета
    comment_max = 256  #: Макс. длина комментария триплета
    comment_regexp = None  #: Формат комментария триплета (RegExp)
    comment_types = (str,)  #: Типы данных комментария триплета

    def __repr__(self):
        return '<{}>'.format(VSPTDSettings.__name__)

    def validate(self, prefix=None, name=None, value=None, comment=None) -> None:
        """
        Проверяет корректность параметра триплета. В случае ошибки вызывает исключение

        .. note:: Проверить можно лишь один параметр за раз. Необходимо всегда указывать имя параметра функции.

        :param prefix: префикс триплета
        :param name: имя триплета
        :param value: значение триплета
        :param comment: комментарий триплета
        """
        if prefix is not None:
            trp_param, min_, max_, regexp, types, param_name = \
                prefix, self.prefix_min, self.prefix_max, self.prefix_regexp, self.prefix_types, 'префикса'
        elif name is not None:
            trp_param, min_, max_, regexp, types, param_name = \
                name, self.name_min, self.name_max, self.name_regexp, self.name_types, 'имени'
        elif value is not None:
            trp_param, min_, max_, regexp, types, param_name = \
                value, self.value_str_min, self.value_str_max, self.value_str_regexp, self.value_types, 'значения'
        elif comment is not None:
            trp_param, min_, max_, regexp, types, param_name = \
                comment, self.comment_min, self.comment_max, self.comment_regexp, self.comment_types, 'комментария'
        else:
            # эта ветка нужна, так как параметры триплета могут принимать значение None,
            # отсюда есть возможность валидация параметров без предварительной проверки на None
            return

        msg_err_type = 'Типом {0} может быть {1}, не {2}'
        msg_err_len = 'Длина {0} должна быть от {1} до {2}, не {3}'
        msg_err_regexp = 'Формат {0} некорректен'

        if not isinstance(trp_param, types):
            types_names = ', '.join(map(lambda x: x.__name__, types))
            raise TypeError(
                msg_err_type.format(param_name, types_names, type_name(trp_param)),
                trp_param
            )
        if not isinstance(trp_param, str):
            # прекратить проверку, если объект не является строкой
            return

        if not (min_ <= len(trp_param) <= max_):
            raise ValueError(
                msg_err_len.format(param_name, min_, max_, len(trp_param)),
                trp_param
            )
        if (isinstance(regexp, str) or hasattr(regexp, 'pattern')) and re.fullmatch(regexp, trp_param) is None:
            raise ValueError(
                msg_err_regexp.format(param_name),
                trp_param
            )

    def to_dict(self) -> dict:
        """
        Возвращает настройки ВСПТД в виде словаря
        """
        # TODO: возможно, стоит представлять типы в виде строк
        # берём нужные свойства класса
        result = {
            attr: value
            for attr, value in VSPTDSettings.__dict__.items()
            if not attr.startswith('_') and not callable(value)
        }
        # берём свойства экземпляра класса
        result.update(self.__dict__)
        return result

    def from_dict(self, settings: dict) -> None:
        """
        Обновляет настройки ВСПТД из переданных в словаре

        .. warning:: Валидация настроек не проводится.

        :param dict settings: настройки
        """
        self.__dict__.update(settings)


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

        * имени или комментарию, равным пустой строке, будет присвоено значение `None`

    :param str prefix:  префикс триплета
    :param name: имя триплета
    :type name: str, необяз.
    :param value: значение триплета; None по умолчанию
    :type value: str, int, float, Trp, TrpExpr, необяз.
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
    #: `Свойство класса.` Настройки конфигурации ВСПТД :class:`VSPTDSettings`; по умолчанию используются стандартные
    settings = VSPTDSettings()

    __slots__ = ('__prefix', '__name', '__value', '__comment', '__bid', '__special')

    def __init__(self, prefix: str, name=None, value=None, comment=None, bid=False, special=False):
        self.settings.validate(prefix=prefix)
        self.__prefix = prefix
        if name == '':
            name = None
        else:
            self.settings.validate(name=name)
        self.__name = name

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
        if isinstance(value, Trp):
            if value.value is not None:
                raise ValueError('В качестве значения можно использовать только триплет-цель', value)
        elif isinstance(value, bool):
            # WARN: необходимый костыль, т.к. bool наследуется от int
            raise TypeError(
                'Значение должно быть str, int, float, Trp, TrpExpr, не ' + type_name(value),
                value
            )
        else:
            self.settings.validate(value=value)
        self.__value = value

    @property
    def comment(self):
        """Комментарий триплета"""
        return self.__comment

    @comment.setter
    def comment(self, value):
        if value == '':
            value = None
        else:
            self.settings.validate(comment=value)
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
        if self.comment is not None and self.comment != '':
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
        # учитывается также комментарий, special, bid
        return isinstance(other, Trp) and \
                self.prefix == other.prefix and \
                self.name == other.name and \
                self.value == other.value and \
                self.comment == other.comment and \
                self.bid == other.bid and \
                self.special == other.special
        # or (isinstance(other, TrpStr) and len(other) == 1 and self == tuple(other)[0])
        # сравнение с трипл. строкой, содержащей один триплет

    def __iter__(self):
        yield 'prefix', self.prefix
        yield 'name', self.name
        yield 'value', self.value
        yield 'comment', self.comment
        yield 'bid', self.bid
        yield 'special', self.special


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
    __slots__ = ('__trps',)

    #: `Свойство класса.` Настройки конфигурации ВСПТД :class:`VSPTDSettings`; по умолчанию используются стандартные
    settings = VSPTDSettings()

    def __init__(self, *trps):
        def check_type(trp):
            # для проверки, все ли аргументы — триплеты
            if isinstance(trp, Trp):
                return True
            else:
                raise TypeError('Должен быть Trp, не ' + type_name(trp), trp)
        self.__trps = OrderedDict({hash((trp.prefix, trp.name)): trp for trp in trps if check_type(trp)})

    def __str__(self):
        trps_sprtr = self.settings.trps_sprtr
        return trps_sprtr.join(str(trp) for trp in self)

    def __repr__(self):
        return 'TrpStr({})'.format(', '.join(repr(trp) for trp in self))

    def __len__(self):
        return len(self.__trps)

    def __bool__(self):
        # приведение к типу bool
        # если в трипл. строке есть триплеты, то True, иначе False
        return len(self) > 0

    def __getitem__(self, key):
        # триплет по префиксу и имени
        if isinstance(key, (tuple, list)):
            return self.get(*key)
        # трипл. строка по префиксу
        elif isinstance(key, str):
            # используется строгая выборка
            return self.getpr(key)
        # триплет по индексу
        elif isinstance(key, int):
            if key >= 0:
                sequence = enumerate(self.__trps.values())
            else:
                sequence = enumerate(reversed(self.__trps.values()))
                key = abs(key) - 1
            try:
                return next(v for i, v in sequence if i == key)
            except StopIteration:
                raise IndexError('Про принятому индексу не существует триплета', key)
        # трипл. строка по срезу
        elif isinstance(key, slice):
            return TrpStr(*tuple(self)[key])
        else:
            raise KeyError('Неверный формат ключа', key)

    def __delitem__(self, key):
        # триплет по префиксу и имени
        if isinstance(key, (tuple, list)):
            self.rem(*key)
        # триплеты по префиксу
        elif isinstance(key, str):
            self.rempr(key)
        # триплет по индексу
        elif isinstance(key, int):
            if key >= 0:
                sequence = enumerate(self.__trps)
            else:
                sequence = enumerate(reversed(self.__trps))
                key = abs(key) - 1
            for i, hash_ in sequence:
                if i == key:
                    del self.__trps[hash_]
                    return
                elif i > key:
                    break
            raise IndexError('Про принятому индексу не существует триплета', key)
        # триплеты по срезу
        elif isinstance(key, slice):
            for hash_ in tuple(self.__trps.keys())[key]:
                del self.__trps[hash_]
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
        # не учитывает порядок триплетов
        return isinstance(other, TrpStr) and \
               len(self) == len(other) and \
               all(trp == other.__trps.get(hash_) for hash_, trp in self.__trps.items())

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

    def __reversed__(self):
        yield from reversed(self.__trps.values())

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

    def index(self, trp) -> int:
        """
        Возвращает позицию триплета в триплетной строке

        :param Trp trp: триплет
        :rtype: int

        :raises TypeError: Если принят не Trp
        :raises ValueError: Если триплет не найден в триплетной строке
        """
        if not isinstance(trp, Trp):
            raise TypeError('Должен быть Trp, не ' + type_name(trp), trp)

        try:
            return next(i for i, trp_ in enumerate(self.__trps.values()) if trp_ == trp)
        except StopIteration:
            raise ValueError('Триплет не найден в триплетной строке', trp)

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
        self.settings.validate(prefix=prefix)
        self.settings.validate(name=name)

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
        self.settings.validate(prefix=prefix)
        self.settings.validate(name=name)

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
        self.settings.validate(prefix=prefix)

        count = len(self.__trps)
        if strict:
            for hash_ in tuple(hash_ for hash_, trp in self.__trps.items() if trp.prefix == prefix):
                del self.__trps[hash_]
        else:
            pattern = r'^([A-Z]+)(\d*)$'  # паттерн для префикса; WARN: опасно, если изменится вид префикса
            for hash_ in tuple(hash_ for hash_, trp in self.__trps.items()
                               if re.findall(pattern, trp.prefix)[0][0] == prefix):
                del self.__trps[hash_]
        if count == len(self.__trps):
            raise KeyError('По заданному префиксу триплетов не найдено', prefix)

    def sort(self) -> None:
        """
        Сортирует триплетную строку в лексиграфическом порядке по префиксу и имени триплетов
        """
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
    :raises TypeError: если элемент не str, int, float, bool, Trp, TrpExpr

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
            elif not isinstance(item, (str, int, float, TrpExpr)) or isinstance(item, bool):
                raise TypeError(
                    'Элемент должен быть str, int, float, Trp, TrpExpr, не ' + type_name(item),
                    item
                )
        self.items = items  #: Операнды и операторы в триплетном выражении

    def __str__(self):
        items_trp_expr_sprtr = TrpExpr.settings.trp_expr_items_sprtr
        return items_trp_expr_sprtr.join(str(item) for item in self.items)

    def __repr__(self):
        return 'TrpExpr({})'.format(', '.join(repr(item) for item in self.items))

    def calculate(self, source=None, special_source=None):
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
            >>> expr.calculate(trp_str)
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
                result.append(str(item.calculate(source, special_source)))
            else:
                result.append(str(item))

        # TODO переписать с использованием модуля operator
        return eval(''.join(result), {'__builtins__': {}})

# настройка валидации значения триплетов
# сделано следующим образом, так как классы Trp и TrpExpr объявляются после объявления VSPTDSettings
VSPTDSettings.value_types = (str, int, float, Trp, TrpExpr)
