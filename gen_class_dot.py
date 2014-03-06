#!/usr/bin/python

import io
import sys, getopt
import engine_utils
from config_parser import get_options
from warhammer_model import get_classes_model
from sqlalchemy import MetaData

def main(argv):
   
    config_file = argv[0] 
    options = get_options(config_file)
    
    warhammerdb = options['classes']['warhammerdb']
    engine = engine_utils.create_mysql_engine(options, warhammerdb)
    metadata = MetaData()
    classes = get_classes_model(options, metadata)
    #  Figure out what create_all is for
    #  metadata.create_all(engine)

    #engine.execute("use "+warhammerdb)

    from sqlalchemy.sql import select
    from sqlalchemy import and_, or_, not_ 
    
    s = select([classes.c.class_name, classes.c.relation, classes.c.value])
    s = s.where(classes.c.relation =='Career Exits')

    conn = engine.connect()
    result = conn.execute(s).fetchall()

    print 'digraph Careers {'
    for row in result:
	    print '\t\"'+row[0]+'\" -> \"'+row[2]+'\";'
    print '}'

if __name__ == "__main__":
    main(sys.argv[1:])
