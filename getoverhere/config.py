import json
import os



def getVersion(basePath, deployment):
    path = os.path.join(basePath, '.goh_versions')
    if not os.path.exists(path):
        versions = {}
    else:
        with open(path) as f:
            versions = json.load(f)
    return versions.get(deployment)



def changeVersion(basePath, deployment, value):
    path = os.path.join(basePath, '.goh_versions')

    if os.path.exists(path):
        with open(path) as f:
            versions = json.load(f)
    else:
        versions = {}

    versions[deployment] = value
    with open(path, 'w') as f:
        json.dump(versions, f)



def getSettings():
    return {
        'sourcemod': {
            'scheme': 'regex',
            'baseURL': 'https://www.sourcemod.net/smdrop/1.8/',
            'regex': '^sourcemod-1\.8\.[0-9]*-git[0-9]*-(windows|linux|mac)\.(zip|tar\.gz)$',
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
            'regex': '^mmsource-1\.11\.[0-9]*-git[0-9]*-(windows|linux|mac)\.(zip|tar\.gz)$',
            'updateFolders': [
                'addons/metamod/bin'
            ],
            'onlyUpdateExisting': []
        },
        'stripper': {
            'scheme': 'regex',
            'baseURL': 'https://www.bailopan.net/stripper/snapshots/1.2/',
            'regex': '^stripper-1\.2\.[0-9]*-git[0-9]*-(windows|linux|mac)\.(zip|tar\.gz)$',
            'updateFolders': [
                'addons/stripper/bin'
            ],
            'onlyUpdateExisting': []
        },
        'tf2items': {
            'scheme': 'regex',
            'baseURL': 'https://builds.limetech.io/?p=tf2items',
            'regex': '^.*tf2items-1\.6\.[0-9]*-hg[0-9]*-(windows|linux|mac)\.(zip|tar\.gz)$',
            'updateFolders': [
                'addons/sourcemod/extensions'
            ],
            'onlyUpdateExisting': []
        },
        'accelerator': {
            'scheme': 'regex',
            'baseURL': 'https://builds.limetech.io/?p=accelerator',
            'regex': '^.*accelerator-2\.3\.[0-9]*-git[0-9]*-[a-zA-Z0-9_]{7}-(windows|linux|mac)\.(zip|tar\.gz)$',
            'updateFolders': [
                'addons/sourcemod/extensions',
                'addons/sourcemod/gamedata'
            ],
            'onlyUpdateExisting': []
        },
        'steamtools': {
            'scheme': 'regex',
            'baseURL': 'https://builds.limetech.io/?p=steamtools',
            'regex': '^.*steamtools-0\.10\.[0-9]*-git.*-(windows|linux|mac)\.(zip|tar\.gz)$',
            'updateFolders': [
                'addons/sourcemod/extensions'
            ],
            'onlyUpdateExisting': []
        }
    }
