
from wx import ART_MENU
from wx import ITEM_CHECK
from wx import ITEM_NORMAL
from wx import ITEM_RADIO

from wx import ArtProvider
from wx import GetTranslation
from wx import MenuItem
from wx import NullBitmap
from wx import NullFont
from wx import Platform

# TODO ask tacao if we can avoid using these
# noinspection PyProtectedMember
from wx._core import ItemKind

from wx import NewId

# noinspection PyUnresolvedReferences
from wx.core import DEFAULT

from metamenus import use_unidecode

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

# More info on 'history' and 'README.md' files.

# Constants --------------------------------------------------------------------

# # If you rather use a different indentation level for menus,
# # change _ind here.
# _ind = 2 * " "

# _sep is used internally only and is a substring that _cannot_
# appear on any of the regular menu labels.
from metamenus.Configuration import Configuration
from metamenus.types import CustomMethods

_sep = " @@@ "

# If you want to use different prefixes for methods called by this
# menu bar/menu, change them here.
# _prefixMB = "OnMB_"
_prefixM  = "OnM_"

# If you want to print messages warning about methods not
# found on parent, change this to True.
_verbose = True


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
        # noinspection SpellCheckingInspection
        """
        Members created/updated here:

        label:            "&New\tCtrl+N"
        label_text:       "&New"
        tlabel:           "&Novo\tCtrl+N"     (full label translated)
        tlabel_text:      "&Novo"             (label text translated)
        acc:              "Ctrl+N"

        I am not actually using all of them right now, but maybe I will...
        """
        self.label = self.params[0].strip()
        self.label_text = self.label.split("\t")[0].strip()
        label, acc = (self.label.split("\t") + [''])[:2]
        self.tLabel_text = GetTranslation(label.strip())
        self.acc = acc.strip()
        if self.acc:
            self.tLabel = "\t".join([self.tLabel_text, self.acc])
        else:
            self.tLabel = self.tLabel_text

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
        return self.tLabel

    def GetLabelTextTranslation(self):
        return self.tLabel_text

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
    def SetMethod(self, prefix: str, customMethods: CustomMethods):

        menuName = _clean(self.GetPath())

        # noinspection SpellCheckingInspection
        method_custom = customMethods.get(menuName)
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
        level  = params[0].count(Configuration().indentation) - 1

        if level > il:
            il += 1
            # Todo fix this !!
            # noinspection PyUnboundLocalVariable
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
        so = "?????????????????????????????????????????????????"
        # noinspection SpellCheckingInspection
        sd = "aaaaaeeeeiiiiooooouuuucyyAAAAAEEEEIIIIOOOOOUUUUCY"

        for i, char in enumerate(so):
            if char in s:
                s = s.replace(char, sd[i])
        s = "".join([x for x in s if x.isalnum()])
        
    return s
    

def _makeMenus(wxMenus, h, k, margin, font, i18n):
    """Internal use only. Creates menu items."""

    label = h.GetRealLabel(i18n)
    Id = h.GetId()
    args, kwargs = h.GetParams()[1:]

    if h.HasChildren():
        args = (wxMenus[h], Id, label) + args
        item = MenuItem(*args, **{"subMenu": wxMenus[h]})
        item = _process_kwargs(item, kwargs, margin, font)

        wxMenus[k].Append(item)

    else:
        if label == "-":
            wxMenus[k].AppendSeparator()

        elif label == "/":
            wxMenus[k].Break()

        else:
            args = (wxMenus[k], Id, label) + args
            item = MenuItem(*args)
            item = _process_kwargs(item, kwargs, margin, font)
            wxMenus[k].Append(item)

    return wxMenus


class _mmPrep:
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

        print(f'Parsing {filename}.py...')

        exec(f'import {filename}')
        mod = eval(filename)

        listObjects = []
        for obj in dir(mod):
            if type(getattr(mod, obj)) == list:
                listObjects.append(obj)

        all_lines = []
        for obj in listObjects:
            gError = False
            header = ["\n# Strings for '%s':\n" % obj]
            err, lines = self.parseMenu(mod, obj)
            if not err:
                print(f"OK: parsed '{obj}'")
                all_lines += header + lines
            else:
                err, lines = self.parseMenuBar(mod, obj)
                if not err:
                    print(f"OK: parsed '{obj}'")
                    all_lines += header + lines
                else:
                    gError = True
            if gError:
                print(f"Warning: could not parse '{obj}'")

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
