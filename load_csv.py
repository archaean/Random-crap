import csv
import engine_utils
import sys
from config_parser import get_options
from sqlalchemy import MetaData
from warhammer_model import get_classes_model

def main (argv):
    config_file = argv[0]
    options = get_options(config_file)

    warhammerdb = options['classes']['warhammerdb']
    engine = engine_utils.create_engine(argv, options, warhammerdb)
    metadata = MetaData(bind=engine)
    table = get_classes_model(options, metadata)
    
    #create table if it doesn't exist and a truncate
    metadata.create_all(engine)
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
    main(sys.argv[1:])
