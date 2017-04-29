# -*- coding: utf-8 -*-
import unittest

from vsptd.vsptd import Trp, TrpStr
from vsptd.parse import *


class TestVSPTDParse(unittest.TestCase):
    """Класс VSPTDParse"""
    def test_params(self):
        regexps = VSPTDParse()
        self.assertEqual(r'(\w+)\.(\w+)', regexps.re_trp_ref_special)
        self.assertEqual(r'\$(\w+)\.(\w+)', regexps.re_trp_ref)
        self.assertEqual(r'(\w+)\.(\w+)\=(.*?)\;', regexps.re_trp_special)
        self.assertEqual(r'\$(\w+)\.(\w+)??\=(.*?)(?:\"(.*?)\")??\;', regexps.re_trp)


class TestParseTrpStr(unittest.TestCase):
    """Разбор триплетных строк различного вида"""
    def test_parse(self):
        """Парсинг различного вида комбинаций"""
        # различные виды триплетов
        self.assertEqual(parse_trp_str("$P.N='V';"), TrpStr(Trp('P', 'N', 'V')))
        self.assertEqual(parse_trp_str("$P.N='V'\"C\";"), TrpStr(Trp('P', 'N', 'V', 'C')))
        self.assertEqual(parse_trp_str("$P.N=:;"), TrpStr(Trp('P', 'N', bid=True)))
        self.assertEqual(parse_trp_str("$P.N=:'V';"), TrpStr(Trp('P', 'N', 'V', bid=True)))
        self.assertEqual(parse_trp_str("$P.=:;"), TrpStr(Trp('P', bid=True)))
        # экзотические
        self.assertEqual(parse_trp_str("$P.=:'V';"), TrpStr(Trp('P', None, 'V', bid=True)))
        self.assertEqual(parse_trp_str("$P.=:'V'\"C\";"), TrpStr(Trp('P', None, 'V', 'C', bid=True)))

        # различные комбинации
        self.assertEqual(parse_trp_str("$A.B='C';$D.E='F';$G.H='I';"),
                         TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('G', 'H', 'I')))
        self.assertEqual(parse_trp_str("$A.B='C';$D.E='F';$G.H='I';$P.N='V';"),
                         TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('G', 'H', 'I'), Trp('P', 'N', 'V')))
        self.assertEqual(
            parse_trp_str("$A.B='C';$P.N='V'\"C\";$D.E='F';$P.=:;$G.H='I';"),
            TrpStr(Trp('A', 'B', 'C'), Trp('P', 'N', 'V', 'C'), Trp('D', 'E', 'F'), Trp('P', bid=True), Trp('G', 'H', 'I'))
        )

    def test_trps_separator(self):
        """Нечувствительность к разделителю между триплетами"""
        self.assertEqual(parse_trp_str("$A.B='C';$D.E='F';$G.H='I';"), parse_trp_str("$A.B='C'; $D.E='F'; $G.H='I';"))

    def test_different_types_of_trp_value(self):
        """Различные виды значения триплета"""
        self.assertEqual(parse_trp_str("$P.N='V';"), TrpStr(Trp('P', 'N', 'V')))
        self.assertEqual(parse_trp_str("$P.N=1;"), TrpStr(Trp('P', 'N', 1)))
        self.assertEqual(parse_trp_str("$P.N=1.25;"), TrpStr(Trp('P', 'N', 1.25)))
        self.assertEqual(parse_trp_str("$P.N=.25;"), TrpStr(Trp('P', 'N', 0.25)))
        self.assertEqual(parse_trp_str("$P.N=10E-5;"), TrpStr(Trp('P', 'N', 10E-5)))
        self.assertEqual(parse_trp_str("$P.N=$A.B;"), TrpStr(Trp('P', 'N', Trp('A', 'B'))))  # триплет-ссылка

