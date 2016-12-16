import pickle
import os

config_file = 'config.pkl'

def clear():
    if os.path.isfile(config_file):
        os.remove(config_file)

def save_obj(raw_obj, origin):
    obj = origin
    obj['oj'] = raw_obj.oj
    obj['prob'][raw_obj.oj] = raw_obj.prob
    obj['lang'][raw_obj.oj] = raw_obj.lang
    obj['code'] = raw_obj.code
    with open(config_file, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj():
    if os.path.isfile(config_file):
        with open(config_file, 'rb') as f:
            return pickle.load(f)
    else:
        return {
            'oj': None,
            'prob': {},
            'lang': {},
            'code': None
        }
