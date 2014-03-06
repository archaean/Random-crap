import sqlalchemy

def create_engine(argv, options, database):
    db_type = argv[1]
    if db_type == 'sqlite':
        engine = create_sqlite_engine(options, database)
    elif db_type == 'mysql':
        engine = create_mysql_engine(options, database)
    else:
        raise Exception('Invalid database: '+db_type)
    return engine

def create_sqlite_engine(options, database):
    engine = sqlalchemy.create_engine('sqlite:///'+database+'.db')
    return engine

def create_mysql_engine(options, database):
    mysqld_op = options['mysqld']
    
    user = mysqld_op['user']
    password = mysqld_op['password']
    password = ':'+password if password else ''
    host = mysqld_op['host']

    mysql_connect = 'mysql://'+user+password+'@'+host   
    engine = sqlalchemy.create_engine(mysql_connect+'/'+database)

    try:
        engine.execute("select 1")
    except Exception as inst:
        #TODO logging
        print 'INFO: '+str(inst)
        print 'INFO: Creating database '+database
        preengine = sqlalchemy.create_engine(mysql_connect)
        preengine.execute("create database if not exists "+database)

    return engine
