import os
import sys
import requests
import platform
import tarfile

from StringIO import StringIO
from bs4 import BeautifulSoup
from settings import getSettings
from versions import getVersion, changeVersion
from utils import query_yes_no
from zipfile import ZipFile



class Downloader(object):
    def __init__(self, deployment, basePath, fullInstall, skipConfirm, forceUpdate):
        self.basePath = basePath
        self.deployment = deployment
        self.fullInstall = fullInstall
        self.skipConfirm = skipConfirm
        self.forceUpdate = forceUpdate
        self._loadSettings()
        self.currentVersion = getVersion(deployment)


    def download(self):
        if self.basePath is None:
            self._print('Base path not set in settings.cfg')
            return

        if self.scheme == 'alliedmodders':
            fn = self._findLatestFile()
            if not self.forceUpdate:
                if fn == self.currentVersion:
                    self._print('Already up to date.')
                    return
            if not self.skipConfirm:
                if not query_yes_no('[%s] Download %s?' % (self.deployment, fn,)):
                    return
            url = '%s%s' % (self.baseURL, fn)
            data = self._download(url)
        else:
            url = self.targetURL
            data = self._download(self.targetURL)

        if fn.endswith('.tar.gz'):
            self._extractTar(data)
        elif fn.endswith('.zip'):
            self._extractZip(data)

        if self.scheme == 'alliedmodders':
            changeVersion(self.deployment, fn)


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


    def _findLatestFile(self):
        r = requests.get(self.baseURL)
        soup = BeautifulSoup(r.text)

        for link in sorted(soup.find_all('a'), reverse=True, key=lambda x: x.get('href')):
            href = link.get('href')
            if not href.startswith('%s-%s' % (self.filePrefix, self.targetVersion)):
                continue
            if platform.system().lower() in href:
                return href
        else:
            self._print('ERROR: No matching version found for your OS.')


    def _download(self, url):
        self._print('Fetching %s' % (url,))
        r = requests.get(url)
        return StringIO(r.content)


    def _downloadFile(self, filename):
        url = '%s%s' % (self.baseURL, filename)
        return self._download(url)


    def _print(self, s):
        print('[%s] %s' % (self.deployment, s))


    def _extractTar(self, f):
        with tarfile.open(fileobj=f) as tf:
            for member in tf.getmembers():
                filename = member.name

                if not self._checkUpdatable(filename):
                    continue

                self._print('(Extract) %s' % (filename,))
                tf.extract(member, self.basePath)


    def _extractZip(self, f):
        with ZipFile(f) as zf:
            for member in zf.infolist():
                filename = member.filename

                if not self._checkUpdatable(filename):
                    continue

                self._print('(Extract) %s' % (filename,))
                zf.extract(member, self.basePath)


    def _checkUpdatable(self, filename):
        if not self.fullInstall:
            for fn in self.updateFolders:
                if filename.startswith(fn):
                    break
            else:
                return False

            for fn in self.onlyUpdateExisting:
                if filename.startswith(fn):
                    if not os.path.exists(
                        os.path.join(self.basePath, filename)):
                        self._print('(Skip) %s' % (filename,))
                        return False

        return True
