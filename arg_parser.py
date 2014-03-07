import sys, getopt

_default_opt_def = [("h","--help",None,False, lambda x : sys.exit(2)),
                    ("c:","--config=","configfile",True),
                    ("d:","--db=","database",True)
                   ]

def dictify(opt_def):
    return [dict(short=i[0], 
                 long=i[1], 
                 arg_name=i[2], 
                 req=i[3],
                 post=(i[4] if len(i) > 4 else None)
                ) 
            for i in opt_def]

def parse_args(script, argv, opt_def=_default_opt_def):
    dict_opt_def = dictify(opt_def)
    short_op = reduce(lambda x,y: x+y, 
                      [x['short'] for x in dict_opt_def])
    print short_op
    long_op = [x['long'] for x in dict_opt_def]
    print long_op
    try:
        opts, args = getopt.getopt(argv,short_op,long_op)
    except getopt.GetoptError:
        print script + reduce(lambda x,y: x+y,
                              [' -{short} <{arg_name}>'.format(**x) 
                               for x in dict_opt_def if x['req']])
        sys.exit(2)
    
    options = dict()
    print opts
    print args
    for opt, arg in opts:
        for opt_def in dict_opt_def:
            print opt +" in " +opt_def['short']+" or "+opt_def['short']
            if opt in (opt_def['short'], opt_def['long']):
                options[opt_def['arg_name']]=arg
                if opt_def['post']:
                    print opt_def['post']
                    opt_def['post']()
    
    return options

if __name__ == "__main__":
    print parse_args(sys.argv[0], sys.argv[1:], _default_opt_def)
