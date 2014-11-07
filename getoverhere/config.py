import os
import json

from platform import system



if system() == 'Linux':
    configPath = os.path.join('~', '.config', 'getoverhere')
else:
    configPath = os.getcwd()

if not os.path.exists(configPath):
    os.makedirs(configPath)



def getVersion(deployment):
    path = os.path.join(configPath, 'versions.cfg')
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
    path = os.path.join(configPath, 'versions.cfg')

    with open(path) as f:
        versions = json.load(f)

    versions[deployment] = value
    with open(path, 'w') as f:
        json.dump(versions, f)



def getSettings():
    path = os.path.join(configPath, 'settings.cfg')
    if not os.path.exists(path):
        settings = {
            'basePath': None,
            'sourcemod': {
                'scheme': 'alliedmodders',
                'baseURL': 'http://www.sourcemod.net/smdrop/',
                'version': '1.6',
                'filePrefix': 'sourcemod',
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
                'scheme': 'alliedmodders',
                'baseURL': 'http://www.metamodsource.net/mmsdrop/',
                'version': '1.10',
                'filePrefix': 'mmsource',
                'updateFolders': [
                    'addons/metamod/bin'
                ],
                'onlyUpdateExisting': []
            },
            'stripper': {
                'scheme': 'alliedmodders',
                'baseURL': 'http://www.bailopan.net/stripper/snapshots/',
                'version': '1.2',
                'filePrefix': 'stripper',
                'updateFolders': [
                    'addons/stripper/bin'
                ],
                'onlyUpdateExisting': []
            },
            'tf2items': {
                'scheme': 'generic',
                'URL': 'http://hg.limetech.org/projects/tf2items/tf2items_release/archive/tip.zip',
                'basePath': 'addons/sourcemod/',
                'updateFolders': [],
                'onlyUpdateExisting': []
            }
        }
        with file(path, 'wb') as f:
            json.dump(settings, f, indent=4)
    else:
        with open(path) as f:
            settings = json.load(f)
    return settings
