#!/usr/bin/env python3

import sys

import wx
from wx import Locale
from wx import StaticLine
from wx.adv import TaskBarIcon


from metamenus.metamenus import MenuBarEx
from metamenus.metamenus import MenuEx

from Demo_menubar import my_menubar
from Demo_context_menu import my_context_menu
from Demo_images import the_snake

# -*- coding: utf-8 -*-

#
# metamenus demo vs. 0.11 (13/06/2020)
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


sys.path.append("..")


class tbIcon(TaskBarIcon):
    def __init__(self, frame, icon):
        TaskBarIcon.__init__(self)
        # This shows how to use a TaskBarIcon with metamenus.

        # The icon.
        self.SetIcon(icon)
        
        # TaskBarIcons are parentless objects, but we still need a reference 
        # to the object that will handle the methods called from metamenu's 
        # MenuEx object.
        self.frame = frame
        
        # And this connects MenuEx, the 'parent' frame and self.
        self.Bind(wx.EVT_MENU, self.OnMenu)

    def OnMenu(self, evt):
        self.menu.OnM_(evt)

    def CreatePopupMenu(self):
        self.menu = MenuEx(self.frame, my_context_menu)
        return self.menu


class mmTestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'metamenus demo')

        # Fetch the snake, get this frame an icon
        frame_icon = the_snake.GetIcon()
        self.SetIcon(frame_icon)

        # Fetch the snake again, shrink it a bit, make it a task bar icon.
        t_snake = wx.Icon(the_snake.GetImage().Scale(16, 16).ConvertToBitmap())
        self.tbIcon = tbIcon(self, t_snake)
        self.tbIcon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnTaskbarLeftDown)

        # Not compulsory, but here we will test metamenus status messages
        self.CreateStatusBar()
        self.SetStatusText("Well here is the status bar")

        # This creates and attaches the menu bar to this frame
        self.mb = MenuBarEx(self, my_menubar)

        # noinspection SpellCheckingInspection
        """
        Shows how to use the custfunc arg
        telling to use 'onSave' instead of 'OnMB_FileSave':
        self.mb = MenuBarEx(self, my_menubar, custfunc={"FileSave": "onSave"})
        """
        panel = wx.Panel(self)

        sizer = wx.GridBagSizer()

        self.text = "metamenus created your wx.MenuBar for this frame, " \
                    "so that now you can play around with its menus " \
                    "to see how they behave.\n\n" \
                    "metamenus also created a popup wx.Menu here. " \
                    "Right-click somewhere to test it."
        self.tc = wx.StaticText(panel, wx.ID_ANY, self.text)
        sizer.Add(self.tc, pos=(0, 0), span=(1, 4), flag=wx.EXPAND | wx.ALL,
                  border=15)

        staticLine: StaticLine = StaticLine(panel)
        sizer.Add(staticLine, pos=(1, 0), span=(1, 4), flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=15)

        b = wx.Button(panel, wx.ID_ANY, "Is foo checked?")
        sizer.Add(b, pos=(2, 1), flag=wx.ALIGN_CENTRE)

        b = wx.ToggleButton(panel, wx.ID_ANY, "Disable/Enable 'All'")
        text = "Try to hit <Ctrl+A> and/or go to Edit > Select "
        b.SetToolTip(text)
        sizer.Add(b, pos=(2, 2), flag=wx.ALIGN_CENTRE)

        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableCol(3)
        sizer.AddGrowableRow(0)
        
        panel.SetSizer(sizer)

        # gospel tapes. for text wrapping purposes. 
        self.Bind(wx.EVT_SIZE, self.OnSize)
        # blues tapes. for menu testing purposes. 
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggle)
        # soul tapes. for context menu testing purposes. 
        panel.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.tc.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        # cassette tapes. yep. 
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        # gtk3 authors have lost something...        
        if "gtk3" in wx.version():
            self.SetSize((500, 400))

    def OnSize(self, evt):
        # 'Reset' text to (re)wrap it.
        self.tc.SetLabel(" ")
        self.tc.SetLabel(self.text)
        self.tc.Wrap(self.GetClientSize()[0]-30)
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
        self.UpdateLocale(wx.LANGUAGE_DEFAULT)

    def OnMB_LanguageChoose(self):
        dlg = wx.SingleChoiceDialog(self, "Select one from you system's available languages:",
                                    'Choose a Language',
                                    sorted(list(wx.GetApp().available_languages.keys())),
                                    wx.CHOICEDLG_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            sel = wx.GetApp().available_languages[dlg.GetStringSelection()]
            self.UpdateLocale(sel)

        dlg.Destroy()

    def OnMB_HelpAbout(self):
        dlg = wx.MessageDialog(self, "Hello!", "metamenus demo", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnM_PopThisUpAboutTheUniverse(self):
        # You selected About > The Universe from the menu titled "Pop this up".
        print("42")  # ditto

    def OnMB_FileExit(self):
        self.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        
        # Find languages available on this system:
        self.available_languages = {}
        for i in [i for i in dir(wx) if i.startswith("LANGUAGE_")]:
            if i not in ["LANGUAGE_DEFAULT", 
                         "LANGUAGE_UNKNOWN", 
                         "LANGUAGE_USER_DEFINED"]:
                at = getattr(wx, i)
                if wx.Locale().IsAvailable(at):
                    self.available_languages[i] = at
        
        mmTestFrame().Show(True)
        return True


if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
