#!/usr/local/bin/python3

import re
import os
import pandas as pd
import json

def print_json(res, indent=2):
    json_object = json.loads(res)
    print(json.dumps(json_object, indent=2))
    
def funcionaFuncao(res):
    print('funciona')
