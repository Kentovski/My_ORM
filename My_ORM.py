# /usr/bin/python3

#MELNIKOV ILYA

import MySQLdb
import MySQLdb.cursors


class AbstractModel:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        insert(self)


class DbField:

    length = None


class TextField(DbField):

    def __init__(self, length):
        self.length = length


class IntegerField(DbField):
    pass


class FloatField(DbField):
    pass


class BooleanField(DbField):
    pass


def get_connection():
    connection = MySQLdb.connect(user='',
                                 passwd='',
                                 db='',
                                 cursorclass=MySQLdb.cursors.DictCursor)
    return connection


def migrate(model_class):
    connection = get_connection()
    cursor = connection.cursor()
    class_name = model_class.__class__.__name__.lower()
    fields = ''

    for field in model_class.__dir__():
        field_name = getattr(model_class, field)
        if isinstance(field_name, DbField):
            type_data = field_name.__class__.__name__.upper()
            field_length = getattr(field_name, 'length')
            fields += ' {} {}({}),'.format(field, type_data, field_length)

    query = 'CREATE TABLE IF NOT EXISTS {} (id INT(10) AUTO_INCREMENT PRIMARY KEY, {});'.format(class_name, fields[:-1])
    cursor.execute(query)


def insert(instance):
    connection = get_connection()
    cursor = connection.cursor()
    instance_name = instance.__class__.__name__.lower()
    values = ''
    fields = ''

    for field in instance.__dir__():
        field_name = getattr(instance.__class__, field)
        if isinstance(field_name, DbField):
            fields += ' ' + field + ','
            values += " '" + str(getattr(instance, field)) + "',"

    query = "INSERT INTO {} ({}) VALUES ({})".format(instance_name, fields[1:-1], values[1:-1])
    cursor.execute(query)
    connection.commit()


def select(model_class, **kwargs):
    connection = get_connection()
    cursor = connection.cursor()
    model_name = model_class.__name__.lower()
    where = ''
    filters = {
        '__gt': ' > ',
        '__gte': ' >= ',
        '__lt': ' < ',
        '__lte': ' <= '
    }

    if kwargs:
        for key, value in kwargs.items():
            if "__" in key:
                filt = filters[key[key.find("_"):]]
                key = key[:key.find("_")]
            else:
                filt = " = "
            where += key + "{}" "'{}'".format(filt, value) + " AND "
            where += "{}{}'{}'  AND ".format(key, filt, value)
        where = where[:len(where) - 4]
        query = "SELECT * FROM {} WHERE {}".format(model_name, where)
    else:
        query = "SELECT * FROM {}".format(model_name)
    cursor.execute(query)
    return cursor.fetchall()