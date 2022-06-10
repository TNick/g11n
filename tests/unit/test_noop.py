import unittest

from g11n.noop import G11nNoOp


class TestNoOp(unittest.TestCase):
    def test_tr(self):
        testee = G11nNoOp('123', time_zone='456')
        self.assertEqual(testee.tr('a'), 'a')
        self.assertEqual(testee.tr('a.b'), 'a.b')
        self.assertEqual(testee.tr('a.b', k=1), 'a.b({"k": 1})')
        self.assertEqual(testee.tr('a.b', k=1, l=2, m=3), 'a.b({"k": 1, "l": 2, "m": 3})')
