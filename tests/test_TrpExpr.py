# -*- coding: utf-8 -*-
import unittest

from vsptd.vsptd import Trp, TrpStr, TrpExpr


class TestTrpExpr(unittest.TestCase):
    def test_str(self):
        """Строковое представление"""
        expr = TrpExpr(Trp('A', 'B'), '*', Trp('C', 'D'))
        self.assertEqual('$A.B*$C.D', str(expr))
        self.assertEqual('$E.F=$A.B*$C.D;', str(Trp('E', 'F', expr)))

    def test_calculate(self):
        """Метод calculate"""
        expr = TrpExpr(Trp('A', 'B'), '*', Trp('C', 'D'), '/', Trp('E', 'F', special=True))
        trp_str = TrpStr(Trp('A', 'B', 21), Trp('C', 'D', 2))
        trp_str_spec = TrpStr(Trp('E', 'F', 1))
        self.assertEqual(42, expr.calculate(trp_str, trp_str_spec))

        expr2 = TrpExpr(expr, '*', 2)
        self.assertEqual(84, expr2.calculate(trp_str, trp_str_spec))
