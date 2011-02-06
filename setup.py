#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='magicotuch',
    version='0.1',
    author='Benedikt Seidl',
    author_email='Benedikt.Seidl@gmx.de',
    url='https://www.libavg.de/svn/trunk/avg_media/mtc/magictouch/',
    license='GNU GPL',
    packages=['magicotuch'],
    scripts=['scripts/magictouch'],
    package_data={
            'magicotuch': ['media/*.png', 'fonts/*.ttf'],
    }
)

