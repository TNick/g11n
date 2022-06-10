import unittest
from typing import Dict, Any

from g11npy.base import G11nAbstract


class Implementation(G11nAbstract):
    def tr(self, key, params: Dict[str, Any] = None, lang: str = None):
        return 'something'


class TestBase(unittest.TestCase):
    def test_init(self):
        testee = Implementation('123', time_zone='456')
        self.assertEqual(testee.default_language, '123')
        self.assertEqual(testee.time_zone, '456')
