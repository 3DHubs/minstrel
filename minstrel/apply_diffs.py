import collections
from logging import getLogger
from typing import Iterable
import json

from sqlalchemy import create_engine, cast, Table, MetaData, and_, Column
from sqlalchemy.inspection import inspect
import jsonpatch
import kombu
import sqlalchemy.exc

logger = getLogger(__name__)


class NoSuchColumnError(Exception):
    pass


class NoSuchTableError(Exception):
    pass


def patch(base: dict, patches: Iterable[dict]):
    return jsonpatch.JsonPatch(patches).apply(base)


def amqp_applier(amqp_url: str, exchange_name: str, routing_key: str,
                 dicts: Iterable[dict]):
    connection = kombu.Connection(amqp_url)
    exchange = kombu.Exchange(exchange_name, type='topic')
    producer = connection.Producer(exchange=exchange)

    for dct in dicts:
        producer.publish(
            json.dumps(dct),
            exchange=exchange,
            routing_key=routing_key,
        )


def sql_applier(sql_url: str, table_name: str, dicts: Iterable[dict]):
    dicts = list(dicts)

    columns = set()
    for dct in dicts:
        for key, value in dct.items():
            if isinstance(value, dict) or isinstance(value, list):
                logger.warning(
                    f'Nested resources are not supported for column "{key}".'
                    ' Continuing anyway.'
                )
            columns.add(key)

    engine = create_engine(sql_url)
    meta = MetaData()

    try:
        table = Table(table_name, meta, autoload_with=engine)
    except sqlalchemy.exc.NoSuchTableError:
        raise NoSuchTableError(f'Table "{table_name}" does not exist.')

    for column in columns:
        if not hasattr(table.c, column):
            raise NoSuchColumnError(f'Column "{column}" does not exist.')

    with engine.connect() as conn:
        for dct in dicts:
            try:
                conn.execute(table.insert(), dct)
            except sqlalchemy.exc.IntegrityError as e:
                pks = inspect(table).primary_key

                pk_columns = []
                for pk in pks:
                    if isinstance(pk, Column):
                        pk_columns.append(pk)
                    else:
                        map(pk_columns.append, pk.columns.values())

                pk_and = and_(*(
                    column == cast(dct[column.name], column.type)
                    for column in pk_columns
                ))
                conn.execute(
                    table.update().where(pk_and),
                    dct
                )
        conn.execute('commit')
