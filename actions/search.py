from backend import GDrive
from os import path

class UploadHandler(object):

    def __init__(self, subcommand):
        self.subcommand = subcommand
        self.backend = GDrive.DriveStorage()

    def _init_args(self, subparser):
        parser = subparser.add_parser(self.subcommand)

        parser.add_argument('files', nargs='+', help='Files you want to upload.')

    def run(self, args):
        for f in args.files:
            if not path.isfile(f):
                print('{} is not a valid file.'.format(f))
                continue
            self.backend.write(f)
            print('{} has been uploaded'.format(f))
