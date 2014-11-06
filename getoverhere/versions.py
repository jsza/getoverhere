import os
import json



def getVersion(deployment):
    path = os.path.join(os.getcwd(), 'versions.cfg')
    if not os.path.exists(path):
        versions = {
            'metamod': None,
            'sourcemod': None,
            'stripper': None
        }
        with open(path, 'wb') as f:
            json.dump(versions, f)
    else:
        with open(path) as f:
            versions = json.load(f)
    return versions[deployment]



def changeVersion(deployment, value):
    path = os.path.join(os.getcwd(), 'versions.cfg')

    with open(path) as f:
        versions = json.load(f)

    versions[deployment] = value
    with open(path, 'w') as f:
        json.dump(versions, f)
