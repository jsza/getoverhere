from __future__ import division

import os
import platform
import tarfile
from StringIO import StringIO
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup

from getoverhere.config import changeVersion, getSettings, getVersion
from getoverhere.utils import query_yes_no, splitPath


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
        return AlliedModdersDownloader(deployment, ours, basePath, fullInstall,
                                       skipConfirm, forceUpdate, verbose)
    elif scheme == 'generic':
        return GenericDownloader(deployment, ours, basePath, fullInstall,
                                 skipConfirm, forceUpdate, verbose)
    else:
        print('[%s] \'%s\' scheme is not supported.' % (deployment, scheme))
        return None



class Downloader(object):
    def __init__(self, deployment, settings, basePath, fullInstall,
                 skipConfirm, forceUpdate, verbose):
        self.deployment = deployment
        self.basePath = basePath
        self.settings = settings
        self.fullInstall = fullInstall
        self.skipConfirm = skipConfirm
        self.forceUpdate = forceUpdate
        self.verbose = verbose


    def _download(self, url):
        self._print('Fetching %s' % (url,))
        r = requests.get(url)
        return StringIO(r.content)


    def _print(self, s):
        print('[%s] %s' % (self.deployment, s))


    def _printVerbose(self, s):
        if self.verbose:
            self._print(s)


    def _extractTar(self, f, basePath=None, depth=0):
        with tarfile.open(fileobj=f) as tf:
            for member in tf.getmembers():
                if depth > 0:
                    member.name = os.path.join(
                        *splitPath(member.name)[depth:])

                self._extract(tf, member, member.name, basePath)


    def _extractZip(self, f, basePath=None, depth=0):
        with ZipFile(f) as zf:
            for member in zf.infolist():
                if depth > 0:
                    member.filename = os.path.join(
                        *splitPath(member.filename)[depth:])

                self._extract(zf, member, member.filename, basePath)


    def _extract(self, zf, member, filename, basePath):
        if filename in self.settings.get('ignoreFiles', []):
            self._printVerbose('(Ignore) %s' % filename)
            return

        if not self._checkUpdatable(filename):
            self._printVerbose('(Skip) %s' % filename)
            return

        self._printVerbose('(Extract) %s' % (filename,))

        if basePath is not None:
            path = os.path.join(self.basePath, basePath)
        else:
            path = basePath

        zf.extract(member, path)


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



class AlliedModdersDownloader(Downloader):
    def download(self):
        if self.basePath is None:
            self._print('Base path not set in settings.cfg')
            return

        fn = self._findLatestFile()
        if fn is None:
            return

        if not self.forceUpdate:
            if fn == getVersion(self.basePath, self.deployment):
                self._print('Already up to date.')
                return
        if not self.skipConfirm:
            if not query_yes_no('[%s] Download %s?' % (self.deployment, fn,)):
                return

        url = '%s%s' % (self._getBaseURL(), fn)

        data = self._download(url)

        if fn.endswith('.tar.gz'):
            self._extractTar(data)
        elif fn.endswith('.zip'):
            self._extractZip(data)

        changeVersion(self.basePath, self.deployment, fn)

        self._print('Success!')


    def _getBaseURL(self):
        return '%s%s/' % (self.settings['baseURL'], self.settings['version'])


    def _findLatestFile(self):
        r = requests.get(self._getBaseURL())
        soup = BeautifulSoup(r.text)

        for link in sorted(soup.find_all('a'), reverse=True, key=lambda x: x.get('href')):
            href = link.get('href')
            if not href.startswith('%s-%s' % (self.settings['filePrefix'],
                                              self.settings['version'])):
                print(href)
                continue
            if platform.system().lower() in href:
                return href
        else:
            self._print('ERROR: No matching version found for your OS.')



class GenericDownloader(Downloader):
    def download(self):
        if self.basePath is None:
            self._print('Base path not set in settings.cfg')
            return

        url = self.settings['URL']
        data = self._download(url)

        if url.endswith('.tar.gz'):
            self._extractTar(data, self.settings['basePath'])
        elif url.endswith('.zip'):
            self._extractZip(data, self.settings['basePath'], 1)

        self._print('Success!')
