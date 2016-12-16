# -*- coding: utf-8 -*-
from vsptd import *
import unittest


class TestTriplet(unittest.TestCase):
    def setUp(self):
        self.trp = Trp('A', 'B', 'C')

    # def test_init(self):
    #     with self.assertRaises(ValueError):
    #         _ = Triplet('S', 'G9')
        # TODO

    def test_str(self):
        self.assertEqual(str(self.trp),
                         "$A.B='C';")

    def test_add(self):
        self.assertIsInstance(self.trp + self.trp,
                              TrpStr)
        self.assertIsInstance(self.trp + self.trp + self.trp,
                              TrpStr)

    def test_equal(self):
        self.assertEqual(Trp('A', 'B', 'C'),
                         Trp('A', 'B', 'C'))
        self.assertNotEqual(self.trp,
                            {'prefix': 'A',
                             'name': 'B',
                             'value': 'C'}
                            )


class TestTriplexString(unittest.TestCase):
    def setUp(self):
        self.trpStr = Trp('A', 'B', 'C') + Trp('D', 'E', 'F')
        self.trpStr2 = Trp('J', 'K', 'L') + Trp('M', 'N', 'O')
        self.trp = Trp('G', 'H', 'I')

    # def test_init(self):
    #     pass

    def test_add(self):
        self.assertIsInstance(self.trpStr + self.trp, TrpStr)
        self.assertIsInstance(self.trp + self.trpStr, TrpStr)
        self.assertEqual(str(self.trpStr + self.trp), "$A.B='C';$D.E='F';$G.H='I';")
        self.assertEqual(str(self.trp + self.trpStr), "$G.H='I';$A.B='C';$D.E='F';")

        # проверка метода add
        self.assertNotEqual(self.trpStr + self.trp, self.trpStr.add(self.trp))
        self.assertNotEqual(self.trpStr + self.trpStr2, self.trpStr.add(self.trpStr2))

    def test_str(self):
        self.assertEqual(str(self.trpStr),
                         "$A.B='C';$D.E='F';")

    def test_equal(self):
        self.assertEqual(self.trpStr + self.trp, self.trp + self.trpStr)
        self.assertNotEqual(self.trpStr,
                            TrpStr(Trp('Z', 'X', 'Y'), Trp('Q', 'R', 'S'))
                            )

    # TODO


class TestParseTrpStr(unittest.TestCase):
    def test_parse_trp_str(self):
        self.assertEqual(parse_trp_str("$A.B='C';$D.E='F';$G.H='I';"),
                         TrpStr(Trp('A', 'B', 'C'), Trp('D', 'E', 'F'), Trp('G', 'H', 'I')))

if __name__ == '__main__':
    unittest.main()
