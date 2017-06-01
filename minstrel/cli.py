import json
import click
from .generate_diffs import differ
from .config import Config
from .mock import Mock
from .transports.sql_transport import (
    NoSuchColumnError,
    NoSuchTableError,
)
from . import transports


def _read_config_into_kwargs(config, kwargs):
    transport_kwargs = kwargs.copy()
    if config is not None:
        with open(config, 'r') as f:
            conf_data = json.load(f)

        if 'sql' in conf_data['transports']:
            transport_kwargs.update(conf_data['transports']['sql'])

    arg_defaults = {
        'server': 'postgresql',
        'host': 'localhost',
        'user': 'postgres',
        'password': '',
        'database': 'postgres',
    }
    for name, default in arg_defaults.items():
        if kwargs[name] is not None:
            transport_kwargs[name] = kwargs[name]

    return transport_kwargs


@click.group()
def minstrel():
    """Generate and apply mocked objects."""
    pass


@minstrel.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('config')
@click.pass_context
def load(ctx, config):
    """Run Minstrel imports according to config file."""
    with open(config, 'r') as f:
        data = json.load(f)
    conf = Config(data)

    while True:
        try:
            arg = ctx.args.pop(0)
        except IndexError:
            break

        if not arg.startswith('--'):
            click.echo(f'Argument {arg} not understood.', err=True)
            return

        transport, setting = arg[2:].split('-', 1)
        value = ctx.args.pop(0)
        conf.transport_settings[transport][setting] = value

    conf.setup()
    conf.run()


@minstrel.command()
@click.argument('source')
@click.argument('target')
@click.option('--indent', type=int, default=2,
              help='Spaces of indentation used in output JSON.')
def generate(source, target, indent):
    """
    Generate Minstrel mock file from a list of JSON objects.

    PLEASE NOTE: this is an alpha implementation and it's mostly broken. No
    promises.

    Reads from JSON file source (should contain a list of objects) and stores
    Minstrel-readable JSON to target. Will parse the objects to find all
    distinct types of objects and create a base object and patches out of them.

    NB: it's recommended that you manually check and adjust the output.
    """
    with open(source, 'r') as f:
        data = json.load(f)

    default, patches = differ(data)

    output = {
        'base': default,
        'derivatives': [{'patches': list(diff)} for diff in patches],
    }
    if target == '-':
        click.echo(json.dumps(output, indent=indent))
    else:
        click.echo('Saving base object and {} patches to {}'
                   .format(len(output['derivatives']), target))

        with open(target, 'w') as f:
            json.dump(output, f, indent=indent)


@minstrel.group()
def apply():
    """Apply mocked objects over a certain transport."""
    pass


@apply.command()
@click.argument('source')
@click.option('--host', '-h', type=str, default='localhost')
@click.option('--user', '-u', type=str, default='guest')
@click.option('--password', '-p', type=str, default='guest')
def amqp(source, host, user, password):
    """Send all generated objects to an AMQP exchange."""
    click.echo('Broken, currently.', err=True)


@apply.command()
@click.argument('source')
@click.option('--config', '-c', type=str)
@click.option('--server', '-s', type=str)
@click.option('--host', '-h', type=str)
@click.option('--user', '-u', type=str)
@click.option('--password', '-p', type=str)
@click.option('--database', '-d', type=str)
def sql(source, config, **kwargs):
    """Store all generated objects key-to-column to an SQL table."""
    transport_kwargs = _read_config_into_kwargs(config, kwargs)
    transport = transports.SQLTransport(**transport_kwargs)

    with open(source, 'r') as f:
        data = json.load(f)

    mock = Mock(data['transports'], data['base'], data['derivatives'])

    try:
        transport.write(mock)
    except (NoSuchTableError, NoSuchColumnError) as e:
        click.echo(e, err=True)


@minstrel.group()
def read():
    """Read from a storage into a Minstrel-loadable file."""
    pass


@read.command('sql')
@click.argument('table_name')
@click.option('--config', '-c', type=str)
@click.option('--server', '-s', type=str)
@click.option('--host', '-h', type=str)
@click.option('--user', '-u', type=str)
@click.option('--password', '-p', type=str)
@click.option('--database', '-d', type=str)
@click.pass_context
def read_sql(ctx, table_name, config, **kwargs):
    """Store all generated objects key-to-column to an SQL table."""
    transport_kwargs = _read_config_into_kwargs(config, kwargs)
    transport = transports.SQLTransport(**transport_kwargs)

    mock = transport.read(table_name)
    click.echo(json.dumps(mock, indent=2))


if __name__ == '__main__':
    minstrel()
