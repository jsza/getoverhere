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
args = parser.parse_args()
fullInstall = args.full_install
skipConfirm = args.skip_confirm

for deployment in args.deployments:
    Downloader(deployment, fullInstall, skipConfirm).download()
