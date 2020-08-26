#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 18:17:43 2020

@author: hliu
"""

import os
import sys

workdir = sys.argv[1]
className = sys.argv[2]

excludes = set(['resource'])


def modify(content, className):
    lines = content.split('\n')
    class_content = ''.join([l if '<p class="%s">' % className in l else '#' for l in lines])
    class_content = class_content.replace('</p>', '</p>\n')
    class_group = [l for l in class_content.split('#') if l != '']
    formatClass = lambda x: '<div class="%s">\n'%className+x.replace('<p class="%s">'%className, '<p>')+'</div>\n'
    new_class_group = [formatClass(c) for c in class_group]
    for c, new_c in zip(class_group, new_class_group):
        content = content.replace(c, new_c)
    return content


for root, dirs, files in os.walk(workdir):
    dirs[:] = [d for d in dirs if d not in excludes]
    for file in files:
        abspath = os.path.join(root, file)
        if file.endswith('.html'):
            with open(abspath, 'r', encoding='utf8') as f:
                content = f.read()
                raw = content
                if '<p class="%s">' % className in content:
                    content = modify(content, className)
                else:
                    pass
            if content != raw:
                with open(abspath, 'w') as out:
                    out.write(content)
                    
