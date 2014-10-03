import os
import json



def getSettings():
    path = os.path.join(os.getcwd(), 'settings.cfg')
    if not os.path.exists(path):
        settings = {
            'basePath': None,
            'sourcemod': {
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
                'baseURL': 'http://www.metamodsource.net/mmsdrop/',
                'version': '1.10',
                'filePrefix': 'mmsource',
                'updateFolders': [
                    'addons/metamod/bin'
                ],
                'onlyUpdateExisting': []
            },
            'stripper': {
                'baseURL': 'http://www.bailopan.net/stripper/snapshots/',
                'version': '1.2',
                'filePrefix': 'stripper',
                'updateFolders': [
                    'addons/stripper/bin'
                ],
                'onlyUpdateExisting': []
            }
        }
        with file(path, 'wb') as f:
            json.dump(settings, f, indent=4)
    else:
        with open(path) as f:
            settings = json.load(f)
    return settings
