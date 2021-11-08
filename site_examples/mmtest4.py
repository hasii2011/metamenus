#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test4.py
#  
#  Copyright 2020 E. A. Tacao <mailto@tacao.com.br>
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  
#  


import wx 
from metamenus.metamenus import MenuBarEx, MenuEx

#-------------------------------------------------------------------------------

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'testing metamenus 4')
        
        menu =  [
                    ['Options'],
                    ['  Foo',    "radio"],
                    ['  Bar',    "radio"],
                    ['  -'],
                    ['  Spam',   "check"],
                    ['  Eggs',   "check"],
                ]
                
        self.mb = MenuBarEx(self, [menu])
        
        self.SetSize((224, 270))
#-------------------------------------------------------------------------------

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()


#
##
### eof
