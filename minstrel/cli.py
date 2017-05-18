import json
import click
from .generate_diffs import differ
from .apply_diffs import (
    amqp_applier,
    NoSuchColumnError,
    NoSuchTableError,
    patcher,
    sql_applier,
)


@click.group()
def minstrel():
    """Generate and apply mocked objects."""
    pass


@minstrel.command()
@click.argument('source')
@click.argument('target')
@click.option('--indent', type=int, default=2,
              help='Spaces of indentation used in output JSON.')
def generate(source, target, indent):
    """
    Generate Minstrel mock file from a list of JSON objects.

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
    with open(source, 'r') as f:
        data = json.load(f)

    try:
        config = data['transports']['queue']
        exchange = config['exchange']
        routing_key = config['routing_key']
    except KeyError:
        click.echo('No AMQP configuration found.', err=True)
        return

    base = data['base']
    derivatives = data['derivatives']

    dicts = patcher(base, (deriv['patches'] for deriv in derivatives))

    amqp_applier(
        f'amqp://{user}:{password}@{host}',
        exchange,
        routing_key,
        dicts,
    )


@apply.command()
@click.argument('source')
@click.option('--server', '-s', type=str, default='postgresql')
@click.option('--host', '-h', type=str, default='localhost')
@click.option('--user', '-u', type=str, default='root')
@click.option('--password', '-p', type=str, default='')
@click.option('--database', '-d', type=str, default='database')
def sql(source, server, host, user, password, database):
    """Store all generated objects key-to-column to an SQL table."""
    with open(source, 'r') as f:
        data = json.load(f)

    try:
        config = data['transports']['sql']
        table = config['table']
    except KeyError:
        click.echo('No SQL configuration found.', err=True)
        return

    base = data['base']
    derivatives = data['derivatives']

    dicts = patcher(base, (deriv['patches'] for deriv in derivatives))

    try:
        sql_applier(
            f'{server}://{user}:{password}@{host}/{database}',
            table,
            dicts,
        )
    except (NoSuchTableError, NoSuchColumnError) as e:
        click.echo(e, err=True)


if __name__ == '__main__':
    minstrel()
