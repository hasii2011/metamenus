# -*- coding: utf-8 -*-

# menu bar used in Demo_metamenus, from the metamenus demo
#
# Written by E. A. Tacao <mailto@tacao.com.br>, (C) 2005... 2020

# Our menus are here, in this separate file, because it is a good idea to:
#  1. Have your menus in a separate file (!) and
#  2. Make the separate file in question to contain only your menus.
#
# This way you will be able to use metamenus from a command line to generate 
# a temporary file that can be read by gettext utilities in order to create
# a .po file with strings to be translated. See the metamenus.__doc__ for 
# more details. And it's easier to debug.

# Actually it is not necessary to import wx here; we would just have to
# replace wx objects to python objects, so that in this sample:
#    replace wx.RED to (255, 0, 0);
#    replace wx.ITEM_CHECK to "check";
#    replace wx.ITEM_RADIO to "radio";
# You may thus remove this import if your menu is in a separate file and 
# doesn't use any wx object.

from typing import Callable

import wx

# This is used in this example to get some bitmaps.
from demo.Demo_images import bmp1
from demo.Demo_images import bmp2

allBmp: Callable = bmp1.GetBitmap
noneBmp: Callable = bmp2.GetBitmap

my_menubar = [
    [
        ['&File'],
        ['  &New\tCtrl+N'],          
        ['  &Open...\tCtrl+O'],
        ['  &Save\tCtrl+S'],
        ['  Save &As...\tCtrl+Shift+S'],
        ['  -'],
        ['  Publis&h\tCtrl+Shift+P'],
        ['  -'],
        ['  &Close\tCtrl+W'],
        ['  C&lose All'],
        ['  -'],
        ['  E&xit\tAlt+X']
    ],

    [
        ['&Edit'],
        ['  Cu&t\tCtrl+X'],
        ['  &Copy\tCtrl+C'],
        ['  &Paste\tCtrl+V'],
        ['  Select'],
        ['    All\tCtrl+A', {"bmpChecked": allBmp}],
        ['    None',        {"bmpChecked": noneBmp}],
        ['    -'],
        ['    Invert Selection'],
        ['  -'],
        ['  Delete\tDel',  ("Information on deletion", ), {"fgColour": wx.RED}],
    ],

    [
        ['&Options'],
        ['  &Foo',         ("Foo status bar text", wx.ITEM_RADIO)],
        ['  &Bar',         ("Bar status bar text", wx.ITEM_RADIO)],
        ['  -'],
        ['  &Spam',        "check"],
        ['  &Eggs',        wx.ITEM_CHECK],
    ],

    [
        ['&Language'],
        ['  &System Default'],
        ['  &Choose...'],
    ],

    [
        ['&Help'],
        ['  &About\tCtrl+KP_8'],
    ]
]
