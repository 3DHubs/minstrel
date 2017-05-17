import json
import click
from .generate_diffs import differ


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
        "base": default,
        "derivatives": [list(diff) for diff in patches],
    }
    if target == '-':
        click.echo(json.dumps(output, indent=indent))
    else:
        click.echo('Saving base object and {} patches to {}'
                   .format(len(output['derivatives']), target))

        with open(target, 'w') as f:
            json.dump(output, f, indent=indent)


@minstrel.command()
def apply(source):
    with open(source, 'r') as f:
        data = json.load(f)

    default, patches = differ(data)

    output = {
        "original": default,
        "patches": [list(diff) for diff in patches],
    }
    click.echo(json.dumps(output, indent=2))
    click.echo('Found {} patches'.format(len(output['patches'])))


if __name__ == '__main__':
    minstrel()
