# -*- coding: utf-8 -*-
import unittest

from vsptd.vsptd import Trp, TrpStr, TrpExpr, VSPTDSettings


class TestVSPTDSettings(unittest.TestCase):
    def test_change_attr(self):
        """Изменение настроек ВСПТД"""
        setts = VSPTDSettings()
        setts.bid = '*'
        setts.prefix_max = 50
        setts.name_min = 10
        setts.comment_regexp = r'.*'

        self.assertEqual(setts.bid, '*')
        self.assertEqual(setts.prefix_max, 50)
        self.assertEqual(setts.name_min, 10)
        self.assertEqual(setts.comment_regexp, r'.*')

    def test_validate(self):
        """Метод validate"""
        setts = VSPTDSettings()
        # префикс
        with self.assertRaises(ValueError):
            setts.validate(prefix='Q' * 100)
        with self.assertRaises(ValueError):
            setts.validate(prefix='eqe')
        with self.assertRaises(ValueError):
            setts.validate(prefix='Ю')
        with self.assertRaises(TypeError):
            setts.validate(prefix=123)

        # имя
        with self.assertRaises(ValueError):
            setts.validate(name='Q' * 100)
        with self.assertRaises(ValueError):
            setts.validate(name='eqe')
        with self.assertRaises(ValueError):
            setts.validate(name='Ю')
        with self.assertRaises(TypeError):
            setts.validate(name=123)

        # значение
        with self.assertRaises(TypeError):
            setts.validate(value=TrpStr())

        # значение-строка
        with self.assertRaises(ValueError):
            setts.validate(value='Q' * 500)
        setts.validate(value='')
        setts.validate(value='sdf2342выава!"№;%:?*()')

        # комментарий
        with self.assertRaises(ValueError):
            setts.validate(comment='Q' * 500)
        setts.validate(comment='')
        setts.validate(comment='sdf2342выава!"№;%:?*()')
        with self.assertRaises(TypeError):
            setts.validate(comment=123)

    def test_to_dict(self):
        """Метод to_dict"""
        setts = VSPTDSettings()
        # стандартные настройки;
        def_setts = dict(
            bid=':',
            trp_start='$',
            trp_pn_sprtr='.',
            trp_nv_sprtr='=',
            trp_end=';',
            trp_val_str_isltr='\'',
            trp_comment_isltr='"',
            trps_sprtr=' ',
            trp_expr_items_sprtr='',
            prefix_max=32,
            prefix_min=1,
            prefix_regexp=r'[A-Z]+\d*',
            prefix_types=(str,),
            name_max=32,
            name_min=1,
            name_regexp=r'[A-Z]+',
            name_types=(str,),
            value_str_max=256,
            value_str_min=0,
            value_str_regexp=None,
            value_types=(str, int, float, Trp, TrpExpr),
            comment_max=256,
            comment_min=0,
            comment_regexp=None,
            comment_types=(str,),
        )
        self.assertEqual(setts.to_dict(), def_setts)

    def test_from_dict(self):
        """Метод from_dict"""
        setts_to_set = dict(
            trp_start='^',
            trp_end='$',
            trps_sprtr='?',
            prefix_max=40,
            value_str_regexp='.*',
        )
        setts = VSPTDSettings()
        setts.from_dict(setts_to_set)

        self.assertEqual(setts.trp_start, '^')
        self.assertEqual(setts.trp_end, '$')
        self.assertEqual(setts.trps_sprtr, '?')
        self.assertEqual(setts.prefix_max, 40)
        self.assertEqual(setts.value_str_regexp, '.*')

        # проверка, что свойства класса не изменились
        self.assertEqual(VSPTDSettings.prefix_max, 32)
        self.assertEqual(VSPTDSettings.value_str_regexp, None)
        self.assertEqual(VSPTDSettings.trp_end, ';')
        self.assertEqual(VSPTDSettings.trp_start, '$')
        self.assertEqual(VSPTDSettings.trps_sprtr, ' ')
