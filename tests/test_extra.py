# -*- coding: utf-8 -*-
import unittest

from vsptd.vsptd import Trp, TrpStr
from vsptd.extra import *


class TestEqualityWithOrdering(unittest.TestCase):
    """Функция eq_with_order"""
    def test(self):
        self.assertEqual(
            True,
            eq_with_order(
                TrpStr(Trp('A', 'B'), Trp('C', 'D')),
                TrpStr(Trp('A', 'B'), Trp('C', 'D'))
            )
        )
        self.assertEqual(
            False,
            eq_with_order(
                TrpStr(Trp('A', 'B'), Trp('C', 'D')),
                TrpStr(Trp('C', 'D'), Trp('A', 'B'))
            )
        )


class TestSatisfyBid(unittest.TestCase):
    """Функция satisfy_bid"""
    def test(self):
        my_trp_str = TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('A', 'R', 'H'))
        self.assertEqual(TrpStr(Trp('A', 'B', 'C'), Trp('A', 'R', 'H')), satisfy_bid(Trp('A', bid=True), my_trp_str))
        self.assertEqual(Trp('A', 'B', 'C'), satisfy_bid(Trp('A', 'B', bid=True), my_trp_str))


class TestVSPTDTechProcTable(unittest.TestCase):
    """Класс VSPTDTechProcTable"""
    def test_init(self):
        _ = VSPTDTechProcTable(
            TrpStr(Trp('A', 'N', '0000'), Trp('P', 'N', '000'), Trp('P', 'KWO', '000'), Trp('Q', 'DI', '00')),
            TrpStr(Trp('A', 'N', 1), Trp('P', 'N', 3), Trp('P', 'KWO', '000'), Trp('Q', 'DI', '00')),
        )

    def test_str(self):
        """Строковое представление"""
        _ = VSPTDTechProcTable(
            TrpStr(Trp('A', 'N', '0000'), Trp('P', 'N', '000'), Trp('P', 'KWO', '000'), Trp('Q', 'DI', '00')),
            TrpStr(Trp('A', 'N', 1), Trp('P', 'N', 3), Trp('P', 'KWO', '000'), Trp('Q', 'DI', '00')),
        )
        self.assertEqual(
            "000000000000: $A.N='0000'; $P.N='000'; $P.KWO='000'; $Q.DI='00'; || " +
            "000100300000: $A.N=1; $P.N=3; $P.KWO='000'; $Q.DI='00';",
            str(_)
        )

    def test_calc_primary_key(self):
        """Метод calc_primary_key"""
        _ = VSPTDTechProcTable()
        trp_str = TrpStr(Trp('A', 'N', '0000'), Trp('P', 'N', '000'), Trp('P', 'KWO', '000'), Trp('Q', 'DI', '00'))
        self.assertEqual('000000000000', _.calc_primary_key(trp_str))
        trp_str = TrpStr(Trp('A', 'N', 1), Trp('P', 'N', 3), Trp('P', 'KWO', '000'), Trp('Q', 'DI', '00'))
        self.assertEqual('000100300000', _.calc_primary_key(trp_str))
