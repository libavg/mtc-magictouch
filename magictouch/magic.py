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

from libavg import avg
P = avg.Point2D
from math import pi, atan2
from helper import SimpleEvent

class Border(avg.DivNode):
    def __init__(self, **kw):
        super(Border, self).__init__(**kw)

        #4 edges
        default = dict(parent=self, href="edge.png", pivot=(0,0))
        e = avg.ImageNode(angle=0,**default) #left top
        avg.ImageNode(pos=self.size, angle=pi,**default) #right bottom
        avg.ImageNode(pos=(0,self.size.y), angle=pi*1.5, **default) #left b
        avg.ImageNode(pos=(self.size.x,0), angle=pi*0.5, **default) #right t

        #4 border
        default = dict(parent=self, href="gradient.png") 
        hs = P(self.size.x-e.size.x*2,e.size.y)
        vs = P(self.size.y-e.size.y*2, e.size.x)
        g = avg.ImageNode(pos=(e.size.x,0), size=hs, **default)
        avg.ImageNode(pos=(e.size.x,self.size.y),
                angle=pi, pivot=(g.size.x*0.5, 0), size=hs, **default)
        avg.ImageNode(pos=(0,e.size.y+vs.x),size=vs,pivot=(0,0),
                angle=pi*1.5, **default)
        avg.ImageNode(pos=(self.size.x,e.size.y),size=vs,pivot=(0,0),
                angle=pi*0.5, **default)

        self.color = "".join(map(
                lambda x: str(hex(ord(x)))[2:].rjust(2,'0'),
                e.getBitmap().getPixels()[:3][::-1]))


class Mask(avg.DivNode):
    def __init__(self, screenSize, left, right, top, bottom, **kw):
        super(Mask, self).__init__(**kw)
        self.size = screenSize
        self.sensitive = False
        p = P(left, top)
        b = Border(
            parent=self, pos=p, size=screenSize-(left+right,top+bottom))
        c = b.color
        default = dict(parent=self, opacity=0, fillopacity=1, fillcolor=c)
        avg.RectNode(
                pos=(0,0),
                size=(screenSize.x, p.y), **default) #top
        avg.RectNode(
                pos=(0,p.y),
                size=(left, screenSize.y-top-bottom), **default) # left
        avg.RectNode(
                pos=(screenSize.x-right,p.y),
                size=(right, screenSize.y-top-bottom), **default) #right
        avg.RectNode(
                pos=(0,screenSize.y-bottom),
                size=(screenSize.x,bottom), **default) # bottom


class Knob(avg.DivNode):
    def __init__(self, callback, **kw):
        super(Knob, self).__init__(**kw)
        self.__callback = callback
        img = avg.ImageNode(parent=self, href="knob.png")
        img.pos = map(int,img.size*-0.5)
        self.wheels = []
        for i in range(5):
            self.wheels.append(
                    avg.ImageNode(
                            parent=self,
                            href="wheel%i.png" % i,
                            blendmode='blend',
                            sensitive=False,
                            opacity=0))
            self.wheels[-1].pos = map(int,self.wheels[-1].size *-0.5)
        self.wheels[0].opacity=1
        self.wheelActive = 0
        activeArea = avg.CircleNode(
                parent=self, r=50, opacity=0)
        self.__aa = activeArea

        SimpleEvent(self.__aa, self.__down, self.__motion, lambda x:None)

        self.__cc = None
        self.__oa = 0
        self.__center = self.pos + self.__aa.pos
        self.__c = 0

    def __turn(self, diff):
        self.__c += diff*10
        k = int(self.__c)%5
        self.wheels[self.wheelActive].opacity = 0
        self.wheelActive = k
        self.wheels[self.wheelActive].opacity = 1

    def __down(self, event):
        self.__oa = self.__getAngleFromPos(event.pos)

    def __motion(self, event):
        a = self.__getAngleFromPos(event.pos)
        diff = (self.__oa - a)
        if diff >= pi:
            diff -= pi*2
        if diff <= -pi:
            diff += pi*2
        self.__oa = a
        if self.__callback(diff):
            self.__turn(diff)

    def __getAngleFromPos(self, pos):
        return atan2(*P(self.__center-pos))


class PlayGround(avg.DivNode):
    def __init__(self, start, **kw):
        super(PlayGround, self).__init__(**kw)
        self.__default = dict(parent=self, color='666666',strokewidth=2)
        self.__lastPos = start
        self.__start = start
        self.__createNewLine() 

    def reset(self, pos=False):
        for child in map(
                lambda x: self.getChild(x),
                xrange(self.getNumChildren())):
            child.unlink(True)
        if pos:
            self.__lastPos = self.__start
        self.__createNewLine()

    def addPoint(self, point):
        if map(int, point) == map(int, self.__lastPos):
            return
        poss = self.__lastLine.pos
        if len(poss) > 1000:
            self.__createNewLine()
            poss = [poss[-1]]
        poss.append(P(map(int,point)))
        self.__lastLine.pos = poss
        self.__lastPos = point

    def __createNewLine(self):
        self.__lastLine = avg.PolyLineNode(**self.__default.copy())
        self.__lastLine.pos = [self.__lastPos]

