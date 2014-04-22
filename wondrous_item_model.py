from sqlalchemy import Table, Column, String


def get_classes_model(options, metadata):
    """
    >>> from config_parser import get_options
    >>> from sqlalchemy import MetaData
    >>> options = get_options('warhammer.ini.example')
    >>> metadata = MetaData()
    """
    classes_table = options['classes']['classes_csv']
    classes = Table(classes_table, metadata,
                    Column('Item', String(150)),
                    Column('Spell', String(150)))

    return classes
