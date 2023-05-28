from newpoc.utils.load_conf import ini_to_dict
from newpoc.api import requests
import base64

def fofa_search(inputs):
    inputs_base64 = base64.b64encode(bytes(inputs, encoding='utf-8'))
    ss = str(inputs_base64).strip('b').strip('\'')
    conf = ini_to_dict()
    res = requests.get('https://fofa.info/api/v1/search/all?email={0}&key={1}&qbase64={2}'.format(conf.FOFA.email, conf.FOFA.key, ss))
    reis = res.json()
    try:
        return ['FOFA'] + reis['results']
    except:
        if 'errmsg' in reis:
            return reis['errmsg']

