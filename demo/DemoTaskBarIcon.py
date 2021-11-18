from wx import EVT_MENU
from wx.adv import TaskBarIcon

from demo.Demo_context_menu import my_context_menu
from metamenus.MenuEx import MenuEx


class DemoTaskBarIcon(TaskBarIcon):
    """
    For demonstration on Windows
    """
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
        self.Bind(EVT_MENU, self.OnMenu)

    def OnMenu(self, evt):
        self.menu.OnM_(evt)

    def CreatePopupMenu(self):
        self.menu = MenuEx(self.frame, my_context_menu)
        return self.menu
