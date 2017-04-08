# -*- coding: utf-8 -*-
# import sys
# sys.path.append('../')
import unittest

from vsptd.vsptd import Trp, TrpStr, TrpExpr


class TestTrp(unittest.TestCase):
    def test_init_with_different_amounts_of_params(self):
        """Инициализация с различным числом параметров"""
        Trp('A', 'B')
        Trp('A', 'B', 'C')
        Trp('A', 'B', 'C', 'D')

        Trp('A', 'B', special=True)
        Trp('A', 'B', 'C', 'D', True)

    def test_init_with_different_types_of_params(self):
        """Инициализация с различными типами параметров (кроме параметра value)"""
        with self.assertRaises(TypeError):
            Trp(0, 'A')
        with self.assertRaises(TypeError):
            Trp('A', 0)
        with self.assertRaises(TypeError):
            Trp('A', 'B', 'C', comment=0)
        with self.assertRaises(TypeError):
            Trp('A', 'B', 'C', special=0)

    def test_str_with_different_types_of_trp_value(self):
        """Различные типы значения триплета"""
        # str
        self.assertEqual("$A.B='C';", str(Trp('A', 'B', 'C')))
        # int
        self.assertEqual("$A.B=0;", str(Trp('A', 'B', 0)))
        # float
        self.assertEqual("$A.B=1.5;", str(Trp('A', 'B', 1.5)))
        # Trp (триплет-цель)
        self.assertEqual('$A.B=$C.D;', str(Trp('A', 'B', Trp('C', 'D'))))
        # TrpExpr
        self.assertEqual('$E.F=$A.B*$C.D;', str(Trp('E', 'F', TrpExpr(Trp('A', 'B'), '*', Trp('C', 'D')))))

        # bool
        with self.assertRaises(TypeError):
            Trp('A', 'B', True)

    def test_attribute_access(self):
        """Доступ к параметрам"""
        # TODO
        trp = Trp('A', 'B', 'C', 'D', False)

        self.assertEqual('A', trp.prefix)
        self.assertEqual('B', trp.name)
        self.assertEqual('C', trp.value)
        self.assertEqual('D', trp.comment)
        self.assertEqual(False, trp.special)

        with self.assertRaises(AttributeError):
            Trp('A', 'B', 'C').prefix = 'E'
        with self.assertRaises(AttributeError):
            Trp('A', 'B', 'C').name = 'E'
        Trp('A', 'B', 'C').value = 'E'
        Trp('A', 'B', 'C').comment = 'E'
        Trp('A', 'B', 'C').special = True

    def test_validate_trp_params(self):
        """Валидация параметров"""
        # TODO
        # префикс
        items = ['', 'a', 'Б', '1a', 'A'*26, '<']
        for item in items:
            with self.subTest(item=item), self.assertRaises(ValueError):
                    Trp(item, 'B')

        # имя
        items = ['', 'a', 'Б', 'A'*26, '<']
        for item in items:
            with self.subTest(item=item), self.assertRaises(ValueError):
                    Trp('A', item)

    def test_str(self):
        """Строковое отображение"""
        # TODO
        self.assertEqual('A.B', str(Trp('A', 'B', special=True)))
        self.assertEqual('$A.B', str(Trp('A', 'B')))
        self.assertEqual('$A.B=\'C\';', str(Trp('A', 'B', 'C')))
        self.assertEqual('$A.B=\'C\'"D";', str(Trp('A', 'B', 'C', 'D')))

    def test_repr(self):
        """repr"""
        self.assertEqual('Trp(prefix=\'A\', name=\'B\')', repr(Trp('A', 'B')))
        self.assertEqual('Trp(prefix=\'A\', name=\'B\', value=\'C\')', repr(Trp('A', 'B', 'C')))
        self.assertEqual('Trp(prefix=\'A\', name=\'B\', value=\'C\', comment=\'D\')', repr(Trp('A', 'B', 'C', 'D')))

        self.assertEqual('Trp(prefix=\'A\', name=\'B\', special=True)', repr(Trp('A', 'B', special=True)))

    def test_add(self):
        """Сложение"""
        # триплет + триплет
        self.assertIsInstance(
            Trp('A', 'B', 'C') + Trp('D', 'E', 'F'),
            TrpStr
        )
        # триплет + триплетная строка
        self.assertIsInstance(
            Trp('A', 'B', 'C') + TrpStr(Trp('D', 'E', 'F'), Trp('G', 'H', 'I')),
            TrpStr
        )

        self.assertCountEqual(
            Trp('A', 'B', 'C') + Trp('D', 'E', 'F'),
            Trp('D', 'E', 'F') + Trp('A', 'B', 'C')
        )
        self.assertCountEqual(
            Trp('A', 'B', 'C') + TrpStr(Trp('D', 'E', 'F'), Trp('G', 'H', 'I')),
            TrpStr(Trp('D', 'E', 'F'), Trp('G', 'H', 'I')) + Trp('A', 'B', 'C')
        )

        items = ['', 0, 0.1, True, Trp, TrpExpr()]
        for item in items:
            with self.subTest(item=item), self.assertRaises(TypeError):
                    Trp('A', 'B', 'C') + item

    def test_equal(self):
        """Равенство"""
        # TODO сравнение с учётом комментария и special
        self.assertEqual(Trp('A', 'B', 'C'),
                         Trp('A', 'B', 'C'))
        self.assertNotEqual(Trp('A', 'B', 'C'),
                            {'prefix': 'A',
                             'name': 'B',
                             'value': 'C'}
                            )

        class MockTrp:
            def __init__(self):
                self.prefix = 'A'
                self.name = 'B'
                self.value = 'C'
                self.comment = 'D'

        self.assertNotEqual(Trp('A', 'B', 'C', 'D'), MockTrp())
