
from wx import ALIGN_CENTRE
from wx import ALL
from wx import BOTTOM
from wx import CHOICEDLG_STYLE
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EVT_RIGHT_UP
from wx import EVT_SIZE
from wx import EVT_TOGGLEBUTTON
from wx import EXPAND
from wx import ICON_INFORMATION
from wx import ID_ANY
from wx import ID_OK
from wx import LANGUAGE_DEFAULT
from wx import Locale
from wx import OK
from wx import TOP

from wx import Button
from wx import ToggleButton
from wx import Panel
from wx import Platform
from wx import SingleChoiceDialog
from wx import StaticLine
from wx import StaticText
from wx import MessageDialog
from wx import Icon
from wx import Frame
from wx import GridBagSizer

from wx import GetApp

from wx import version as wxVersion

from wx.adv import EVT_TASKBAR_LEFT_DOWN

from demo.DemoTaskBarIcon import DemoTaskBarIcon
from demo.Demo_context_menu import my_context_menu
from metamenus.Constants import THE_GREAT_MAC_PLATFORM

from demo.Demo_images import the_snake
from demo.Demo_menubar import DemonstrationMenuBar

from metamenus.MenuBarEx import MenuBarEx
from metamenus.MenuEx import MenuEx

from metamenus.types import CustomMethods
from metamenus.types import MenuName
from metamenus.types import MethodName


class DemoFrame(Frame):
    def __init__(self):
        Frame.__init__(self, None, ID_ANY, 'metamenus Demonstration')

        self._setupTaskBarIcons()

        # Not compulsory, but here we will test metamenus status messages
        self.CreateStatusBar()
        self.SetStatusText("Well here is the status bar")

        # noinspection SpellCheckingInspection
        """
            This creates and attaches the menu bar to this frame
            self.mb = MenuBarEx(self, my_menubar)
        """
        # noinspection SpellCheckingInspection
        """
        Shows how to use the  customMethods argument
        Instructs metamenus to use 
            'onSave' instead of 'OnMB_FileSave'
        and
            'onCloseAll' instead of 'OnMB_FileCloseAll'
        """
        customMethods: CustomMethods = CustomMethods({
            MenuName("FileSave"):     MethodName("onSave"),
            MenuName("FileCloseAll"): MethodName("onCloseAll")
        })
        self.mb = MenuBarEx(self, DemonstrationMenuBar, customMethods=customMethods)
        panel = Panel(self)

        sizer = GridBagSizer()

        self.text = "metamenus created your wx.MenuBar for this frame, " \
                    "so that now you can play around with its menus " \
                    "to see how they behave.\n\n" \
                    "metamenus also created a popup wx.Menu here. " \
                    "Right-click somewhere to test it."
        self.tc = StaticText(panel, ID_ANY, self.text)
        sizer.Add(self.tc, pos=(0, 0), span=(1, 4), flag=EXPAND | ALL, border=15)

        staticLine: StaticLine = StaticLine(panel)
        sizer.Add(staticLine, pos=(1, 0), span=(1, 4), flag=EXPAND | TOP | BOTTOM, border=15)

        b = Button(panel, ID_ANY, "Is foo checked?")
        sizer.Add(b, pos=(2, 1), flag=ALIGN_CENTRE)

        b = ToggleButton(panel, ID_ANY, "Disable/Enable 'All'")
        text = "Try to hit <Ctrl+A> and/or go to Edit > Select "
        b.SetToolTip(text)
        sizer.Add(b, pos=(2, 2), flag=ALIGN_CENTRE)

        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableCol(3)
        sizer.AddGrowableRow(0)

        panel.SetSizer(sizer)

        # gospel tapes. for text wrapping purposes.
        self.Bind(EVT_SIZE, self.OnSize)
        # blues tapes. for menu testing purposes.
        self.Bind(EVT_BUTTON, self.OnButton)
        self.Bind(EVT_TOGGLEBUTTON, self.OnToggle)
        # soul tapes. for context menu testing purposes.
        panel.Bind(EVT_RIGHT_UP, self.OnRightUp)
        self.tc.Bind(EVT_RIGHT_UP, self.OnRightUp)
        # cassette tapes. yep.
        self.Bind(EVT_CLOSE, self.OnClose)

        # gtk3 authors have lost something...
        if "gtk3" in wxVersion():
            self.SetSize((500, 400))

    def OnSize(self, evt):
        # 'Reset' text to (re)wrap it.
        self.tc.SetLabel(" ")
        self.tc.SetLabel(self.text)
        self.tc.Wrap(self.GetClientSize()[0] - 30)
        evt.Skip()

    def OnButton(self, evt):
        if "foo" in evt.GetEventObject().GetLabel():
            # How to get a radio or check menu item state:
            v = self.mb.GetItemState("OptionsFoo")
            if v:
                print("Foo is checked.")
            else:
                print("Foo is NOT checked.")

    def OnToggle(self, evt):
        # How to enable or disable a menu item:
        flag = not evt.GetEventObject().GetValue()
        self.mb.EnableItem("EditSelectAll", flag)

        # How to enable or disable a top menu:
        # self.mb.EnableTopMenu("File", not evt.GetEventObject().GetValue())
        # This also works, but accelerators are kept alive; see 'known issues'.

    def OnRightUp(self, evt):
        # Shows how to use a context menu. They have to be created as needed.
        menu = MenuEx(self, my_context_menu, show_title=True)
        menu.Popup(evt)

        # Always destroy a popup menu after using to avoid segfaults.
        menu.Destroy()
        evt.Skip()

    def OnTaskbarLeftDown(self, evt):
        print("You clicked on the taskbar icon")
        evt.Skip()

    def OnClose(self, evt):
        # We need to explicitly destroy the TaskBarIcon object since it is not
        # a child of this frame and so closing the frame will not 'close' the
        # TaskBarIcon object automatically.
        if Platform != THE_GREAT_MAC_PLATFORM:
            self.tbIcon.Destroy()

        # Continue with your regular schedule.
        evt.Skip()

    def UpdateLocale(self, lang_id):
        # Shows how to do wx l10n/i18n stuff
        locale = Locale(lang_id)
        locale.AddCatalogLookupPathPrefix("locale")
        locale.AddCatalog("Demo_metamenus.mo")

        # metamenus l10n/i18n stuff
        self.mb.UpdateMenus()

    def OnMB_OptionsSpam(self):
        # How to get a check or radio menu item state:
        state = self.mb.GetItemState("OptionsSpam")
        print(state, "Spam, Spam, Spam, egg and Spam")

    def OnMB_LanguageSystemDefault(self):
        self.UpdateLocale(LANGUAGE_DEFAULT)

    def OnMB_LanguageChoose(self):
        dlg = SingleChoiceDialog(self, "Select one from you system's available languages:",
                                 'Choose a Language',
                                 sorted(list(GetApp().available_languages.keys())),
                                 CHOICEDLG_STYLE)

        if dlg.ShowModal() == ID_OK:
            sel = GetApp().available_languages[dlg.GetStringSelection()]
            self.UpdateLocale(sel)

        dlg.Destroy()

    def OnMB_HelpAbout(self):
        dlg = MessageDialog(self, 'Welcome!', 'This is a metamenus demonstration program', OK | ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnM_PopThisUpAboutTheUniverse(self):
        # You selected About > The Universe from the menu titled "Pop this up".
        print("42")  # ditto

    def OnMB_FileExit(self):
        self.Destroy()

    def _setupTaskBarIcons(self):
        if Platform != THE_GREAT_MAC_PLATFORM:
            # Fetch the snake, get this frame an icon
            frame_icon = the_snake.GetIcon()
            self.SetIcon(frame_icon)
        if Platform != THE_GREAT_MAC_PLATFORM:
            # Fetch the snake again, shrink it a bit, make it a task bar icon.
            t_snake = Icon(the_snake.GetImage().Scale(16, 16).ConvertToBitmap())
            self.tbIcon = DemoTaskBarIcon(self, t_snake)
            self.tbIcon.Bind(EVT_TASKBAR_LEFT_DOWN, self.OnTaskbarLeftDown)
