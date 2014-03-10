"""
>>> argv = ['arg_parser.py','-c','warhammer.ini','-d','sqlite']
>>> parse_args(argv[0],argv[1:])
({'dbtype': 'sqlite', 'configfile': 'warhammer.ini'}, [])
"""

import sys
import getopt

_default_opt_def = [("c", "config", "configfile", True),
                    ("d", "db", "dbtype", True)]


def dictify(opt_def):
    """
    >>> dictify(_default_opt_def)
    [{'req': True, 'arg_name': 'configfile', 'long': 'config', 'short': 'c'}, {'req': True, 'arg_name': 'dbtype', 'long': 'db', 'short': 'd'}]
    >>> dictify([("the","wrong","len")])
    Traceback (most recent call last):
    ...
    IndexError: tuple index out of range
    """
    return [dict(short=i[0],
                 long=i[1],
                 arg_name=i[2],
                 req=i[3],)
            for i in opt_def]


def parse_args(script, argv, opt_def=_default_opt_def):
    """
    >>> parse_args('script.py', ['-h'])
    Traceback (most recent call last):
    ...
    SystemExit: 0
    >>> parse_args('script.py', ['-c', 'config', '--db=stuff'])
    ({'dbtype': 'stuff', 'configfile': 'config'}, [])
    >>> parse_args('script.py', ['--notarealopt'])
    Traceback (most recent call last):
    ...
    SystemExit: 2
    """
    dict_opt_def = dictify(opt_def)
    short_op = reduce(lambda x, y: x + y,
                      [x['short'] + (':' if x['req'] else '')
                       for x in dict_opt_def])
    short_op = '-h' + short_op
    long_op = [x['long'] + ('=' if x['req'] else '') for x in dict_opt_def]
    #long_op = long_op.insert(0,'--help')

    help = script + reduce(lambda x, y: x + y,
                           [' -{short} <{arg_name}>'.format(**x)
                            for x in dict_opt_def if x['req']])

    try:
        opts, args = getopt.getopt(argv, short_op, long_op)
    except getopt.GetoptError:
        print help
        sys.exit(2)

    options = dict()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print help
            sys.exit(0)
        for opt_def in dict_opt_def:
            if opt in ('-' + opt_def['short'], '--' + opt_def['long']):
                options[opt_def['arg_name']] = arg

    return options, args

if __name__ == "__main__":
    parse_args(sys.argvi[0], sys.argv[1:])
