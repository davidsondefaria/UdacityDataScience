#!/usr/local/bin/python3

import re
import os
import pandas as pd
import json
from pprint import pprint
from tabulate import tabulate


def print_pretty(res, indent=2, tabular=False):
    if(tabular):
        if type(res) == type({}) or type(res) == type([]):
            dict_keys = list(res['essay'].keys())
            print(tabulate([ [k, *v.values()] for k, v in res.items() ], headers=['content', *dict_keys]))
        else:
            print(json.dumps(res, indent, ensure_ascii=False))
    else:
        if type(res) == type({}) or type(res) == type([]):
            pprint(res, indent=indent, width=1)
        else:
            print(json.dumps(res, indent, ensure_ascii=False))