import json
import os

configPath = os.path.join(os.path.expanduser('~'), '.config', 'getoverhere')

if not os.path.exists(configPath):
    os.makedirs(configPath)



def getVersion(basePath, deployment):
    path = os.path.join(configPath, 'versions.cfg')
    if not os.path.exists(path):
        versions = {}
        with open(path, 'wb') as f:
            json.dump(versions, f)
    else:
        with open(path) as f:
            versions = json.load(f)
    return versions.get(basePath, {}).get(deployment)



def changeVersion(basePath, deployment, value):
    path = os.path.join(configPath, 'versions.cfg')

    if os.path.exists(path):
        with open(path) as f:
            versions = json.load(f)
    else:
        versions = {}

    versions.setdefault(basePath, {})[deployment] = value
    with open(path, 'w') as f:
        json.dump(versions, f)



def getSettings():
    return {
        'sourcemod': {
            'scheme': 'regex',
            'baseURL': 'https://www.sourcemod.net/smdrop/1.7/',
            'regex': '^sourcemod-1\.7\.[0-9]*-(git|hg)[0-9]*-(windows|linux|mac)\.(zip|tar\.gz)$',
            'updateFolders': [
                'addons/sourcemod/bin/',
                'addons/sourcemod/extensions/',
                'addons/sourcemod/translations/',
                'addons/sourcemod/plugins/'
            ],
            'onlyUpdateExisting': [
                'addons/sourcemod/plugins'
            ]
        },
        'metamod': {
            'scheme': 'regex',
            'baseURL': 'https://www.metamodsource.net/mmsdrop/1.11/',
            'regex': '^mmsource-1\.11\.[0-9]*-(git|hg)[0-9]*-(windows|linux|mac)\.(zip|tar\.gz)$',
            'updateFolders': [
                'addons/metamod/bin'
            ],
            'onlyUpdateExisting': []
        },
        'stripper': {
            'scheme': 'regex',
            'baseURL': 'https://www.bailopan.net/stripper/snapshots/1.2/',
            'regex': '^stripper-1\.2\.[0-9]*-(git|hg)[0-9]*-(windows|linux|mac)\.(zip|tar\.gz)$',
            'updateFolders': [
                'addons/stripper/bin'
            ],
            'onlyUpdateExisting': []
        },
        'tf2items': {
            'scheme': 'regex',
            'baseURL': 'https://builds.limetech.org/files/',
            'regex': '^tf2items-1\.6\.[0-9]*-(git|hg)[0-9]*-(windows|linux|mac)\.(zip|tar\.gz)$',
            'updateFolders': [
                'addons/sourcemod/extensions'
            ],
            'onlyUpdateExisting': []
        }
    }
