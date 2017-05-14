import json
import click
from .generate_diffs import differ


@click.group()
def minstrel():
    """A mocking tool."""
    pass


@minstrel.command()
@click.argument('source')
def generate(source):
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
