# -*- coding: utf-8 -*-

# context menu used in Demo_metamenus, from the metamenus demo
#
# Written by E. A. Tacao <mailto@tacao.com.br>, (C) 2005... 2020
from typing import Callable

from demo.Demo_images import bmp1
from demo.Demo_images import bmp2

embedBmp: Callable = bmp1.GetBitmap
cloudBmp: Callable = bmp2.GetBitmap

my_context_menu = \
[
    ["Pop this up"],   # the first MenuEx line is always the menu title.
    ["  Show more"],     
    ["  Hide less"], 
    ["    Panels"], 
    ["    Frames"], 
    ["      Embed", {"bmp":        embedBmp}],
    ["      Cloud", {"bmpChecked": cloudBmp}],
    ["  Colours..."],    
    ["  About"], 
    ["    Life"], 
    ["    The Universe"], 
    ["    Everything"], 
    ["  -"],        
    ["  Exit"]
]
