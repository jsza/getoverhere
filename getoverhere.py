 #!/usr/bin/python

from argparse import ArgumentParser
from getoverhere.downloader import Downloader



def main():
    parser = ArgumentParser()
    parser.add_argument('path',
                        help='Target path on disk.')
    parser.add_argument('deployments', nargs='*', help='Deployments.')
    parser.add_argument('-fi', '--full-install',
                        help='Overwrite all files.',
                        action='store_true')
    parser.add_argument('-sc', '--skip-confirm',
                        help='Skip confirmation for downloading files.',
                        action='store_true')
    parser.add_argument('-fu', '--force-update',
                        help='Force install if already up-to-date. '
                             'This should not be needed unless something went horribly wrong.',
                        action='store_true')
    args = parser.parse_args()
    basePath = args.path
    fullInstall = args.full_install
    skipConfirm = args.skip_confirm
    forceUpdate = args.force_update

    for deployment in args.deployments:
        Downloader(deployment, basePath, fullInstall, skipConfirm, forceUpdate).download()



if __name__ == '__main__':
    main()
