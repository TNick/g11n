"""
The application that uses this package can deposit in
`translator` variable the one instance of the `G11nAbstract` class
that it uses:

>>> import g11npy
>>> from g11npy.noop import G11nNoOp
>>> g11npy.translator = G11nNoOp()

A convenience `tr()` function is provided that makes use of the `translator`.
"""
from typing import Optional

from g11npy.base import G11nAbstract


translator: Optional[G11nAbstract] = None


def tr(key, lang: str = None, **kwargs):
    """
    A function that translates a key into a string in a specific language.

    If the lang parameter is None the implementation shall use the
    `translator.default_language` value.

    This is just a shortcut for `g11npy.translator.tr()`.
    """
    return translator.tr(key, lang, **kwargs)
