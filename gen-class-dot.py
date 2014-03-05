import ConfigParser
import io
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = MetaData()
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read('warhammer.ini')

classes_table = config.get("classes","classes_csv")
classes = Table(classes_table, metadata, Column('class', String), Column('relation', String), Column('value', String), Column('modifier', String))

user = config.get("mysqld","user")
password = config.get("mysqld","password")
if password:
	password = ':'+password
host = config.get("mysqld","host")
engine = sqlalchemy.create_engine('mysql://'+user+password+'@'+host)

warhammerdb = config.get("classes","warhammerdb")
engine.execute("use "+warhammerdb)

metadata.create_all(engine)
from sqlalchemy.sql import select

s = select([classes])
conn = engine.connect()
result = conn.execute(s)
for row in result:
	print row
