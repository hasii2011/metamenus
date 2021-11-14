
from typing import Dict

from wx import ART_MENU
from wx import ArtProvider

from wx import Platform
# noinspection PyUnresolvedReferences
from wx.core import DEFAULT

from wx import Font
from wx import MenuItem
from wx import NullBitmap
from wx import NullFont

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

    def _makeMenus(self, wxMenus, h, k, margin, font, i18n):
        """
        Internal use only. Creates menu items.
        """

        label = h.GetRealLabel(i18n)
        Id = h.GetId()
        args, kwargs = h.GetParams()[1:]

        if h.HasChildren():
            args = (wxMenus[h], Id, label) + args
            item = MenuItem(*args, **{"subMenu": wxMenus[h]})
            item = self._process_kwargs(item, kwargs, margin, font)

            wxMenus[k].Append(item)

        else:
            if label == "-":
                wxMenus[k].AppendSeparator()

            elif label == "/":
                wxMenus[k].Break()

            else:
                args = (wxMenus[k], Id, label) + args
                item = MenuItem(*args)
                item = self._process_kwargs(item, kwargs, margin, font)
                wxMenus[k].Append(item)

        return wxMenus

    def _process_kwargs(self, item, kwargs, margin, font):
        """
        Internal use only. This is responsible for setting bitmap(s), font, margin
        and colour for menu items.
        """

        # "bmpChecked" and "bmp" are aliases; they can be both bitmaps or
        # bitmap-callable objects.
        if "bmpChecked" in kwargs or "bmp" in kwargs:
            if "bmpChecked" in kwargs:
                checked = kwargs["bmpChecked"]
            else:
                # but "bmp" may also be a string to evoke ArtProvider Ids
                checked = kwargs["bmp"]
                if type(checked) == str:
                    try:
                        import wx  # The eval depends on this import;  Ugh
                        ArtID = eval("wx.ART_" + checked.upper())
                        # checked = wx.ArtProvider.GetBitmap(ArtID, wx.ART_MENU)
                        checked = ArtProvider.GetBitmap(ArtID, ART_MENU)
                    # cannot resolve; let's try one more thing.
                    # https://wxpython.org/Phoenix/docs/html/stock_items.html
                    except AttributeError:
                        # noinspection SpellCheckingInspection
                        if Platform == '__WXGTK__':
                            checked = ArtProvider.GetBitmap("gtk-" + checked, ART_MENU)
                            if not checked.IsOk():
                                checked = NullBitmap  # ok, give up.
                        else:
                            checked = NullBitmap

            unchecked = kwargs.get("bmpUnchecked", NullBitmap)

            # call if callable
            if callable(checked):
                checked = checked()
            if callable(unchecked):
                unchecked = unchecked()

            item.SetBitmaps(checked, unchecked)

        # these should work under MSW
        kwlist = [("font",     "SetFont"),
                  ("margin",   "SetMarginWidth"),
                  ("fgColour", "SetTextColour"),
                  ("bgColour", "SetBackgroundColour")]

        for kw, m in kwlist:
            if kw in kwargs:
                getattr(item, m)(kwargs[kw])

        if margin != DEFAULT:
            item.SetMarginWidth(margin)

        if font != NullFont:
            item.SetFont(font)

        return item
