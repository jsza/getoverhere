from argparse import ArgumentParser
from downloader import Downloader



parser = ArgumentParser()
parser.add_argument('deployments', nargs='*', help='Deployments.')
parser.add_argument('-fi', '--full-install',
                    help='Download and overwrite all files.',
                    action='store_true')
parser.add_argument('-sc', '--skip-confirm',
                    help='Skip confirmation for downloading files.',
                    action='store_true')
parser.add_argument('-fu', '--force-update',
                    help='Force install if already up-to-date. '
                         'This should not be needed unless something went horrible wrong.',
                    action='store_true')
args = parser.parse_args()
fullInstall = args.full_install
skipConfirm = args.skip_confirm
forceUpdate = args.force_update

for deployment in args.deployments:
    Downloader(deployment, fullInstall, skipConfirm, forceUpdate).download()
