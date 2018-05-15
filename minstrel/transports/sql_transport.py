from datetime import datetime
import collections
from sqlalchemy import create_engine, cast, Table, MetaData, and_, Column
from sqlalchemy.inspection import inspect
import sqlalchemy.exc
from .base_transport import Transport
from ..mock import Mock


class NoSuchColumnError(Exception):
    pass


class NoSuchTableError(Exception):
    pass


class SQLTransport(Transport):

    server = None
    host = None
    user = None
    password = None
    database = None

    @property
    def sql_url(self):
        return '{server}://{user}:{password}@{host}/{database}'.format(
            server=self.server,
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
        )

    def __init__(self, server, host, user, password, database):
        self.server = server
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def _setup_table(self, table_name):
        self.engine = create_engine(self.sql_url)
        meta = MetaData()

        try:
            table = Table(table_name, meta, autoload_with=self.engine)
        except sqlalchemy.exc.NoSuchTableError:
            raise NoSuchTableError(f'Table "{table_name}" does not exist.')

        return table

    def write(self, mock):
        config = mock.transport_configs['sql']
        table_name = config['table_name']

        columns = set()
        for obj in mock.objects:
            for key, value in obj.items():
                columns.add(key)

        table = self._setup_table(table_name)

        for column in columns:
            if not hasattr(table.c, column):
                raise NoSuchColumnError(f'Column "{column}" does not exist.')

        with self.engine.connect() as conn:
            for obj in mock.objects:
                try:
                    conn.execute(table.insert(), obj)
                except sqlalchemy.exc.IntegrityError as e:
                    if 'duplicate key' not in str(e):
                        raise
                    pks = inspect(table).primary_key

                    pk_columns = []
                    for pk in pks:
                        if isinstance(pk, Column):
                            pk_columns.append(pk)
                        else:
                            map(pk_columns.append, pk.columns.values())

                    pk_and = and_(*(
                        column == cast(obj[column.name], column.type)
                        for column in pk_columns
                    ))
                    conn.execute(
                        table.update().where(pk_and),
                        obj
                    )

            # PostgreSQL will not update a sequence after an `id` has been inserted, work around that:
            for col in table.columns:
                if not col.autoincrement:
                    continue
                print(f'Updating autoincrement for {col.name} in {table.name}: {table.name}_{col.name}_seq')
                value = conn.execute(f"""
                    SELECT max({col.name}) FROM {table.name}""").fetchone()[0]
                if value is not None:
                    value = int(value) + 1
                    conn.execute(f"""
                        ALTER SEQUENCE IF EXISTS {table.name}_{col.name}_seq
                        MINVALUE {value} START {value} RESTART {value}""")
            conn.execute('commit')

    def read(self, table_name):
        table = self._setup_table(table_name)
        base = {column.name: None for column in table.c}

        objects = []
        with self.engine.connect() as conn:
            results = conn.execute(table.select())
            for result in results:
                obj = base.copy()
                for key in obj:
                    value = result[key]
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    obj[key] = value
                objects.append(obj)

        return {
            'transports': {
                'sql': {
                    'table_name': table_name,
                },
            },
            'base': objects.pop(0),
            'derivatives': [{'merge': obj} for obj in objects],
        }
