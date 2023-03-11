import sys
import unittest


def patched(lang: str):
    return {}


class TestDict(unittest.TestCase):
    def setUp(self):
        if 'g11npy.dict_based' in sys.modules:
            del sys.modules['g11npy.dict_based']
        if 'g11npy.hooks' in sys.modules:
            del sys.modules['g11npy.hooks']

    def test_init(self):
        from g11npy.dict_based import G11n
        testee = G11n({'a': {'b': '2'}}, '123', time_zone='456')
        self.assertDictEqual(testee.data, {'a': {'b': '2'}})
        self.assertEqual(testee.default_language, '123')
        self.assertEqual(testee.time_zone, '456')

    def test_load_language(self):
        from g11npy.dict_based import G11n
        from g11npy.hooks import g11n_hookimpl, g11n_pm
        testee = G11n(lang='ab')
        testee.load_language('bc')
        self.assertDictEqual(testee.data, {'bc': {}})

        class Something1:
            @g11n_hookimpl
            def load_language(self, lang: str):
                return {'a': '1', 'b': '2', 'e': lang}

        class Something2:
            @g11n_hookimpl
            def load_language(self, lang: str):
                return {'a': '10', 'b': '20', 'c': lang}

        g11n_pm.register(Something1())
        g11n_pm.register(Something2())

        testee.load_language('ef')
        self.assertDictEqual(
            testee.data, {
                'bc': {},
                'ef': {'a': '1', 'b': '2', 'c': 'ef', 'e': 'ef'}
            }
        )

    def test_tr(self):
        from g11npy.dict_based import G11n
        from g11npy.hooks import g11n_hookimpl, g11n_pm

        testee = G11n(lang='ab', data={'ab': {}})
        self.assertEqual(testee.tr('a'), 'a')
        self.assertEqual(testee.tr('a.b.c'), 'a.b.c')
        self.assertEqual(testee.tr('a.b.c', f=1), 'a.b.c')

        testee = G11n(lang='ab', data={'ab': {'a': '123'}})
        self.assertEqual(testee.tr('a'), '123')

        testee = G11n(lang='ab', data={'ab': {'a': {'b': '456'}}})
        self.assertEqual(testee.tr('a.b'), '456')
        self.assertEqual(testee.tr('a.b', lang='xy'), 'a.b')

    def test_complete(self):
        from g11npy.dict_based import G11n
        from g11npy.hooks import g11n_hookimpl, g11n_pm

        class Something1:
            @g11n_hookimpl
            def load_language(self, lang: str):
                return {
                    'a': '1',
                    'b': {
                        'o': '2',
                    },
                    'c': '3',
                }

        class Something2:
            @g11n_hookimpl
            def load_language(self, lang: str):
                return {
                    'a': '10',
                    'b': '20',
                    'c': '30',
                }

        g11n_pm.register(Something1())
        g11n_pm.register(Something2())
        testee = G11n(lang='ab')
        self.assertEqual(testee.tr('a'), '1')
        self.assertEqual(testee.tr('b.o'), '2')
