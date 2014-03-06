from ConfigParser import RawConfigParser

def get_options(config_file):
    config = RawConfigParser(allow_no_value=True)
    config.read(config_file)
    return config._sections
