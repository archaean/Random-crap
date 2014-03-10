#!/usr/bin/python

import sys
import engine_utils
from arg_parser import parse_args
from config_parser import get_options
from warhammer_model import get_classes_model
from sqlalchemy import MetaData


def main(argv):
    opts, args = parse_args(argv[0], argv[1:])
    config_file = opts['configfile']
    db_type = opts['dbtype']
    options = get_options(config_file)

    warhammerdb = options['classes']['warhammerdb']
    engine = engine_utils.create_engine(db_type, options, warhammerdb)
    metadata = MetaData()
    classes = get_classes_model(options, metadata)

    generate_dot(engine, classes)


def generate_dot(engine, classes):
    from sqlalchemy.sql import select
    #from sqlalchemy import and_, or_, not_

    s = select([classes.c.class_name,
                classes.c.relation,
                classes.c.value,
                classes.c.modifier])
    s = s.where(classes.c.relation == 'Career Exits')

    conn = engine.connect()
    result = conn.execute(s).fetchall()

    print 'digraph Careers {'
    print """
    splines=ortho;
    sep="+25,25";
    overlap=scalexy;
    nodesep=0.6;
    node [fontsize=11];"""
    for row in result:
        print '\t\"' + row[0] + '\" -> \"' + row[2] + '\"' + ' [ taillabel=\"' + row[3] + '\" ];'
    print '}'


if __name__ == "__main__":
    main(sys.argv)
