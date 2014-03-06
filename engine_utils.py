import sqlalchemy

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
