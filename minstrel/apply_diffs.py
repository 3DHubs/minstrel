from logging import getLogger
import json
from typing import Iterable
import kombu
from sqlalchemy import create_engine, Table, MetaData
import sqlalchemy.exc
import jsonpatch

logger = getLogger(__name__)


class NoSuchColumnError(Exception):
    pass


class NoSuchTableError(Exception):
    pass


def patcher(base: dict, derivatives: Iterable[Iterable[dict]]):
    yield base
    for derivative in derivatives:
        yield jsonpatch.JsonPatch(derivative).apply(base)


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
            if isinstance(value, dict):
                logger.warning(f'Nested resources are not supported at {key}')
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
        conn.execute(table.insert(), dicts)
