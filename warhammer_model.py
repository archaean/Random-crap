from sqlalchemy import Table, Column, Integer, String, ForeignKey

def get_classes_model(options, metadata):
    """
    >>> from config_parser import get_options
    >>> from sqlalchemy import MetaData
    >>> options = get_options('warhammer.ini.example')
    >>> metadata = MetaData()
    >>> get_classes_model(options, metadata)
    Table('classes_csv', MetaData(bind=None), Column('class_name', String(length=50), table=<classes_csv>), Column('relation', String(length=50), table=<classes_csv>), Column('value', String(length=50), table=<classes_csv>), Column('modifier', String(length=50), table=<classes_csv>), schema=None)
    """
    classes_table = options['classes']['classes_csv']
    classes = Table(classes_table, metadata,
        Column('class_name', String(50)), Column('relation', String(50)),
        Column('value', String(50)), Column('modifier', String(50)))

    return classes
