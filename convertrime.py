#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from zhconv import convert as zhconv

transformtable = (
(re.compile('([nl])v'), r'\1ü'),
(re.compile('([nl])ue'), r'\1üe'),
(re.compile('([jqxy])v'), r'\1u'),
(re.compile('eh'), 'ê'),
(re.compile('([aeiou])(ng?|r)([1234])'), r'\1\3\2'),
(re.compile('([aeo])([iuo])([1234])'), r'\1\3\2'),
(re.compile('a1'), 'ā'),
(re.compile('a2'), 'á'),
(re.compile('a3'), 'ǎ'),
(re.compile('a4'), 'à'),
(re.compile('e1'), 'ē'),
(re.compile('e2'), 'é'),
(re.compile('e3'), 'ě'),
(re.compile('e4'), 'è'),
(re.compile('o1'), 'ō'),
(re.compile('o2'), 'ó'),
(re.compile('o3'), 'ǒ'),
(re.compile('o4'), 'ò'),
(re.compile('i1'), 'ī'),
(re.compile('i2'), 'í'),
(re.compile('i3'), 'ǐ'),
(re.compile('i4'), 'ì'),
(re.compile('u1'), 'ū'),
(re.compile('u2'), 'ú'),
(re.compile('u3'), 'ǔ'),
(re.compile('u4'), 'ù'),
(re.compile('ü1'), 'ǖ'),
(re.compile('ü2'), 'ǘ'),
(re.compile('ü3'), 'ǚ'),
(re.compile('ü4'), 'ǜ'),
(re.compile('5'), ''),
(re.compile('ê\d'), 'ê'))

def pynum2tone(pinyin):
    for rexp, rsub in transformtable:
        pinyin = rexp.sub(rsub, pinyin)
    return pinyin

def uniq(seq): # Dave Kirby
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

dic = {}

started = False
with open('terra_pinyin.dict.yaml') as f:
    for ln in f:
        ln = ln.strip()
        if started and ln:
            l = ln.split('\t')
            w, c = l[0], pynum2tone(l[1])
            if len(w) > 1:
                continue
            if w in dic:
                dic[w].append(c)
            else:
                dic[w] = [c]
            ws = zhconv(w, 'zh-hans')
            if ws != w:
                if ws in dic:
                    dic[ws].append(c)
                else:
                    dic[ws] = [c]
        elif ln == '...':
            started = True

header = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Pinyin dictionary from librime/terra_pinyin
"""

# Unicode 编码作为字典的 key
pinyin_dict = {
'''

with open('pinyin_dict.py', 'w') as f:
    f.write(header)
    for c in sorted(dic):
        f.write("0x%04x: '%s', # %s\n" % (ord(c), ','.join(uniq(dic[c])), c))
    f.write('}\n')
