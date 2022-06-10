from typing import Dict, Any

from g11npy.base import G11nAbstract
from g11npy.hooks import g11n_pm


class G11n(G11nAbstract):
    """
    Internationalization and localization provider.

    Internationalization
    --------------------

    The class relies on other libraries to provide the translated strings
    in a "key:value" fashion. It starts with an empty repository by default (the
    `data` attribute) which is later populated by the calls to `load_language()`.

    In `data` each key represents a language and each value is a complete
    set of strings for current application.

    The string set for a language can be nested as `tr()` implementation
    will split `a.b.c` strings into components and will use them to
    access the nested value in `"a": {"b": {"c": "value"}}`.
    """
    data: Dict[str, Dict[str, Any]]

    def __init__(self, data: Dict[str, Dict[str, Any]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data if data else {}

    def load_language(self, lang: str):
        """
        Asks all the plugins for data about a language and stores the result.
        """
        result = {}
        for partial in g11n_pm.hook.load_language(lang=lang):
            result.update(partial)
        self.data[lang] = result
        return result

    def tr(self, key, lang: str = None, **kwargs):
        # Make sure we have a language.
        if not lang:
            lang = self.default_language

        # Attempt to retrieve the string set for this language.
        data = self.data.get(lang, None)
        if data is None:
            # If not found load the language.
            data = self.load_language(lang)

        # Separate the chain into components.
        parts = key.split('.')

        # Locate this key in data.
        try:
            for part in parts:
                data = data[part]
        except (KeyError, TypeError):
            # We have no such key in our repository.
            return key

        # Format resulted string.
        if kwargs:
            return data.format(**kwargs)

        return data
