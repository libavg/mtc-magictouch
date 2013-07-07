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

from libavg import avg, player
from helper import getArc, SimpleEvent

P = avg.Point2D

class MenuButton(avg.DivNode):
    def __init__(self, text, cb, parent=None, **kw):
        super(MenuButton, self).__init__(**kw)
        self.registerInstance(self, parent)
        
        points = []
        points += getArc(0,0, "lt")
        points += getArc(100,0, "rt")
        points += getArc(100,20, "rb")
        points += getArc(0,20, "lb")
        points.append(points[0])
        self.__bg = avg.PolygonNode(parent=self,
                pos=points,
                opacity=0)
        self.__up(None, noCallback=True)
        self.appendChild(text)
        text.sensitive = False
        text.pos = (50,-2)
        SimpleEvent(self.__bg, self.__down, lambda x:None, self.__up)
        self.__cb = cb

    def __down(self, event):
        self.__bg.fillopacity = 0.8

    def __up(self, eventi, noCallback=False):
        self.__bg.fillopacity = 0.5
        noCallback or self.__cb()


class Menu(avg.DivNode):
    def __init__(self, centerBottom, quitCb, resetCb, parent=None, **kw):
        super(Menu, self).__init__(**kw)
        self.registerInstance(self, parent)
        
        w = 200
        h = 200
        self.__shield = avg.RectNode(
                parent=self.getParent(),
                pos=P(centerBottom) - P(w,0),
                opacity=0,
                size=(w*2, h))
        self.__background = MenuBackground(parent=self, w=w, h=h)
        
        self.__inPos = P(centerBottom) + P(0,h+20)
        self.__outPos = P(centerBottom)
        self.__cursorOffset = P()
        self.__wasOutWhenPressed = False
        
        content = avg.DivNode(parent=self, pos=(-w,-h))
        
        d = dict(fontsize=20,
                font="DejaVu Sans",
                variant="ExtraLight",
                alignment='center',
                color='333333')
        
        MenuButton(parent=content,
                text = avg.WordsNode(text="Quit", **d),
                cb = quitCb,
                pos = (w-120,150))
        MenuButton(parent=content,
                text = avg.WordsNode(text="Reset", **d),
                cb = resetCb,
                pos = (w+20,150))
        
        d = dict(parent=content, **d)
        avg.WordsNode(text="""magictouch""", pos=(w,10), **d)
        avg.WordsNode(text="""© 2011 Benedikt Seidl<br/>
                Made with Python and libavg<br/>
                magictouch is licensed under GNU GPL""", pos=(w,49), **d)

        self.__aa = avg.RectNode(parent=self,
                size=(40,40),
                pos =(-20,-h-60),
                opacity=0)
        SimpleEvent(self.__aa, self.__down, self.__motion, self.__up)
        self.reset()
    
    def reset(self):
        self.pos = self.__outPos
        player.setTimeout(800, lambda: self.__animateTo(self.__inPos))

    def __down(self, event):
        self.__background.highlight(True)
        self.__cursorOffset = self.pos - event.pos
        newposY = (event.pos + self.__cursorOffset).y
        if newposY - (self.__inPos + self.__outPos).y * 0.5 < 0:
            self.__wasOutWhenPressed = True
        else:
            self.__wasOutWhenPressed = False
    
    def __motion(self, event):
        newpos = P(self.pos.x, (event.pos + self.__cursorOffset).y)
        if self.__outPos.y <= newpos.y <= self.__inPos.y:
            self.pos = newpos
    
    def __up(self, event):
        self.__background.highlight(False)
        enoughMoved = abs(event.contact.motionvec.y) > 30
        if self.__wasOutWhenPressed == enoughMoved:
            pos = self.__inPos
        else:
            pos = self.__outPos
        self.__animateTo(pos)

    def __animateTo(self, pos):
        avg.LinearAnim(self,
                "pos",
                200,
                self.pos,
                pos,
                True).start()


class MenuBackground(avg.DivNode):
    def __init__(self, w, h, parent=None, **kw):
        super(MenuBackground, self).__init__(**kw)
        self.registerInstance(self, parent)
        
        self.__outline = avg.PolygonNode(
                parent=self,
                opacity=0.3,
                fillopacity=0.9,
                fillcolor='cccccc')
        self.__arrow = avg.PolygonNode(parent=self,
                fillopacity=0.8,
                opacity=0)
        player.setTimeout(500,lambda :self.highlight(False))
        ps = []
        ps += getArc(-w,0, "lb")
        ps += getArc(-w,-h, "lt")
        ps += getArc(-20-21,-h-21, "rb")[::-1]
        ps += getArc(-20,-h-60, "lt")
        ps += getArc(+20,-h-60, "rt")
        ps += getArc(+20+21,-h-21, "lb")[::-1]
        ps += getArc(w,-h, "rt")
        ps += getArc(+w,0, "rb")
        ps.append(ps[0])
        self.__outline.pos = ps
        self.__arrow.pos = map(lambda x: P(0,-h-60)+x,
                [[14, 14], [0, 0], [-14, 14],
                [-10, 18], [-3, 11], [-3, 30],
                [3, 30], [3, 11], [10, 18], [14, 14]])

    def highlight(self, val):
            avg.LinearAnim(
                    self.__arrow,
                    "fillopacity",
                    200,
                    self.__arrow.fillopacity,
                    0.8 if val else 0.3).start()

