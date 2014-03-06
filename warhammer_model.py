from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

def get_classes_model(options):
    metadata = MetaData()
    classes_table = options['classes']['classes_csv']
    classes = Table(classes_table, metadata,
        Column('class_name', String), Column('relation', String),
        Column('value', String), Column('modifier', String))

    return metadata, classes
