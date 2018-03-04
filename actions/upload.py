
class UploadHandler(object):

    def __init__(self, subcommand):
        self.subcommand = subcommand

    def _init_args(self, subparser):
        subparser.add_parser(self.subcommand)

    def run(self, args):
        pass
