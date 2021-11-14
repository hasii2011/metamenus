
from wx import ITEM_CHECK
from wx import ITEM_NORMAL
from wx import ITEM_RADIO

from wx import NewId
from wx import GetTranslation

# TODO ask tacao if we can avoid using these
# noinspection PyProtectedMember
from wx._core import ItemKind

from metamenus.metamenus import _clean

from metamenus.metamenus import _sep
from metamenus.types import CustomMethods


class SItem:
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
