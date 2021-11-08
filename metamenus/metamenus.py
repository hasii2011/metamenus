#!/usr/bin/env python3

from wx import ART_MENU
from wx import EVT_MENU
from wx import ITEM_CHECK
from wx import ITEM_NORMAL
from wx import ITEM_RADIO

from wx import ArtProvider
from wx import GetTranslation
from wx import Menu
from wx import MenuBar
from wx import MenuItem
from wx import NullBitmap
from wx import NullFont
from wx import Platform
from wx import PostEvent

# TODO ask tacao if we can avoid using these
# noinspection PyProtectedMember
from wx._core import ItemKind
# noinspection PyProtectedMember
from wx._core import wxAssertionError

from wx import NewId

# noinspection PyUnresolvedReferences
from wx.core import DEFAULT

from metamenus import use_unidecode
from metamenus import MenuExBeforeEvent
from metamenus import MenuExAfterEvent

# from wx.lib.newevent import NewCommandEvent

# -*- coding: utf-8 -*-

#
# metamenus vs. 0.13 (15/09/2020)
#
# Written by E. A. Tacao <mailto@tacao.com.br>, (C) 2005... 2020
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     (1) Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#     (2) Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#
#     (3)The name of the author may not be used to
#     endorse or promote products derived from this software without
#     specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

__author__  = "E. A. Tacao <mailto |at| tacao.com.br>"
__date__    = "15 Sep 2020, 19:27 GMT-03:00"
__version__ = "0.13"

# More info on 'history' and 'README.md' files.

# -------------------------------------------------------------------------------
        

# try:
#     # noinspection PyUnresolvedReferences
#     import unidecode
#     use_unidecode = True
# except ModuleNotFoundError:
#     use_unidecode = False
#
# # Events -----------------------------------------------------------------------
#
# (MenuExBeforeEvent, EVT_BEFOREMENU) = NewCommandEvent()
# (MenuExAfterEvent,  EVT_AFTERMENU) = NewCommandEvent()

# Constants --------------------------------------------------------------------

# If you rather use a different indentation level for menus,
# change _ind here.
_ind = 2 * " "

# _sep is used internally only and is a substring that _cannot_
# appear on any of the regular menu labels.
_sep = " @@@ "

# If you want to use different prefixes for methods called by this
# menu bar/menu, change them here.
_prefixMB = "OnMB_"
_prefixM  = "OnM_"

# If you want to print messages warning about methods not
# found on parent, change this to True.
_verbose = False


class _sItem:
    """
    Internal use only. This provides a structure for parsing the 'trees'
    supplied in a sane way.
    """

    def __init__(self, params):
        self.parent = None
        self.Id = NewId()
        self.params = self._adjust(params)
        self.children = []

        self.Update()

    def _adjust(self, params):
        """
        This is responsible for formatting the args and kwargs for items
        supplied within the 'tree'.
        """

        args = ()
        kwargs = {}
        params = params + [None] * (3 - len(params))

        if type(params[1]) == tuple:
            args = params[1]
        elif type(params[1]) in [str, int, ItemKind]:
            args = (params[1],)
        elif type(params[1]) == dict:
            kwargs = params[1]

        if type(params[2]) == tuple:
            args = params[2]
        elif type(params[2]) in [str, int, ItemKind]:
            args = (params[2],)
        elif type(params[2]) == dict:
            kwargs = params[2]

        args = list(args) + [""] * (2 - len(args))

        # For those who believe wx.UPPERCASE_STUFF_IS_UGLY... 8^)
        kind_conv = {"radio":  ITEM_RADIO,
                     "check":  ITEM_CHECK,
                     "normal": ITEM_NORMAL}
        # ...well, these strings look more compact.

        if args[0] in list(kind_conv.keys()) + list(kind_conv.values()):
            args = (args[1], args[0])

        kind_conv.update({"normal": None, "": None})

        if type(args[1]) in [str]:
            kind = kind_conv.get(args[1])
            if kind is not None:
                args = (args[0], kind)
            else:
                args = (args[0],)

        return params[0], tuple(args), kwargs

    def Update(self):
        # Members created/updated here:
        #
        # label:            "&New\tCtrl+N"
        # label_text:       "&New"
        # tlabel:           "&Novo\tCtrl+N"     (full label translated)
        # tlabel_text:      "&Novo"             (label text translated)
        # acc:              "Ctrl+N"
        #
        # I'm not actually using all of them right now, but maybe I will...

        self.label = self.params[0].strip()
        self.label_text = self.label.split("\t")[0].strip()
        label, acc = (self.label.split("\t") + [''])[:2]
        self.tlabel_text = GetTranslation(label.strip())
        self.acc = acc.strip()
        if self.acc:
            self.tlabel = "\t".join([self.tlabel_text, self.acc])
        else:
            self.tlabel = self.tlabel_text

    def AddChild(self, Item):
        Item.parent = self
        self.children.append(Item)
        return Item

    def GetRealLabel(self, i18n):
        if i18n:
            label = self.GetLabelTranslation()
        else:
            label = self.GetLabel()
        return label

    def GetLabel(self):
        return self.label

    def GetLabelText(self):
        return self.label_text

    def GetLabelTranslation(self):
        return self.tlabel

    def GetLabelTextTranslation(self):
        return self.tlabel_text

    def GetAccelerator(self):
        return self.acc

    def GetId(self):
        return self.Id

    def GetParams(self):
        return self.params

    def GetParent(self):
        return self.parent

    def GetChildren(self, recursive=False):
        def _walk(Item, r):
            for child in Item.GetChildren():
                r.append(child)
                if child.HasChildren():
                    _walk(child, r)
            return r

        if not recursive:
            return self.children
        else:
            return _walk(self, [])

    def HasChildren(self):
        return bool(self.children)

    def GetChildWithChildren(self):
        def _walk(Item, r):
            for child in Item.GetChildren():
                if child.HasChildren():
                    r.insert(0, child)
                    _walk(child, r)
            return r

        return _walk(self, [])

    def GetChildWithId(self, Id):
        r = None
        for child in self.GetChildren(True):
            if child.GetId() == Id:
                r = child
                break
        return r

    def GetPath(self):
        this = self
        path = this.GetLabelText()

        while this.GetParent() is not None:
            this = this.GetParent()
            path = "%s %s %s" % (this.GetLabelText(), _sep, path)

        return path

    # noinspection SpellCheckingInspection
    def SetMethod(self, prefix, custfunc):
        menuName = _clean(self.GetPath())

        # noinspection SpellCheckingInspection
        method_custom = custfunc.get(menuName)
        method_default = prefix + menuName

        # noinspection SpellCheckingInspection
        # If a custfunc was passed here, use it; otherwise we'll use a
        # default method name when this menu item is selected.
        self.method = method_custom or method_default

        # We also store a reference to all method names that the public
        # methods can address.
        self.all_methods = {method_custom: self.GetId(),
                            method_default: self.GetId(),
                            menuName: self.GetId()}

    def GetMethod(self):
        return self.method

    def GetAllMethods(self):
        return self.all_methods


def _process_kwargs(item, kwargs, margin, font):
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


def _evolve(a):
    """Internal use only. This will parse the menu 'tree' supplied."""

    top = _sItem(a[0])
    il = 0
    cur = {il: top}

    for i in range(1, len(a)):
        params = a[i]
        level  = params[0].count(_ind) - 1

        if level > il:
            il += 1
            cur[il] = new_sItem
        elif level < il:
            il = level

        new_sItem = cur[il].AddChild(_sItem(params))

    return top


def _clean(s):
    """
    Internal use only. Tries to remove all accentuated chars from a string.
    """
    
    if use_unidecode:
        # noinspection PyUnresolvedReferences
        s = unidecode.unidecode("".join([x for x in s if x.isalnum()]))

    else:
        # noinspection SpellCheckingInspection
        so = "áàãâäéèêëíìîïóòõôöúùûüçýÿÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇÝ"
        # noinspection SpellCheckingInspection
        sd = "aaaaaeeeeiiiiooooouuuucyyAAAAAEEEEIIIIOOOOOUUUUCY"

        for i, char in enumerate(so):
            if char in s:
                s = s.replace(char, sd[i])
        s = "".join([x for x in s if x.isalnum()])
        
    return s
    

def _makeMenus(wxmenus, h, k, margin, font, i18n):
    """Internal use only. Creates menu items."""

    label = h.GetRealLabel(i18n)
    Id = h.GetId()
    args, kwargs = h.GetParams()[1:]

    if h.HasChildren():
        args = (wxmenus[h], Id, label) + args
        item = MenuItem(*args, **{"subMenu": wxmenus[h]})
        item = _process_kwargs(item, kwargs, margin, font)

        wxmenus[k].Append(item)

    else:
        if label == "-":
            wxmenus[k].AppendSeparator()

        elif label == "/":
            wxmenus[k].Break()

        else:
            args = (wxmenus[k], Id, label) + args
            item = MenuItem(*args)
            item = _process_kwargs(item, kwargs, margin, font)
            wxmenus[k].Append(item)

    return wxmenus


class _mmprep:
    """
    Generates a temporary file that can be read by gettext utilities in
    order to create a .po file with strings to be translated. This class is
    called when you run metamenus from the command line.

    Usage:
     1. Make sure your menus are in a separate file and that the separate
        file in question contain only your menus;

     2. From a command line, type:
          metamenus.py separate_file output_file

        where 'separate_file' is the python file containing the menu
        'trees', and 'output_file' is the python-like file generated that
        can be parsed by gettext utilities.

    To get a .po file containing the translatable strings, put the
    'output_file' in the app.fil list of translatable files and run the
    mki18n.py script. For more info please see
    <http://wiki.wxpython.org/index.cgi/Internationalization>.
    """

    def __init__(self, filename, output_file):
        """Constructor."""

        print("Parsing %s.py..." % filename)

        exec("import %s" % filename)
        mod = eval(filename)

        objs = []
        for obj in dir(mod):
            if type(getattr(mod, obj)) == list:
                objs.append(obj)

        all_lines = []
        for obj in objs:
            gerr = False
            header = ["\n# Strings for '%s':\n" % obj]
            err, lines = self.parseMenu(mod, obj)
            if not err:
                print("OK: parsed '%s'" % obj)
                all_lines += header + lines
            else:
                err, lines = self.parseMenuBar(mod, obj)
                if not err:
                    print("OK: parsed '%s'" % obj)
                    all_lines += header + lines
                else:
                    gerr = True
            if gerr:
                print("Warning: couldn't parse '%s'" % obj)

        try:
            # f = file("%s.py" % output_file, "w")
            # f.writelines(all_lines)
            # f.close()

            with open("%s.py" % output_file, "w") as f:
                f.writelines(all_lines)

            print("File %s.py successfully written." % output_file)

        except (ValueError, Exception) as e:
            print("ERROR: File %s.py was NOT written." % output_file)
            print(f'{e}')
            raise

    def form(self, lines):
        """Removes separators and breaks and adds gettext stuff."""

        new_lines = []
        for line in lines:
            if line not in ["-", "/"]:
                new_lines.append("_(" + repr(line) + ")\n")
        return new_lines

    def parseMenuBar(self, mod, obj):
        """Tries to parse a MenuBarEx object."""

        err = False
        lines = []
        try:
            for menu in getattr(mod, obj):
                top = _evolve(menu)
                lines.append(top.GetLabelText())
                for child in top.GetChildren(True):
                    lines.append(child.GetLabelText())
        except(ValueError, Exception) as e:
            print(f'{e}')
            err = True

        return err, self.form(lines)

    def parseMenu(self, mod, obj):
        """Tries to parse a MenuEx object."""

        err = False
        lines = []
        try:
            top = _evolve(getattr(mod, obj))
            lines.append(top.GetLabelText())
            for child in top.GetChildren(True):
                lines.append(child.GetLabelText())
        except (ValueError, Exception) as e:
            print(f'{e}')
            err = True

        return err, self.form(lines)


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
            wxmenus = {top: Menu()}
            for k in top.GetChildWithChildren():
                wxmenus[k] = Menu()

                # ...and append their respective children.
                for h in k.GetChildren():
                    wxmenus = _makeMenus(wxmenus, h, k, margin, font, i18n)

            # Now append these items to the top level menu.
            for h in top.GetChildren():
                wxmenus = _makeMenus(wxmenus, h, top, margin, font, i18n)

            # Now append the top menu to the menu bar.
            self.Append(wxmenus[top], top.GetRealLabel(i18n))

            # Store a reference of this sItem.
            tops.append(top)

            # 'fix' for https://github.com/wxWidgets/Phoenix/issues/1648
            self.x.append(wxmenus)

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

            self.OnMB_after(attr_name)

        except KeyError:
            # Maybe another menu was triggered elsewhere in parent.
            pass

    def OnMB_before(self):
        """
        If you need to execute something right before a menu event is
        triggered, you can bind the EVT_BEFOREMENU.
        """

        evt = MenuExBeforeEvent(-1, obj=self)
        PostEvent(self, evt)

    def OnMB_after(self, attr_name=None):
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


class MenuEx(Menu):
    """
    MenuEx Main stuff
    """
    def __init__(self, *args, **kwargs):
        # noinspection SpellCheckingInspection
        """
        MenuEx(parent, menu, margin=wx.DEFAULT, font=wx.NullFont, show_title=True, custfunc={}, i18n=True, style=0)
        """

        # Initializing...
        self.parent, menu = args
        margin = kwargs.pop("margin", DEFAULT)
        font = kwargs.pop("font", NullFont)
        show_title = kwargs.pop("show_title", True)
        # noinspection SpellCheckingInspection
        custfunc = kwargs.pop("custfunc", {})
        i18n = self.i18n = kwargs.pop("i18n", True)

        Menu.__init__(self, **kwargs)

        self._title = menu[0][0]
        if show_title:
            if i18n:
                self.SetTitle(GetTranslation(self._title))
            else:
                self.SetTitle(self._title)

        # 'fix' for https://github.com/wxWidgets/Phoenix/issues/1648
        self.x = []

        # Parse the menu 'tree' supplied.
        top = _evolve(menu)

        # Create these menus first...
        wxmenus = {top: self}
        for k in top.GetChildWithChildren():
            wxmenus[k] = Menu()

            # ...and append their respective children.
            for h in k.GetChildren():
                wxmenus = _makeMenus(wxmenus, h, k, margin, font, i18n)

        # Now append these items to the top level menu.
        for h in top.GetChildren():
            wxmenus = _makeMenus(wxmenus, h, top, margin, font, i18n)

        # Now find out what are the methods that should be called upon
        # menu items selection.
        self.MenuIds = {}
        self.MenuStrings = {}
        self.MenuList = []
        for child in top.GetChildren(True):
            Id = child.GetId()
            item = self.FindItemById(Id)
            if item:
                child.SetMethod(_prefixM, custfunc)
                self.MenuIds[Id] = child
                self.MenuStrings.update(child.GetAllMethods())
                self.MenuList.append([Id, child.GetPath()])

        # 'fix' for https://github.com/wxWidgets/Phoenix/issues/1648
            self.x.append(wxmenus)

        # Initialize menu states.
        self.MenuState = {}
        for Id in self.MenuIds.keys():
            if self.FindItemById(Id).IsCheckable():
                is_checked = self.IsChecked(Id)
            else:
                is_checked = False
            self.MenuState[Id] = is_checked

        # Nice class. 8^) Will take care of this automatically.
        #
        # TODO: Used to work before Phoenix on TaskBarIcons,
        # now it seems we have to bind there instead... 8^(
        self.parent.Bind(EVT_MENU, self.OnM_)

    def _update(self, i):
        def _resetRadioGroup(i):
            g = []
            n = []

            for Id, s in self.MenuList:
                item = self.FindItemById(Id)
                if item.GetKind() == ITEM_RADIO:
                    g.append(Id)
                else:
                    g.append(None)

            for x in range(g.index(i), 0, -1):
                # if g[x] != None:
                if g[x] is not None:
                    n.append(g[x])
                else:
                    break

            for x in range(g.index(i) + 1, len(g)):
                # if g[x] != None:
                if g[x] is not None:
                    n.append(g[x])
                else:
                    break

            for i in n:
                self.MenuState[i] = False

        kind = self.FindItemById(i).GetKind()

        if kind == ITEM_CHECK:
            self.MenuState[i] = not self.IsChecked(i)

        elif kind == ITEM_RADIO:
            _resetRadioGroup(i)
            self.MenuState[i] = True

    def OnM_(self, evt):
        """
        Called on all menu events for this menu. It will in turn call
        the related method on parent, if any.
        """
        try:
            attr = self.MenuIds[evt.GetId()]

            self.OnM_before()

            if isinstance(attr, _sItem):
                attr_name = attr.GetMethod()

                if callable(attr_name):
                    attr_name()
                elif hasattr(self.parent, attr_name) and callable(getattr(self.parent, attr_name)):
                    getattr(self.parent, attr_name)()
                else:
                    if _verbose:
                        print("%s not found in parent." % attr_name)

            self.OnM_after(attr_name)

        except KeyError:
            # Maybe another menu was triggered elsewhere in parent,
            # maybe I screwed something up somewhere...
            pass

        evt.Skip()

    def OnM_before(self):
        """
        If you need to execute something right before a menu event is
        triggered, you can bind the EVT_BEFOREMENU.
        """

        evt = MenuExBeforeEvent(-1, obj=self)
        PostEvent(self, evt)

    def OnM_after(self, attr_name=None):
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

        This method never seems to be called from the demo programs.  Which
        is probably why `MenuIds` un-resolved does not matter;  Talk to
        tacao;  -- Humberto
        """

        if not self.i18n:
            return

        # noinspection PyUnresolvedReferences
        for k, v in MenuIds.items():
            item = self.FindItemById(k)
            if item is not None:   # Skip separators
                v.Update()
                self.SetLabel(k, v.GetRealLabel(self.i18n))

    def Popup(self, evt):
        """Pops this menu up."""

        [self.Check(i, v) for i, v in self.MenuState.items() \
         if self.FindItemById(i).IsCheckable()]

        obj = evt.GetEventObject()
        pos = evt.GetPosition()
        obj.PopupMenu(self, pos)

    def GetItemState(self, menu_string):
        """Returns True if a checkable menu item is checked."""

        this = self.MenuStrings[menu_string]
        try:
            r = self.IsChecked(this)
        except wxAssertionError:
            r = False
        return r

    def SetItemState(self, menu_string, check):
        """Toggles a checkable menu item checked or unchecked."""

        this = self.MenuStrings[menu_string]
        self.MenuState[this] = check

    def EnableItem(self, menu_string, enable=True):
        """Enables or disables a menu item via its label."""

        this = self.MenuStrings[menu_string]
        self.Enable(this, enable)

    def EnableItems(self, menu_string_list, enable=True):
        """Enables or disables menu items via a list of labels."""

        for menu_string in menu_string_list:
            self.EnableItem(menu_string, enable)

    def EnableAllItems(self, enable=True):
        """Enables or disables all menu items."""

        for Id in self.MenuIds.keys():
            self.Enable(Id, enable)


if __name__ == "__main__":
    import sys
    import os.path
    args = sys.argv[1:]
    if len(args) == 2:
        _mmprep(*[os.path.splitext(arg)[0] for arg in args])
    else:
        print("""
---------------------------------------------------------------------------
metamenus %s

%s
%s
Distributed under the BSD-3-Clause LICENSE.
---------------------------------------------------------------------------

Usage:
------

metamenus.py menu_file output_file

- 'menu_file' is the python file containing the menu 'trees';
- 'output_file' is the output file generated that can be parsed by the
  gettext utilities.

Please see metamenus.__doc__ (under the 'More about i18n' section) and
metamenus._mmprep.__doc__ for more details.
---------------------------------------------------------------------------
""" % (__version__, __author__, __date__))
