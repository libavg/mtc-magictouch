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
from libavg import avg, AVGAppUtil, Point2D
from libavg.gameapp import GameApp
P = Point2D

from magic import PlayGround, Mask, Knob
from helper import Noise
from menu import Menu

__all__ = ['apps', 'MagicTouch']


#avg.Player.get().setMultiSampleSamples(4) # better quality

class MagicTouch(GameApp):
    def init(self):
        self._parentNode.mediadir = AVGAppUtil.getMediaDir(__file__)
        screenSize = avg.Player.get().getRootNode().size
        self.__screenSize = screenSize
        root = self._parentNode
        left = right = top = 60
        bottom = 160
        self.__point = P(left, top) \
                + ((screenSize - (right+left, bottom+top)) * 0.5)

        avg.RectNode(
                parent=root,
                size=screenSize,
                opacity=0,
                fillopacity=1,
                fillcolor='cccccc')
        self.__pg = PlayGround(parent=root,
                start=self.__point)
        self.__menu = Menu(parent=root,
                quitCb = self.leave,
                resetCb = self.__pg.reset,
                centerBottom=(screenSize.x * 0.5,screenSize.y-bottom-17))
        m = Mask(parent=root,
                left=left,right=right,
                top=top,bottom=bottom,
                screenSize=screenSize)
        l = Knob(parent=root,
                callback=lambda x: self.__move(P(0,x)),
                pos=(0.5*bottom,screenSize.y-bottom*0.5))
        l = Knob(parent=root,
                callback=lambda x: self.__move(P(x,0)),
                pos=(screenSize.x-bottom*0.5,screenSize.y-bottom*0.5))
        
        img = avg.ImageNode(parent=root,
                href="magic-libavg-touch.png",
                pos=(screenSize.x/2, screenSize.y-bottom*0.5))
        img.pos = img.pos - img.size * 0.5
        Noise(parent=root, size=screenSize)
        
        self.__left = left
        self.__right = right
        self.__bottom = bottom
        self.__top = top

    def _enter(self):
        print "endetetetet"
        self.__pg.reset(pos=True)
        self.__menu.reset()

    def __move(self, diff):
        point = self.__point + diff*10
        m = 17 # transparent part of the graphic
        sz = self.__screenSize
        if self.__left + m + 1 < point.x < sz.x-self.__right -m and\
           self.__top + m + 1 < point.y < sz.y-self.__bottom - m:
            self.__point = point
            self.__pg.addPoint(self.__point)
            return True
        else:
            return False

#--------------------------------------------------------------------------#

def createPreviewNode(maxSize):
    filename = os.path.join(AVGAppUtil.getMediaDir(__file__), 'preview.png')
    return AVGAppUtil.createImagePreviewNode(maxSize, absHref = filename)

apps = ({'class': MagicTouch, 'createPreviewNode': createPreviewNode},)

if __name__ == '__main__':
   MagicTouch.start()
