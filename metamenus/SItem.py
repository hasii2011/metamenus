
from logging import Logger
from logging import getLogger

from wx import ITEM_CHECK
from wx import ITEM_NORMAL
from wx import ITEM_RADIO

from wx import NewId
from wx import GetTranslation

# TODO ask tacao if we can avoid using these
# noinspection PyProtectedMember
from wx._core import ItemKind

from metamenus.metamenus import _clean

from metamenus.types import CustomMethods

from metamenus.Constants import _sep
from metamenus.Constants import META_MENUS_LOGGING_NAME


class SItem:
    """
    Internal use only. This provides a structure for parsing the 'trees'
    supplied in a sane way.
    """
    def __init__(self, params):

        self.logger: Logger = getLogger(META_MENUS_LOGGING_NAME)

        self._parent = None
        self._id: int = self._assignMenuId()
        self.params  = self._adjust(params)
        self.children = []

        self._label:        str = ''
        self._labelText:    str = ''
        self._tLabel:       str = ''
        self._tLabelText:   str = ''
        self._accelerator:  str = ''

        self.Update()

    def _adjust(self, params):
        """
        This is responsible for formatting the args and kwargs for items
        supplied within the 'tree'.
        TODO:  Lots of chicanery going on here with the same variable changing
        types and formats
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
        labelText:        "&New"
        tLabel:           "&Novo\tCtrl+N"     (full label translated)
        tLabelText:       "&Novo"             (label text translated)
        accelerator:      "Ctrl+N"

        Not actually using all of them right now, but maybe later
        """
        preLabel: str = self.params[0]

        self._label     = preLabel.strip()
        self._labelText = self._label.split("\t")[0].strip()

        label, acc = (self._label.split("\t") + [''])[:2]

        self.tLabel_text = GetTranslation(label.strip())
        self._accelerator = acc.strip()
        if self._accelerator is None or self._accelerator == '':
            self._tLabel = self.tLabel_text
        else:
            self._tLabel = "\t".join([self.tLabel_text, self._accelerator])

    def AddChild(self, Item):
        Item._parent = self
        self.children.append(Item)
        return Item

    def GetRealLabel(self, i18n):
        if i18n:
            label = self.GetLabelTranslation()
        else:
            label = self.GetLabel()
        return label

    def GetLabel(self):
        return self._label

    def GetLabelText(self):
        return self._labelText

    def GetLabelTranslation(self):
        return self._tLabel

    def GetLabelTextTranslation(self):
        return self.tLabel_text

    def GetAccelerator(self):
        return self._accelerator

    def GetId(self):
        return self._id

    def GetParams(self):
        return self.params

    def GetParent(self):
        return self._parent

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

    def _assignMenuId(self) -> int:

        parent: SItem = self._parent
        if parent is not None:
            labelText = parent._labelText
            self.logger.warning(f'{labelText}')

        return NewId()