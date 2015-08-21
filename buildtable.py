#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
from collections import defaultdict
from pinyin_dict import pinyin_dict
from common_surnames import d as common_surnames

phonetic_symbol = {
"ā": "a",
"á": "a",
"ǎ": "a",
"à": "a",
"ē": "e",
"é": "e",
"ě": "e",
"è": "e",
"ō": "o",
"ó": "o",
"ǒ": "o",
"ò": "o",
"ī": "i",
"í": "i",
"ǐ": "i",
"ì": "i",
"ū": "u",
"ú": "u",
"ǔ": "u",
"ù": "u",
"ü": "v",
"ǖ": "v",
"ǘ": "v",
"ǚ": "v",
"ǜ": "v",
"ń": "n",
"ň": "n",
"": "m"
}


def untone(text):
    # This is a limited version only for entities defined in xml_escape_table
    for k, v in phonetic_symbol.items():
        text = text.replace(k, v)
    return text

d = defaultdict(list)

for k, v in pinyin_dict.items():
    for p in v.split(','):
        notone = untone(p.strip())
        d[notone].append(chr(k))

trie = defaultdict(set)

for p in d:
    d[p] = ''.join(sorted(frozenset(d[p])))
    trie[p[0]].add(p)

surnames = defaultdict(list)

for ln in open('data/surnames.txt', 'r').read().splitlines():
    ln = ln.strip().split('\t')
    if len(ln) > 1:
        surnames[untone(ln[1])].append(ln[0])
    else:
        name = ln[0]
        py = untone(' '.join(pinyin_dict[ord(ch)].split(',')[0] for ch in name))
        surnames[py].append(name)

pyformat = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

chrevlookup = %s

pinyintrie = %s

surnamerev = %s
'''

pf = pprint.PrettyPrinter(indent=0).pformat

with open('lookuptable.py', 'w') as f:
    f.write(pyformat % (pf(dict(d)), pf(dict(trie)), pf(dict(surnames))))
