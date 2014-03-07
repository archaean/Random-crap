from ConfigParser import RawConfigParser

def get_options(config_file):
    """
    >>> get_options('warhammer.ini.example')
    OrderedDict([('mysqld', OrderedDict([('__name__', 'mysqld'), ('user', 'user'), ('password', 'password'), ('host', 'localhost')])), ('classes', OrderedDict([('__name__', 'classes'), ('warhammerdb', 'warhammer'), ('csv_file', 'classes.csv'), ('classes_csv', 'classes_csv')]))])
    """
    config = RawConfigParser(allow_no_value=True)
    config.read(config_file)
    return config._sections
