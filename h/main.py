import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('title')
def create(title):
    click.echo(title)
