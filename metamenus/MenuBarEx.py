
from wx import EVT_MENU
from wx import NullFont

from wx import Menu
from wx import MenuBar

from wx import PostEvent

# noinspection PyUnresolvedReferences
from wx.core import DEFAULT

# TODO ask tacao if we can avoid using these
# noinspection PyProtectedMember
from wx._core import wxAssertionError

from metamenus import MenuExAfterEvent
from metamenus import MenuExBeforeEvent
from metamenus.metamenus import _clean
from metamenus.metamenus import _makeMenus
from metamenus.metamenus import _sItem
from metamenus.metamenus import _verbose
from metamenus.metamenus import _evolve
from metamenus.metamenus import _prefixMB


class MenuBarEx(MenuBar):
    """
    MenuBarEx Main stuff
    """
    def __init__(self, *args, **kwargs):
        # noinspection SpellCheckingInspection
        """
        MenuBarEx(parent, menus, margin=wx.DEFAULT, font=wx.NullFont,custfunc={}, i18n=True, style=0)
        """

        # Initializing...
        self.parent, menus = args
        margin = kwargs.pop("margin", DEFAULT)
        font = kwargs.pop("font", NullFont)
        # noinspection SpellCheckingInspection
        custfunc = kwargs.pop("custfunc", {})
        i18n = self.i18n = kwargs.pop("i18n", True)

        MenuBar.__init__(self, **kwargs)

        # A reference to all of the sItems involved.
        tops = []

        # 'fix' for https://github.com/wxWidgets/Phoenix/issues/1648
        self.x = []

        # For each menu...
        for a in menus:
            # Parse the menu 'tree' supplied.
            top = _evolve(a)

            # Create these menus first...
            wxMenus = {top: Menu()}
            for k in top.GetChildWithChildren():
                wxMenus[k] = Menu()

                # ...and append their respective children.
                for h in k.GetChildren():
                    wxMenus = _makeMenus(wxMenus, h, k, margin, font, i18n)

            # Now append these items to the top level menu.
            for h in top.GetChildren():
                wxMenus = _makeMenus(wxMenus, h, top, margin, font, i18n)

            # Now append the top menu to the menu bar.
            self.Append(wxMenus[top], top.GetRealLabel(i18n))

            # Store a reference of this sItem.
            tops.append(top)

            # 'fix' for https://github.com/wxWidgets/Phoenix/issues/1648
            self.x.append(wxMenus)

        # Now find out what are the methods that should be called upon
        # menu items selection.
        MBIds = {}
        self.MBStrings = {}
        for top in tops:
            for child in top.GetChildren(True):
                child.SetMethod(_prefixMB, custfunc)
                MBIds[child.GetId()] = child
                self.MBStrings.update(child.GetAllMethods())

        # It won't hurt if we get rid of a None key, if any.
        # noinspection PyUnusedLocal
        bogus = self.MBStrings.pop(None, None)

        # We store the position of top-level menus rather than ids because
        # wx.Menu.EnableTop uses positions...
        for i, top in enumerate(tops):
            self.MBStrings[_clean(top.GetLabelText())] = i
            MBIds[i] = top

        # Nice class. 8^) Will take care of this automatically.
        self.parent.SetMenuBar(self)
        self.parent.Bind(EVT_MENU, self.OnMB_)

        # Now do something about the IDs and accelerators...
        self.MBIds = MBIds

    def OnMB_(self, evt):
        """
        Called on all menu events for this menu. It will in turn call
        the related method on parent, if any.
        """

        try:
            attr = self.MBIds[evt.GetId()]

            self.OnMB_before()

            if isinstance(attr, _sItem):
                attr_name = attr.GetMethod()

                if callable(attr_name):
                    attr_name()
                elif hasattr(self.parent, attr_name) and callable(getattr(self.parent, attr_name)):
                    getattr(self.parent, attr_name)()
                else:
                    if _verbose:
                        print("%s not found in parent." % attr_name)
            # TODO fix this
            # noinspection PyUnboundLocalVariable
            self.OnMB_after(attr_name)

        except KeyError:
            # Maybe another menu was triggered elsewhere in parent.
            pass

    def OnMB_before(self):
        # noinspection SpellCheckingInspection
        """
        If you need to execute something right before a menu event is
        triggered, you can bind the EVT_BEFOREMENU.
        """

        evt = MenuExBeforeEvent(-1, obj=self)
        PostEvent(self, evt)

    def OnMB_after(self, attr_name=None):
        # noinspection SpellCheckingInspection
        """
        If you need to execute something right after a menu event is
        triggered, you can bind the EVT_AFTERMENU.
        """

        evt = MenuExAfterEvent(-1, obj=self, item=attr_name)
        PostEvent(self, evt)

    def UpdateMenus(self):
        """
        Call this to update menu labels whenever the current locale
        changes.
        """

        if not self.i18n:
            return

        for k, v in self.MBIds.items():
            # Update top-level menus
            if not v.GetParent():
                v.Update()
                self.SetMenuLabel(k, v.GetRealLabel(self.i18n))
            # Update other menu items
            else:
                item = self.FindItemById(k)
                if item is not None:   # Skip separators
                    v.Update()
                    self.SetLabel(k, v.GetRealLabel(self.i18n))

    def GetItemState(self, menu_string):
        """Returns True if a checkable menu item is checked."""

        this = self.MBStrings[menu_string]
        try:
            r = self.IsChecked(this)
        except wxAssertionError:
            r = False
        return r

    def SetItemState(self, menu_string, check=True):
        """Toggles a checkable menu item checked or unchecked."""

        this = self.MBStrings[menu_string]
        self.Check(this, check)

    def EnableItem(self, menu_string, enable=True):
        """Enables or disables a menu item via its label."""

        this = self.MBStrings[menu_string]
        self.Enable(this, enable)

    def EnableItems(self, menu_string_list, enable=True):
        """Enables or disables menu items via a list of labels."""

        for menu_string in menu_string_list:
            self.EnableItem(menu_string, enable)

    def EnableTopMenu(self, menu_string, enable=True):
        """Enables or disables a top level menu via its label."""

        this = self.MBStrings[menu_string]
        self.EnableTop(this, enable)

    def EnableTopMenus(self, menu_string_list, enable=True):
        """Enables or disables top level menus via a list of labels."""

        for menu_string in menu_string_list:
            self.EnableTopMenu(menu_string, enable)
