# -*- coding: utf-8 -*-

import os

def filen(name: str):
    # For absolute path.
    
    base_path = os.path.abspath('.')
    if 'emoj' in name:
        if name in os.listdir(base_path):
            return os.path.join(base_path, name)
        else:
            base_path = base_path.rpartition('\\')[0]
            if name in os.listdir(base_path):
                return os.path.join(base_path, name)
            else:
                return None
    elif name in os.listdir(base_path):
        return os.path.join(base_path, name)
    else:
        return None
