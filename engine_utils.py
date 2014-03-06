import sqlalchemy

def create_mysql_engine(options):
    mysqld_op = options['mysqld']
    
    user = mysqld_op['user']
    password = mysqld_op['password']
    password = ':'+password if password else ''
    host = mysqld_op['host']

    engine = sqlalchemy.create_engine('mysql://'+user+password+'@'+host)
    return engine
