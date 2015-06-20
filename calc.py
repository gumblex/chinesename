#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
from collections import Counter
from common_surnames import d as common_surnames

names = Counter()
surnames = set()

with open('data/surnames.txt', 'r') as f:
    for ln in f:
        l = ln.strip().split()[0]
        if l:
            surnames.add(l)

# filters only Han names

with open('data/allnames.txt', 'r') as f:
    for l in f:
        fullname = l.strip()
        if len(fullname) < 2 or len(fullname) > 4:
            continue
        if len(fullname) > 2 and fullname[:2] in surnames:
            name = fullname[2:]
            if not name:
                name = fullname[1:]
            elif len(name) > 2:
                continue
        elif fullname[0] in surnames:
            name = fullname[1:]
            if not name:
                name = fullname
            elif len(name) > 2:
                continue
        else:
            continue
        names[name] += 1

popnames = {}
with open('data/popular.txt', 'r') as f:
    for l in f:
        fullname, num = tuple(l.strip().split())
        if not fullname:
            continue
        num = int(num)
        if fullname[0] in surnames:
            name = fullname[1:]
            sur = fullname[0]
        else:
            continue
        if name in popnames:
            popnames[name] = (
                popnames[name][0] + num, popnames[name][1] + common_surnames[sur])
        else:
            popnames[name] = (num, common_surnames[sur])

for name in popnames:
    names[name] = int(names[name] * 0.8 + (popnames[name][0] /
        popnames[name][1] / 1360000000 * 0.2))

firstchar = Counter()
secondchar = Counter()
for name in names:
    firstchar[name[0]] += names[name]
    secondchar[name[1:]] += names[name]

for name in set(firstchar.keys()):
    if firstchar[name] < 15:
        print(name, firstchar[name])
        del firstchar[name]

for name in set(secondchar.keys()):
    if secondchar[name] < 15:
        print(name, secondchar[name])
        del secondchar[name]

count = sum(firstchar.values())
for name in firstchar:
    firstchar[name] /=  count

count = sum(secondchar.values())
for name in secondchar:
    secondchar[name] /=  count

with open('namemodel.m', 'wb') as f:
    pickle.dump((dict(firstchar), dict(secondchar)), f)
with open('names.m', 'wb') as f:
    pickle.dump(dict(names), f)
