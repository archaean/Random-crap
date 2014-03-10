import csv
import engine_utils
import sys
from arg_parser import parse_args
from config_parser import get_options
from sqlalchemy import MetaData
from warhammer_model import get_classes_model

def main (argv):
    opts, args = parse_args(argv[0],argv[1:])
    db_type = opts['dbtype']
    config_file = opts['configfile']
    options = get_options(config_file)

    warhammerdb = options['classes']['warhammerdb']
    engine = engine_utils.create_engine(db_type, options, warhammerdb)
    metadata = MetaData(bind=engine)
    table = get_classes_model(options, metadata)
    
    #create table if it doesn't exist and a truncate
    metadata.create_all(engine)
    load_csv(engine, table, options, opts)    


def load_csv(engine, table, options, opts):
    db_type = opts['dbtype']
    if db_type == 'sqlite':
        engine.execute('delete from '+str(table))
        engine.execute('vacuum')
    else:
        engine.execute('truncate table '+str(table))

    #load csv_file
    csv_file = options['classes']['csv_file']
    with open(csv_file) as f:
        #first line is header
        cf = csv.DictReader(f, delimiter=',')
        conn = engine.connect()
        for row in cf:
            ins = table.insert().values(**row)
            conn.execute(ins)

if __name__ == "__main__":
    main(sys.argv)
