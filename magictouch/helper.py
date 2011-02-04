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
from math import pi, sin, cos
import random

P = avg.Point2D

def getArc(x,y,loc):
    strToPi = dict(lb=1.5*pi, rb=0, rt=pi*0.5, lt=pi*1.0)
    offset = strToPi[loc]
    pos = P(x,y)
    points = []
    for i in range(20,0,-1):
        points.append(pos + P(
                10*sin(offset + pi*0.5*i/20),
                10*cos(offset + pi*0.5*i/20)))
    return points

class SimpleEvent(object):
    def __init__(self, node, down, motion, up):
        self.__node = node
        self.__downCb = down
        self.__motionCb = motion
        self.__upCb = up
        self.__cc = None

        self.__node.setEventHandler(
                avg.CURSORDOWN,
                avg.MOUSE,
                self.__down)
        self.__node.setEventHandler(
                avg.CURSORMOTION,
                avg.MOUSE,
                self.__motion)
        self.__node.setEventHandler(
                avg.CURSORUP,
                avg.MOUSE,
                self.__up)

    def __down(self, event):
        if self.__cc == None:
            self.__node.setEventCapture(event.cursorid)
            self.__cc = event.cursorid
            self.__downCb(event)

    def __motion(self, event):
        if self.__cc == event.cursorid:
            self.__motionCb(event)

    def __up(self, event):
        if self.__cc == event.cursorid:
            self.__node.releaseEventCapture(event.cursorid)
            self.__cc = None
            self.__upCb(event)

class Noise(avg.ImageNode):
    def __init__(self, **kw):
        super(Noise, self).__init__(**kw)
        self.sensitive=False
        self.opacity=0.05
        self.blendmode='blend'
        b = avg.Bitmap(self.size, avg.I8, "noisnoisee")
        s = ""
        randomString = ""
        for k in range(int(self.size.y*3)):
            randomString += chr(random.randint(0,255))
        c = 0
        numPixels = int(self.size.x * self.size.y)
        while c < numPixels:
            l = random.randint(0,len(randomString))
            if c + l > numPixels:
                l = numPixels - c
            s += randomString[:l]
            c += l
        b.setPixels(s)
        self.setBitmap(b)

