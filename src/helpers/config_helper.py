import yaml


class ConfigHelper(object):

    @staticmethod
    def parse_config(path: str):
        stream = open(path, 'r')
        return yaml.load(stream,yaml.SafeLoader)
