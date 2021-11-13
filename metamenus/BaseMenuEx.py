
from typing import Dict

from wx import Font
from wx import NullFont

# noinspection PyUnresolvedReferences
from wx.core import DEFAULT

from metamenus.Configuration import Configuration

from metamenus.types import CustomMethods


class BaseMenuEx:
    """
    A 'mixin' class to get some common attributes and behavior in a common place
    """
    def __init__(self,  *args, **kwargs):

        self._parent, self._menus = args    # TODO fix this with typing

        self._configuration: Configuration = Configuration()

    def _extractKeyWordValues(self, **kwargs) -> Dict:
        """
        Copy our custom keyword input values to our protected values or use the defaults

        Args:
            **kwargs:

        Returns:  The cleaned up dictionary of keyword arguments
        """

        self._margin:        int  = kwargs.pop("margin", DEFAULT)
        self._font:          Font = kwargs.pop("font", NullFont)
        self._show_title:    bool = kwargs.pop("show_title", True)
        self._customMethods: CustomMethods = kwargs.pop('customMethods', CustomMethods({}))
        self._i18n:          bool = kwargs.pop("i18n", True)

        return kwargs
