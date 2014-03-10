"""
>>> from config_parser import get_options
>>> options = get_options('warhammer.ini.example')
>>> create_engine('sqlite', options, None)
Engine(sqlite://)
>>> create_engine('sqlite', options, 'huh')
Engine(sqlite:///huh.db)
>>> create_engine('invalid', options, 'some')
Traceback (most recent call last):
...
Exception: Invalid database: invalid
>>> create_engine('mysql', options, 'what')
Traceback (most recent call last):
...
OperationalError: (OperationalError) (1045, "Access denied for user 'user'@'localhost' (using password: YES)") None None
"""

import sqlalchemy


def create_engine(db_type, options, database):
    if db_type == 'sqlite':
        engine = create_sqlite_engine(options, database)
    elif db_type == 'mysql':
        engine = create_mysql_engine(options, database)
    else:
        raise Exception('Invalid database: ' + db_type)
    return engine


def create_sqlite_engine(options, database):
    database_sqlite = '/' + database + '.db' if database else ''
    engine = sqlalchemy.create_engine('sqlite://' + database_sqlite)
    return engine


def create_mysql_engine(options, database):
    mysqld_op = options['mysqld']
    user = mysqld_op['user']
    password = mysqld_op['password']
    password = ':' + password if password else ''
    host = mysqld_op['host']

    mysql_connect = 'mysql://' + user + password + '@' + host
    engine = sqlalchemy.create_engine(mysql_connect + '/' + database)

    try:
        engine.execute("select 1")
    except Exception as inst:
        #TODO logging
        print 'INFO: ' + str(inst)
        print 'INFO: Creating database ' + database
        preengine = sqlalchemy.create_engine(mysql_connect)
        preengine.execute("create database if not exists " + database)

    return engine
