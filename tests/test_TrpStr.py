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

    def test_bool(self):
        """Приведение к bool"""
        self.assertEqual(False, bool(TrpStr()))
        self.assertEqual(True, bool(TrpStr(Trp('A', 'B', 'C'))))

    def test_equal(self):
        """Проверка на равенство"""
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'))
        _trp_str2 = TrpStr(Trp('J', 'K', 'L'), Trp('M', 'N', 'O'))
        _trp = Trp('J', 'K', 'L')

        self.assertEqual(_trp_str + _trp, _trp + _trp_str)
        self.assertEqual(_trp_str + _trp_str2, _trp_str2 + _trp_str)
        self.assertNotEqual(TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F')),
                            TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('J', 'K', 'L')))
        self.assertNotEqual(TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('J', 'K', 'L')),
                            TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F')))

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

    def test_reversed(self):
        """Реверсная итерация"""
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        self.assertEqual((Trp('D', 'E', 'F'), Trp('A2', 'D', 'C'), Trp('A', 'D', 'C'), Trp('A', 'B', 'C')),
                         tuple(reversed(_trp_str)))

    def test_sort(self):
        """Сортировка"""
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        _trp_str.sort()

    def test_order(self):
        """Порядок триплетов"""
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'))
        _trp_str2 = TrpStr(Trp('A', 'D', 'C'), Trp('A', 'B', 'C'))
        self.assertNotEqual(tuple(_trp_str), tuple(_trp_str2))

        # сохранение позиции триплета после обновления
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'))
        _trp_str.add(Trp('A', 'B', 'E'))
        self.assertEqual(tuple(_trp_str), tuple(TrpStr(Trp('A', 'B', 'E'), Trp('A', 'D', 'C'))))

        # новый триплет добавляется в конец
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'))
        _trp_str.add(Trp('D', 'B', 'E'))
        self.assertEqual(tuple(_trp_str), tuple(TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'), Trp('D', 'B', 'E'))))

    def test_index(self):
        """Метод index"""
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        self.assertEqual(1, _trp_str.index(Trp('A', 'D', 'C')))
        with self.assertRaises(ValueError):
            _trp_str.index(Trp('A', 'A', 'A'))

    def test_get(self):
        """Получение триплетов по префиксу, или префиксу и имени, или по индексу, или по срезу"""
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))

        # по префиксу и имени
        self.assertEqual(Trp('A', 'B', 'C'), _trp_str.get('A', 'B'))
        self.assertEqual(Trp('A', 'B', 'C'), _trp_str['A', 'B'])

        # по префиксу
        self.assertCountEqual(TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C')), _trp_str.getpr('A'))
        self.assertCountEqual(TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C')), _trp_str['A'])

        # по индексу
        self.assertEqual(Trp('A', 'D', 'C'), _trp_str[1])
        self.assertEqual(Trp('D', 'E', 'F'), _trp_str[-1])  # отрицательный индекс
        with self.assertRaises(IndexError):
            _ = _trp_str[50]

        # по срезу
        # TODO
        self.assertEqual(TrpStr(Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F')), _trp_str[1:])
        self.assertEqual(TrpStr(Trp('A', 'B', 'C'),  Trp('A2', 'D', 'C')), _trp_str[::2])
        self.assertEqual(TrpStr(Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C')), _trp_str[1:3])
        self.assertEqual(TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F')),
                         _trp_str[:100])

    def test_rem(self):
        """Удаление триплетов по префиксу, или префиксу и имени, или по индексу, или по срезу"""
        # по префиксу и имени
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        _trp_str.rem('A', 'B')
        self.assertCountEqual(TrpStr(Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F')), _trp_str)

        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        del _trp_str['A', 'B']
        self.assertCountEqual(TrpStr(Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F')), _trp_str)

        # по префиксу
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        _trp_str.rempr('A')
        self.assertCountEqual(TrpStr(Trp('A2', 'D', 'C'), Trp('D', 'E', 'F')), _trp_str)

        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        del _trp_str['A']
        self.assertCountEqual(TrpStr(Trp('A2', 'D', 'C'), Trp('D', 'E', 'F')), _trp_str)

        # по префиксу, нестрогое
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        _trp_str.rempr('A', strict=False)
        self.assertCountEqual(TrpStr(Trp('D', 'E', 'F')), _trp_str)

        # по индексу
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        del _trp_str[1]
        self.assertEqual(TrpStr(Trp('A', 'B', 'C'), Trp('A2', 'D', 'C'), Trp('D', 'E', 'F')),
                         _trp_str)
        with self.assertRaises(IndexError):
            del _trp_str[50]

        # по отрицательному индексу
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        del _trp_str[-1]
        self.assertEqual(TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C')),
                         _trp_str)
        del _trp_str[-2]
        self.assertEqual(TrpStr(Trp('A', 'B', 'C'), Trp('A2', 'D', 'C')),
                         _trp_str)

        # по срезу
        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        del _trp_str[1:]
        self.assertEqual(TrpStr(Trp('A', 'B', 'C')), _trp_str)

        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        del _trp_str[::2]
        self.assertEqual(TrpStr(Trp('A', 'D', 'C'), Trp('D', 'E', 'F')), _trp_str)

        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        del _trp_str[1:3]
        self.assertEqual(TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F')), _trp_str)

        _trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('A', 'D', 'C'),  Trp('A2', 'D', 'C'), Trp('D', 'E', 'F'))
        del _trp_str[:100]
        self.assertEqual(TrpStr(), _trp_str)
