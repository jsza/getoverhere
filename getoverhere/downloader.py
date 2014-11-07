import os
import requests
import platform
import tarfile

from StringIO import StringIO
from bs4 import BeautifulSoup
from utils import query_yes_no
from zipfile import ZipFile

from getoverhere.config import getVersion, changeVersion, getSettings



def getDownloader(deployment, basePath, fullInstall, skipConfirm, forceUpdate,
                  verbose):
    settings = getSettings()

    try:
        ours = settings[deployment]
    except KeyError:
        print('[%s] \'%s\' is not a supported deployment.' % (deployment, deployment))
        return None

    scheme = ours['scheme']
    if scheme == 'alliedmodders':
        return AlliedModdersDownloader(ours, basePath, fullInstall,
                                       skipConfirm, forceUpdate, verbose)
    elif scheme == 'generic':
        return GenericDownloader(ours, basePath, fullInstall, skipConfirm,
                                 forceUpdate, verbose)
    else:
        print('[%s] \'%s\' scheme is not supported.' % (deployment, scheme))
        return None


    self.scheme = ours['scheme']
    self.targetVersion = ours['version']
    self.filePrefix = ours['filePrefix']
    self.baseURL = '%s%s/' % (
        ours['baseURL'], self.targetVersion)
    self.updateFolders = ours['updateFolders']
    self.onlyUpdateExisting = ours['onlyUpdateExisting']



class Downloader(object):
    def __init__(self, settings, basePath, fullInstall, skipConfirm,
                 forceUpdate, verbose):
        self.deployment = settings['deployment']
        self.basePath = basePath
        self.settings = settings
        self.fullInstall = fullInstall
        self.skipConfirm = skipConfirm
        self.forceUpdate = forceUpdate
        self.verbose = verbose


    def _loadSettings(self):
        settings = getSettings()
        ours = settings[self.deployment]
        self.scheme = ours['scheme']
        self.targetVersion = ours['version']
        self.filePrefix = ours['filePrefix']
        self.baseURL = '%s%s/' % (
            ours['baseURL'], self.targetVersion)
        self.updateFolders = ours['updateFolders']
        self.onlyUpdateExisting = ours['onlyUpdateExisting']


    def _download(self, url):
        self._print('Fetching %s' % (url,))
        r = requests.get(url)
        return StringIO(r.content)


    def _print(self, s):
        print('[%s] %s' % (self.deployment, s))


    def _printVerbose(self, s):
        if self.verbose:
            self._print(s)


    def _extractTar(self, f):
        with tarfile.open(fileobj=f) as tf:
            for member in tf.getmembers():
                filename = member.name

                if not self._checkUpdatable(filename):
                    continue

                self._printVerbose('(Extract) %s' % (filename,))
                tf.extract(member, self.basePath)


    def _extractZip(self, f):
        with ZipFile(f) as zf:
            for member in zf.infolist():
                filename = member.filename

                if not self._checkUpdatable(filename):
                    continue

                self._printVerbose('(Extract) %s' % (filename,))
                zf.extract(member, self.basePath)



class AlliedModdersDownloader(Downloader):
    def download(self):
        if self.basePath is None:
            self._print('Base path not set in settings.cfg')
            return

        fn = self._findLatestFile()
        if not self.forceUpdate:
            if fn == getVersion(self.deployment):
                self._print('Already up to date.')
                return
        if not self.skipConfirm:
            if not query_yes_no('[%s] Download %s?' % (self.deployment, fn,)):
                return
        url = '%s%s' % (self.settings['baseURL'], fn)
        data = self._download(url)

        if fn.endswith('.tar.gz'):
            self._extractTar(data)
        elif fn.endswith('.zip'):
            self._extractZip(data)

        changeVersion(self.deployment, fn)


    def _findLatestFile(self):
        r = requests.get(self.baseURL)
        soup = BeautifulSoup(r.text)

        for link in sorted(soup.find_all('a'), reverse=True, key=lambda x: x.get('href')):
            href = link.get('href')
            if not href.startswith('%s-%s' % (self.settings['filePrefix'],
                                              self.settings['targetVersion'])):
                continue
            if platform.system().lower() in href:
                return href
        else:
            self._print('ERROR: No matching version found for your OS.')


    def _checkUpdatable(self, filename):
        if not self.fullInstall:
            for fn in self.settings['updateFolders']:
                if filename.startswith(fn):
                    break
            else:
                return False

            for fn in self.settings['onlyUpdateExisting']:
                if filename.startswith(fn):
                    if not os.path.exists(
                        os.path.join(self.settings['basePath'], filename)):
                        self._printVerbose('(Skip) %s' % (filename,))
                        return False

        return True



class GenericDownloader(Downloader):
    def download(self):
        if self.basePath is None:
            self._print('Base path not set in settings.cfg')
            return

        url = self.targetURL
        data = self._download(self.settings['targetURL'])

        if url.endswith('.tar.gz'):
            self._extractTar(data)
        elif url.endswith('.zip'):
            self._extractZip(data)
