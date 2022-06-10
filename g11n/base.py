import abc
import datetime
from typing import Dict, Any, Union


class G11nAbstract(abc.ABC):
    """
    A class that handles translations.

    Internationalization
    --------------------

    The class stores a default language that is used when the user calls the `tr` method
    without a language parameter.

    Localization
    ------------

    The time zone to use is simply stored inside.
    """
    default_language: str
    time_zone: Union[datetime.tzinfo, str]

    def __init__(self, lang: str = 'en', time_zone: Union[datetime.tzinfo, str] = 'UTC'):
        self.default_language = lang
        self.time_zone = time_zone

    @abc.abstractmethod
    def tr(self, key, lang: str = None, **kwargs):
        """
        A method that translates a key into a string in a specific language.

        If the lang parameter is None the implementation shall use the
        `self.default_language` value.
        """
        pass
