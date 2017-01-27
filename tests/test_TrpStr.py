# -*- coding: utf-8 -*-
import unittest

from vsptd.vsptd import Trp, TrpStr


class TestTrpStr(unittest.TestCase):
    def test_init_with_different_types_of_items(self):
        """Инициализация с различными типами параметров"""
        TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'))

        items = ['', 0, True, Trp]
        for item in items:
            with self.subTest(item=item), self.assertRaises(TypeError):
                    TrpStr(Trp('A', 'B', 'C'), item)

    def test_add(self):
        """Сложение"""
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'))
        _trp_str2 = TrpStr(Trp('J', 'K', 'L'), Trp('M', 'N', 'O'))
        _trp_str3 = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('J', 'K', 'L'), Trp('M', 'N', 'O'))
        _trp_str4 = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('J', 'K', 'L'))
        _trp = Trp('J', 'K', 'L')

        self.assertIsInstance(
            _trp_str + _trp_str2,
            TrpStr
        )
        self.assertIsInstance(
            _trp_str + _trp,
            TrpStr
        )

        self.assertCountEqual(
            _trp_str3,
            _trp_str + _trp_str2
        )
        self.assertCountEqual(
            _trp_str4,
            _trp_str + _trp
        )

        # метод add
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'))
        _trp_str2 = TrpStr(Trp('J', 'K', 'L'), Trp('M', 'N', 'O'))
        _trp_str3 = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('J', 'K', 'L'), Trp('M', 'N', 'O'))

        self.assertEqual(None, _trp_str.add(_trp_str2))
        self.assertCountEqual(_trp_str3, _trp_str)

        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'))
        _trp_str4 = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('J', 'K', 'L'))
        _trp = Trp('J', 'K', 'L')

        self.assertEqual(None, _trp_str.add(_trp))
        self.assertCountEqual(_trp_str4, _trp_str)

    # def test_equal(self):
    #     self.assertCountEqual(self.trpStr + self.trp, self.trp + self.trpStr)
    #     self.assertEqual(self.trpStr + self.trp, self.trp + self.trpStr)
    #     self.assertNotEqual(self.trpStr,
    #                         TrpStr(Trp('Z', 'X', 'Y'), Trp('Q', 'R', 'S'))
    #                         )

    def test_contains(self):
        """Наличие триплета в триплетной строке"""
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('J', 'K', 'L'), Trp('M', 'N', 'O'))

        self.assertEqual(True, 'A' in _trp_str)
        self.assertEqual(True, ('A', 'B') in _trp_str)
        self.assertEqual(False, 'Q' in _trp_str)
        self.assertEqual(False, ('Q', 'R') in _trp_str)

    def test_iter(self):
        """Итерация"""
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'))

        self.assertCountEqual([Trp('A', 'B', 'C'), Trp('D', 'E', 'F')], list(_trp_str))
        self.assertCountEqual((Trp('A', 'B', 'C'), Trp('D', 'E', 'F')), tuple(_trp_str))

    def test_get(self):
        """Получение триплетов по префиксу или префиксу и имени"""
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'R', 'H'))

        self.assertEqual(Trp('A', 'B', 'C'), _trp_str.get('A', 'B'))
        self.assertEqual(Trp('A', 'B', 'C'), _trp_str['A', 'B'])

        self.assertCountEqual(TrpStr(Trp('A', 'B', 'C'), Trp('A', 'R', 'H')), _trp_str.getpr('A'))
        self.assertCountEqual(TrpStr(Trp('A', 'B', 'C'), Trp('A', 'R', 'H')), _trp_str['A'])

    def test_del(self):
        """Удаление триплетов по префиксу или префиксу и имени"""
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'R', 'H'))
        self.assertEqual(None, _trp_str.rem('A', 'B'))
        self.assertCountEqual(TrpStr(Trp('D', 'E', 'F'), Trp('A', 'R', 'H')), _trp_str)

        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'R', 'H'))
        del _trp_str['A', 'B']
        self.assertCountEqual(TrpStr(Trp('D', 'E', 'F'), Trp('A', 'R', 'H')), _trp_str)

        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'R', 'H'))
        self.assertEqual(None, _trp_str.rempr('A'))
        self.assertCountEqual(TrpStr(Trp('D', 'E', 'F')), _trp_str)

        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'R', 'H'))
        del _trp_str['A']
        self.assertCountEqual(TrpStr(Trp('D', 'E', 'F')), _trp_str)
