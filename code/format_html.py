import re
import os
import sys
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree, html

workdir = sys.argv[1]

excludes = set(['zhibei'])

for root, dirs, files in os.walk(workdir):
    dirs[:] = [d for d in dirs if d not in excludes]
    for file in files:
        abspath = os.path.join(root, file)
        if file.endswith('.html'):
            with open(abspath, 'r', encoding='utf8') as f:
                content = BeautifulSoup(f.read(), 'html5')
                content_raw = str(content)
                p_tags = content.findAll('p')
                for p in p_tags:
                    innerHtml = p.decode_contents()
                    #innerHtml = p.decode_contents()
                    if '\n' in innerHtml:
                        p.string = innerHtml.replace('\n', '')
                html_output = str(content).replace('&lt;','<').replace('&gt;','>')
            if html_output != content_raw:
                print(abspath)
                with open(abspath, 'w', encoding='utf8') as f:
                    f.write(html_output.replace('<head></head>', ''))