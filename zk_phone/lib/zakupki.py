import sys
import requests


def zk_version():
    try:
        data = requests.get('https://ai.uaprom/stats/zkprom', verify=False).json()
        return data['by_version']['zkprom1']['cfg']['title']
    except:
        return None
