from sqlalchemy import Table, Column, Integer, String, ForeignKey

def get_classes_model(options, metadata):
    classes_table = options['classes']['classes_csv']
    classes = Table(classes_table, metadata,
        Column('class_name', String(50)), Column('relation', String(50)),
        Column('value', String(50)), Column('modifier', String(50)))

    return classes
