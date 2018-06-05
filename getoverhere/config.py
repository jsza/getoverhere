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
            'baseURL': 'https://www.sourcemod.net/smdrop/1.9/',
            # 'regex': '^sourcemod-1\.8\.[0-9]*-git[0-9]*-(windows|linux|mac)\.(zip|tar\.gz)$',
            'regex': '^sourcemod-1\.9\.0-git6235-(windows|linux|max)\.(zip|tar\.gz)$',
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
        },
        'collisionhook': {
            'scheme': 'generic',
            'URL': 'https://bitbucket.org/VoiDeD/collisionhook/downloads/collisionhook-0.2.zip',
            'updateFolders': [
                'sourcemod/extensions',
                'sourcemod/gamedata',
                'sourcemod/scripting'
            ],
            'onlyUpdateExisting': [],
            'appendPath': 'addons'
        },
        'dhooks': {
            'scheme': 'regex',
            'baseURL': 'http://users.alliedmods.net/~drifter/builds/dhooks/2.2/',
            'regex': '^dhooks-2.2.0-hg126-(windows|linux|mac)\.tar.gz$',
            'updateFolders': [
                'addons/sourcemod/extensions',
                'addons/sourcemod/gamedata',
                'addons/sourcemod/scripting'
            ],
            'onlyUpdateExisting': []
        }
    }
