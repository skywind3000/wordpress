#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# config.py - 
#
# Created by skywind on 2019/05/04
# Last Modified: 2019/05/04 20:05:31
#
#======================================================================
from __future__ import print_function, unicode_literals
import sys
import os


#----------------------------------------------------------------------
# path setup
#----------------------------------------------------------------------
FILE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.abspath(os.path.join(FILE, '..'))

sys.path.append(os.path.join(HOME, 'lib'))

if __name__ is None:
    sys.path.append('../lib')

try:
    import ascmini
    import markdown2
except:
    pass


#----------------------------------------------------------------------
# config
#----------------------------------------------------------------------
cfg = ascmini.ConfigReader(os.path.join(HOME, 'etc/config.ini'))


#----------------------------------------------------------------------
# option 
#----------------------------------------------------------------------
options = {}

options['site'] = cfg.option('default', 'site', '').strip()
options['user'] = cfg.option('default', 'user', '').strip()
options['passwd'] = cfg.option('default', 'passwd', '').strip()


#----------------------------------------------------------------------
# styles 
#----------------------------------------------------------------------
styles = {}

styles['tabsize'] = cfg.option('markdown', 'tabsize', 4)


#----------------------------------------------------------------------
# testing suit 
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        print(options)
        print(styles)
        return 0
    test1()



