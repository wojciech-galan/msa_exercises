#! /usr/bin/python
# -*- coding: utf-8 -*-

import re

SP_RE = re.compile("SP score= ([0-9.]+)")
TC_RE = re.compile("TC score= ([0-9.]+)")

class NotProperNumberException(Exception):
    pass

def parse_blaliscore_v2_output(text):
    try:
        sp = SP_RE.search(text.decode("utf-8")).group(1)
        tc = TC_RE.search(text.decode("utf-8")).group(1)
    except AttributeError:
        raise NotProperNumberException()
    return float(sp), float(tc)
