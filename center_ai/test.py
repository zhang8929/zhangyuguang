#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
h5 = '<img class="normal" width="500px" data-loadfunc="0" <src="https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=4235327086,2456842491&amp;fm=173&amp;app=25&amp;f=JPEG?w=500&amp;h=300&amp;s=1CEDFC045EF254961FBAA0DA0300D09F"/> data-loaded="0">'

res = re.findall(r'src=(.*)/>',h5)
print res[0]
print os.path.dirname(os.path.realpath(__file__))