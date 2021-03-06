#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MagicTouch
#
# Copyright (C) 2011
#    Benedikt Seidl, <Benedikt.Seidl at gmx dot de>
#
# This file is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, see <http://www.gnu.org/licenses/>.


import os
from libavg import avg, utils, Point2D, player, app
P = Point2D

from magic import PlayGround, Mask, Knob
from helper import Noise
from menu import Menu



class MagicTouch(app.MainDiv):
    def onInit(self):
        self.mediadir = utils.getMediaDir(__file__)
        left = right = top = 60
        bottom = 160
        self.__point = P(left, top) \
                + ((self.size - (right+left, bottom+top)) * 0.5)

        avg.RectNode(
                parent=self,
                size=self.size,
                opacity=0,
                fillopacity=1,
                fillcolor='cccccc')
        self.__pg = PlayGround(parent=self,
                start=self.__point)
        self.__menu = Menu(parent=self,
                quitCb = player.stop,
                resetCb = self.__pg.reset,
                centerBottom=(self.size.x * 0.5,self.size.y-bottom-17))
        m = Mask(parent=self,
                left=left,right=right,
                top=top,bottom=bottom,
                screenSize=self.size)
        l = Knob(parent=self,
                callback=lambda x: self.__move(P(0,x)),
                pos=(0.5*bottom,self.size.y-bottom*0.5))
        l = Knob(parent=self,
                callback=lambda x: self.__move(P(x,0)),
                pos=(self.size.x-bottom*0.5,self.size.y-bottom*0.5))
        
        img = avg.ImageNode(parent=self,
                href="magic-libavg-touch.png",
                pos=(self.size.x/2, self.size.y-bottom*0.5))
        img.pos = img.pos - img.size * 0.5
        Noise(parent=self, size=self.size)
        
        self.__left = left
        self.__right = right
        self.__bottom = bottom
        self.__top = top

        self.__setupMultitouch()

    def __move(self, diff):
        point = self.__point + diff*10
        m = 17 # transparent part of the graphic
        sz = self.size
        if self.__left + m + 1 < point.x < sz.x-self.__right -m and\
           self.__top + m + 1 < point.y < sz.y-self.__bottom - m:
            self.__point = point
            self.__pg.addPoint(self.__point)
            return True
        else:
            return False

    def _getPackagePath(self):
        return __file__

    def __setupMultitouch(self):
        if app.instance.settings.getBoolean('multitouch_enabled'):
            return

        import platform

        if platform.system() == 'Linux':
            os.putenv('AVG_MULTITOUCH_DRIVER', 'XINPUT')
        elif platform.system() == 'Windows':
            os.putenv('AVG_MULTITOUCH_DRIVER', 'WIN7TOUCH')
        else:
            os.putenv('AVG_MULTITOUCH_DRIVER', 'TUIO')

        try:
            player.enableMultitouch()
        except Exception, e:
            os.putenv('AVG_MULTITOUCH_DRIVER', 'TUIO')
            player.enableMultitouch()
