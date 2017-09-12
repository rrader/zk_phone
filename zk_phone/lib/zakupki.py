import sys
import requests


def zk_version():
    try:
        data = requests.get('https://ai.uaprom/stats/zkprom', verify=False).json()
        return data['last_migration']['source_title']
    except:
        return None
