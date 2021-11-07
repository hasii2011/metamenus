# -*- coding: utf-8 -*-

# context menu used in Demo_metamenus, from the metamenus demo
#
# Written by E. A. Tacao <mailto@tacao.com.br>, (C) 2005... 2020

import Demo_images
bmp1 = Demo_images.bmp1.GetBitmap
bmp2 = Demo_images.bmp2.GetBitmap

my_context_menu = \
[
    ["Pop this up"],   # the first MenuEx line is always the menu title.
    ["  Show more"],     
    ["  Hide less"], 
    ["    Panels"], 
    ["    Frames"], 
    ["      Embed", {"bmp": bmp1}], 
    ["      Cloud", {"bmpChecked": bmp2}], 
    ["  Colours..."],    
    ["  About"], 
    ["    Life"], 
    ["    The Universe"], 
    ["    Everything"], 
    ["  -"],        
    ["  Exit"]
]


#
##
### eof
