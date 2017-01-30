# -*- coding: utf-8 -*-
import re
# from collections import OrderedDict

from vsptd.support import type_name

__all__ = ('VSPTDSettings', 'Trp', 'TrpStr', 'TrpExpr')


# noinspection SpellCheckingInspection
class VSPTDSettings:
    """
    **Хранение настроек параметров ВСПТД-объектов и правил валидации строковых значений**

    Правила валидации значений представлены в виде регулярных выражений (RegExp).

    :Пример работы:
        >>> settings = VSPTDSettings()
        >>> settings.prefix.max = 100
        >>> settings.trp_start = '~'
    """
    bid = ':'  #: Заявка. См. описание ВСПТД

    trp_start = '$'  #: Начало триплета
    trp_pn_sprtr = '.'  #: Разделитель префикса и имени триплета
    trp_nv_sprtr = '='  #: Разделитель имени и значения триплета
    trp_end = ';'  #: Конец триплета
    trp_val_str_isltr = '\''  #: Обособление значения-строки триплета
    trp_comment_isltr = '"'  #: Обособление комментария триплета
    trps_sprtr = ' '  #: Разделитель триплетов в триплетной строке :class:`TrpStr`
    items_trp_expr_sprtr = ' '  #: Разделитель операторов и операндов в триплетном выражении :class:`TrpExp`

    # для удобного доступа к параметрам
    class __TrpSettings:
        def __init__(self, min_len, max_len, regexp):
            self.min = min_len  #: Минимальная длина параметра
            self.max = max_len  #: Максимальная длина параметра
            self.regexp = regexp  #: RegExp для проверки параметра триплета

        def __repr__(self):
            return '<TrpSettings(min=%r, max=%r, regexp=%r)>' % (self.min, self.max, self.regexp)

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
        return '<%s>' % VSPTDSettings.__name__

    def validate_prefix(self, prefix: str) -> None:
        """
        Проверяет корректность префикса триплета

        :param str prefix: префикс
        :raises ValueError: префикс несоответствующей длины
        :raises ValueError: префикс не удовлетворяет соответствующему формату
        """
        min_len, max_len, regexp = self.prefix.min, self.prefix.max, self.prefix.regexp
        if not (min_len <= len(prefix) <= max_len):
            raise ValueError(
                'Длина префикса должна быть от %s до %s, не %s' % (min_len, max_len, len(prefix)), prefix
            )
        elif re.fullmatch(regexp, prefix) is None:
            raise ValueError('Префикс не удовлетворяет соответствующим требованиям', prefix)

    def validate_name(self, name: str) -> None:
        """
        Проверяет корректность имени триплета

        :param str name: имя
        :raises ValueError: имя несоответствующей длины
        :raises ValueError: имя не удовлетворяет соответствующему формату
        """
        min_len, max_len, regexp = self.name.min, self.name.max, self.name.regexp
        if not (min_len <= len(name) <= max_len):
            raise ValueError(
                'Длина имени должна быть от %s до %s, не %s' % (min_len, max_len, len(name)), name
            )
        elif re.fullmatch(regexp, name) is None:
            raise ValueError('Имя не удовлетворяет соответствующим требованиям', name)

    def validate_value(self, value_str) -> None:
        """
        Проверяет корректность значения-строки триплета

        :param str value_str: значение-строка
        :raises ValueError: значение несоответствующей длины
        :raises ValueError: значение не удовлетворяет соответствующему формату
        """
        min_len, max_len, regexp = self.value.min, self.value.max, self.value.regexp
        if not (min_len <= len(value_str) <= max_len):
            raise ValueError(
                'Длина значения должна быть от %s до %s, не %s' % (min_len, max_len, len(value_str)), value_str
            )
        elif re.fullmatch(regexp, value_str) is None:
            raise ValueError('Значение не удовлетворяет соответствующим требованиям', value_str)

    def validate_comment(self, comment) -> None:
        """
        Проверяет корректность комментария триплета

        :param str comment: комментарий
        :raises ValueError: комментарий несоответствующей длины
        :raises ValueError: комментарий не удовлетворяет соответствующему формату
        """
        min_len, max_len, regexp = self.comment.min, self.comment.max, self.comment.regexp
        if not (min_len <= len(comment) <= max_len):
            raise ValueError(
                'Длина комментария должна быть от %s до %s, не %s' % (min_len, max_len, len(comment)), comment
            )
        elif re.fullmatch(regexp, comment) is None:
            raise ValueError('Комментарий не удовлетворяет соответствующим требованиям', comment)


# noinspection SpellCheckingInspection
class Trp:
    """
    **Триплет**

    При создании триплета и изменении его значений производится
    валидация, в результате чего могут возникнуть различные ошибки.
    См. дополнительно в описании ВСПТД требования к параметрам триплета.

    :Примечания:
        * свойства `prefix` и `name` недоступны для изменения после создания триплета;
        * если не указано значение триплета, то созданный триплет может использоваться
          как триплет-ссылка в значении другого триплета или в триплетном выражении :class:`TrpExpr`:

            >>> print(Trp('A', 'B', Trp('C', 'D')))
            $A.B=$C.D;

    :param str prefix:  префикс триплета
    :param str name: имя триплета
    :param value: значение триплета; None по умолчанию
    :type value: str, int, float, bool, Trp, TrpExpr, необяз.
    :param comment: комментарий; пустая строка по умолчанию
    :type comment: str, необяз.
    :param special: "особенный" триплет
    :type special: bool, необяз.
    :param bid: заявка
    :type bid: bool, необяз.

    :raises TypeError: если параметры не соответствующих типов
    :raises ValueError: если параметры не удовлетворяют соответствующим требованиям
    :raises ValueError: при попытке использовать в качестве значения триплет, не являющийся триплетом-ссылкой
    :raises AttributeError: при попытке изменить свойства `prefix` и `name`

    :Пример работы:
        >>> Trp('A', 'B', 'C')
        Trp(prefix='A', name='B', value='C')
    """
    # TODO нужна ли проверка при различных сочетаниях параметров?
    #: Настройки конфигурации ВСПТД :class:`VSPTDSettings`; по умолчанию используются стандартные
    settings = VSPTDSettings()

    __slots__ = ('__prefix', '__name', '__value', '__comment', '__special', '__bid')

    def __init__(self, prefix: str, name=None, value=None, comment=None, special=False, bid=False):
        if not isinstance(prefix, str):
            raise TypeError('Префикс должен быть str, не ' + type_name(prefix), prefix)
        if not isinstance(name, str) and name is not None:
            raise TypeError('Имя должно быть str, не ' + type_name(name), name)

        self.settings.validate_prefix(prefix)
        if isinstance(name, str):
            self.settings.validate_name(name)
        self.__prefix = prefix
        self.__name = name
        # установка свойств value, comment, special, bind выполняется
        # таким образом с целью их валидации через setter'ы
        self.__value = None
        self.value = value
        self.__comment = None
        self.comment = comment
        self.__special = False
        self.special = special
        self.__bid = False
        self.bid = bid

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
        if not isinstance(value, (str, int, float, bool, Trp, TrpExpr)) and value is not None:
            raise TypeError(
                'Значение должно быть str, int, float, bool, Trp, TrpExpr, не ' + type_name(value),
                value
            )
        if isinstance(value, Trp) and value.value is None and value.bid:
            raise ValueError('В качестве значения можно использовать только триплет-ссылку', value)
        if isinstance(value, str):
            self.settings.validate_value(value)
        self.__value = value

    @property
    def comment(self):
        """Комментарий триплета"""
        return self.__comment

    @comment.setter
    def comment(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError('Комментарий должен быть str, не ' + type_name(value), value)
        if value != '' and value is not None:
            self.settings.validate_comment(value)
        self.__comment = value

    @property
    def special(self):
        return self.__special

    @special.setter
    def special(self, value):
        """Параметр special"""
        if not isinstance(value, bool):
            raise TypeError('Параметр special должен быть bool, не ' + type_name(value), value)
        self.__special = value

    @property
    def bid(self):
        return self.__bid

    @bid.setter
    def bid(self, value):
        """Заявка"""
        if not isinstance(value, bool):
            raise TypeError('Параметр заявки должен быть bool, не ' + type_name(value), value)
        self.__bid = value

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
            # если не указано значение триплета и это не заявка, то считаем, что это триплет-ссылка
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
        result = 'Trp(prefix=%r' % self.prefix
        if self.name is not None:
            result += ', name=%r' % self.name
        if self.value is not None:
            result += ', value=%r' % self.value
        if self.comment is not None:
            result += ', comment=%r' % self.comment
        if self.special:
            result += ', special=%r' % self.special
        if self.bid:
            result += ', bid=%r' % self.bid
        result += ')'
        return result

    def __eq__(self, other):
        # TODO проверять ли и комментарий, special, bid?
        return isinstance(other, Trp) and \
               self.prefix == other.prefix and \
               self.name == other.name and \
               self.value == other.value


# noinspection SpellCheckingInspection
class TrpStr:
    """
    **Триплетная строка**

    :param `*trps`: триплеты :class:`Trp`
    :raises TypeError: если параметры не :class:`Trp`
    :Пример работы:
        >>> TrpStr(Trp('A', 'B', 'C'))
        TrpStr(Trp(prefix='A', name='B', value='C'))
    """
    # TODO важен порядок триплетов в трипл. строке? - можно использовать OrderedDict
    __slots__ = ('__trps',)

    #: Настройки конфигурации ВСПТД :class:`VSPTDSettings`; по умолчанию используются стандартные
    settings = VSPTDSettings()

    def __init__(self, *trps):
        # self.__trps = OrderedDict()
        self.__trps = {}
        for trp in trps:
            # все ли аргументы — триплеты
            if not isinstance(trp, Trp):
                raise TypeError('Должен быть Trp, не ' + type_name(trp), trp)
            self.__trps.update({(trp.prefix, trp.name): trp})

    def __str__(self):
        trps_sprtr = self.settings.trps_sprtr
        return trps_sprtr.join(str(trp) for trp in self.__trps.values())

    def __repr__(self):
        return 'TrpStr({})'.format(', '.join(repr(trp) for trp in self.__trps.values()))

    def __len__(self):
        return len(self.__trps)

    def __getitem__(self, key):
        if isinstance(key, (tuple, list)):
            return self.get(*key)
        elif isinstance(key, str):
            return self.getpr(key)

    def __delitem__(self, key):
        if isinstance(key, (tuple, list)):
            self.rem(*key)
        elif isinstance(key, str):
            self.rempr(key)

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
        # TODO валидация?
        # префикс
        if isinstance(item, str):
            for prefix, name in self.__trps:
                if prefix == item:
                    return True
            return False
        # (префикс, имя)
        elif isinstance(item, (tuple, list)):
            return tuple(item) in self.__trps
        else:
            raise TypeError('Должен быть str, tuple, list, не ' + type_name(item), item)

    def __eq__(self, other):
        return isinstance(other, TrpStr) and self.__trps == other.__trps

    def __add__(self, other):
        if isinstance(other, Trp):
            result = TrpStr()
            result.__trps.update(self.__trps)
            result.__trps.update({(other.prefix, other.name): other})
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
            self.__trps.update({(other.prefix, other.name): other})
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

        :raises KeyError: если по заданным префиксу и имени триплет не найден
        :raises ValueError: префикс/имя не удовлетворяет соответствующим требованиям
        """
        self.settings.validate_prefix(prefix)
        if isinstance(name, str):
            self.settings.validate_name(name)

        try:
            return self.__trps[prefix, name]
        except KeyError:
            raise KeyError('По заданным префиксу и имени триплет не найден', (prefix, name))

    def getpr(self, prefix: str):
        """
        Возвращает из триплетной строки триплеты по заданному префиксу

        Эквивалентно ``<TrpStr>[prefix]``

        :param str prefix: префикс
        :rtype: TrpStr

        :raises KeyError: если по заданному префиксу триплетов не найдено
        :raises ValueError: префикс не удовлетворяет соответствующим требованиям
        """
        self.settings.validate_prefix(prefix)

        result = TrpStr()
        result.__trps.update({key: self.__trps[key] for key in self.__trps if key[0] == prefix})
        if len(result.__trps) == 0:
            raise KeyError('По заданному префиксу триплетов не найдено', prefix)
        return result

    def rem(self, prefix: str, name) -> None:
        """
        Удаляет из триплетной строки триплет по заданным префиксу и имени

        Эквивалентно ``del <TrpStr>[prefix, name]``

        :param str prefix: префикс
        :param str name: имя параметра

        :raises KeyError: если по заданным префиксу и имени триплет не найден
        :raises ValueError: префикс/имя не удовлетворяет соответствующим требованиям
        """
        self.settings.validate_prefix(prefix)
        if isinstance(name, str):
            self.settings.validate_name(name)

        try:
            del self.__trps[prefix, name]
        except KeyError:
            raise KeyError('По заданным префиксу и имени триплет не найден', (prefix, name))

    def rempr(self, prefix: str) -> None:
        """
        Удаляет из триплетной строки все триплеты по заданному префиксу

        Эквивалентно ``del <TrpStr>[prefix]``

        :param str prefix: префикс

        :raises KeyError: если по заданному префиксу триплетов не найдено
        :raises ValueError: префикс не удовлетворяет соответствующим требованиям
        """
        # TODO Нужно ли учитывать для функции del_trp_pref триплеты с префиксами вида E, E1, E2
        # TODO оптимизировать
        self.settings.validate_prefix(prefix)

        count = len(self.__trps)
        self.__trps = {key: item for key, item in self.__trps.items() if key[0] != prefix}
        if count == len(self.__trps):
            raise KeyError('По заданному префиксу триплетов не найдено', prefix)

    # def sort(self) -> None:
    #     """
    #     Сортирует триплетную строку в лексиграфическом порядке по префиксу и имени триплетов
    #     """
    #     self._trps = OrderedDict(sorted(self._trps.items(), key=lambda item: item[0]))


class TrpExpr:
    """
    **Триплетное выражение**

    :Примечания:
        * операторы должны быть в виде строк `str`.
    :param `*items`: параметры
    :type `*items`: str, int, float, bool, Trp

    :raises TypeError: если элемент не str, int, float, bool или Trp
    :Пример работы:
        >>> expr = TrpExpr( Trp('A', 'B'), '*', Trp('C', 'D') )
        >>> print(expr)
        $A.B*$C.D
        >>> print(Trp('E', 'F', expr))
        $E.F=$A.B*$C.D;
    """
    # TODO
    __slots__ = ('items',)

    #: Настройки конфигурации ВСПТД :class:`VSPTDSettings`; по умолчанию используются стандартные
    settings = VSPTDSettings()

    def __init__(self, *items):
        for item in items:
            if not isinstance(item, (str, int, float, bool, Trp)):
                raise TypeError(
                    'Элемент должен быть str, int, float, bool, Trp, не ' + type_name(item),
                    item
                )
        self.items = items  #: операнды и операторы в триплетном выражении

    def __str__(self):
        return ''.join(str(item) for item in self.items)

    def __repr__(self):
        return 'TrpExpr({})'.format(', '.join(repr(item) for item in self.items))

    def compute(self, source=None, special_source=None):
        """
        Вычисляет выражение

        :param TrpStr source:
        :param TrpStr special_source:
        :return: результат вычисления выражения
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

        return eval(''.join(result))

    # def to_sql(self):
    #     """
    #     Возвращает выражение в виде sql запроса
    #     """
    #     pass
