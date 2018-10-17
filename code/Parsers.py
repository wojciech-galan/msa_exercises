#! /usr/bin/python
# -*- coding: utf-8 -*-

import re

SP_RE = re.compile("SP score= ([0-9.]+)")
TC_RE = re.compile("TC score= ([0-9.]+)")

def parse_blaliscore_v2_output(text):
    sp = SP_RE.search( text.decode("utf-8")).group(1)
    tc = TC_RE.search(text.decode("utf-8")).group(1)
    return float(sp), float(tc)