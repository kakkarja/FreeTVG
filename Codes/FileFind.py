# -*- coding: utf-8 -*-

import os

def filen(name: str):
    # For absolute path.
    
    base_path = os.path.abspath('.')
    if name in os.listdir(base_path):
        return os.path.join(base_path, name)
    else:
        return None
