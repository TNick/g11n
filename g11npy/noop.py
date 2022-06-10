import json
from g11npy.base import G11nAbstract


class G11nNoOp(G11nAbstract):
    """
    The class implements the `tr()` method which simply stringifies the
    arguments.
    """
    def tr(self, key, lang=None, **kwargs):
        if not kwargs:
            return key
        else:
            return f'{key}({json.dumps(kwargs)})'
