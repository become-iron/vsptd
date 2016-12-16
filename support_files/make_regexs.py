# -*- coding: utf-8 -*-


def islt_re(x):
    # обособление рег. выражения знаками начала и конца слова ('^', '$')
    return '^' + x + '$'


# WODS - without dollar sign ('$')
# NI - not isolated by '^' and '$'
RE_PREFIX = r'(?!.{25})[A-Za-z]+\d*'  # не для включения в другие выражения
_RE_PREFIX = r'(?=.{0,24}\.)[A-Za-z]+\d*'  # для составных выражений только
RE_NAME = '[A-Za-z]+'
RE_VALUE = r"'?[\wА-Яа-яЁё ()-.:?–—−]*'?"
RE_PREFIX_NAME_WODS = _RE_PREFIX + '\.' + RE_NAME
RE_PREFIX_NAME = '\$' + RE_PREFIX_NAME_WODS
RE_TRIPLET_WODS = '(' + _RE_PREFIX + ')\.(' + RE_NAME + ')=(' + RE_VALUE + ');'
RE_TRIPLET = '\$' + RE_TRIPLET_WODS

RE_FUNC_PRESENT = '(?:есть|ЕСТЬ)\(' + RE_PREFIX_NAME + '\)'
RE_FUNC_PRESENT_WODS = '(?:есть|ЕСТЬ)\(' + RE_PREFIX_NAME_WODS + '\)'
RE_FUNC_ABSENCE = '(?:нет|НЕТ)\(' + RE_PREFIX_NAME + '\)'
RE_FUNC_ABSENCE_WODS = '(?:нет|НЕТ)\(' + RE_PREFIX_NAME_WODS + '\)'
RE_SLICE = r'(\[(\d+),(\d+)\])'  # срез [n,n]

# правило и действия
RE_RULE = 'ЕСЛИ (.+) ТО (.+);'  # правило
RE_ACT_FIND_IN_DB = r'НАЙТИ_В_БД\((.*)\)'  # искать в БД
RE_ACT_FIND_IN_DB_WO = r'НАЙТИ_В_БД\((.*)\\\\(.*)(\+|-)\\\\\)'  # искать в БД (with order by)
RE_ACT_ADD_IN_DB = 'ДОБАВИТЬ_В_БД\((' + _RE_PREFIX + ')\)'  # добавить в БД
RE_ACT_DEL_FROM_DB = 'УДАЛИТЬ_В_БД\((' + _RE_PREFIX + ')\)'  # удалить из БД

# реквизит
RE_RQST = '\$(' + _RE_PREFIX + ')\.(' + RE_NAME + ')(?:(\||:)(' + RE_VALUE + ')?)?'

# RE_FUNC_PRESENT = '(?:есть|ЕСТЬ)\(\$[A-Za-z]\.[A-Za-z]+\)'  # функция ЕСТЬ
# RE_FUNC_PRESENT_WODS = '(?:есть|ЕСТЬ)\([A-Za-z]\.[A-Za-z]+\)'  # функция ЕСТЬ без $
# RE_FUNC_ABSENCE = '(?:нет|НЕТ)\(\$[A-Za-z]\.[A-Za-z]+\)'  # функция НЕТ
# RE_FUNC_ABSENCE_WODS = '(?:нет|НЕТ)\([A-Za-z]\.[A-Za-z]+\)'  # функция НЕТ без $
# RE_SLICE = '(\[(\d+),(\d+)\])')  # срез [n,n]

# RE_PREFIX = islt_re(RE_PREFIX))  # префикс: 1 латинский символ
# RE_NAME = islt_re(RE_NAME))  # имя: латинские символы и, возможно, число
# RE_VALUE = islt_re(RE_VALUE))  # значение
# RE_PREFIX_NAME_WODS_NI = RE_PREFIX_NAME_WODS)  # префикс.имя
# RE_PREFIX_NAME_WODS = islt_re(RE_PREFIX_NAME_WODS))  # префикс.имя
# RE_PREFIX_NAME_NI = RE_PREFIX_NAME)  # $префикс.имя
# RE_PREFIX_NAME = islt_re(RE_PREFIX_NAME))  # $префикс.имя
# RE_TRIPLET = RE_TRIPLET)  # триплет
# RE_TRIPLET_WODS = RE_TRIPLET_WODS)  # триплет без $)

regexs = (('RE_PREFIX', islt_re(RE_PREFIX)),
          ('RE_NAME', islt_re(RE_NAME)),
          ('RE_VALUE', islt_re(RE_VALUE)),
          ('RE_PREFIX_NAME_WODS_NI', RE_PREFIX_NAME_WODS),
          ('RE_PREFIX_NAME_WODS', islt_re(RE_PREFIX_NAME_WODS)),
          ('RE_PREFIX_NAME_NI', RE_PREFIX_NAME),
          ('RE_PREFIX_NAME', islt_re(RE_PREFIX_NAME)),
          ('RE_TRIPLET_WODS', RE_TRIPLET_WODS),
          ('RE_TRIPLET', RE_TRIPLET),

          ('RE_FUNC_PRESENT', RE_FUNC_PRESENT),
          ('RE_FUNC_PRESENT_WODS', RE_FUNC_PRESENT_WODS),
          ('RE_FUNC_ABSENCE', RE_FUNC_ABSENCE_WODS),
          ('RE_FUNC_ABSENCE_WODS', RE_FUNC_ABSENCE_WODS),
          ('RE_SLICE', RE_SLICE),

          # правило и действия
          ('RE_RULE', islt_re(RE_RULE)),
          ('RE_ACT_FIND_IN_DB', islt_re(RE_ACT_FIND_IN_DB)),
          ('RE_ACT_FIND_IN_DB_WO', islt_re(RE_ACT_FIND_IN_DB_WO)),
          ('RE_ACT_ADD_IN_DB', islt_re(RE_ACT_ADD_IN_DB)),
          ('RE_ACT_DEL_FROM_DB', islt_re(RE_ACT_DEL_FROM_DB)),

          # реквизиты
          ('RE_RQST', RE_RQST)
          )

for r in regexs:
    # print('{} = r"{}"'.format(r[0], r[1]))
    print('{} = re.compile(r"{}")'.format(r[0], r[1]))
