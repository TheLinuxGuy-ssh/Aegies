import click
from db import Database, SCHEMA_SQL
from models import Problem
from scheduler import next_box, next_review_date
from exceptions import ProblemNotFoundError, InvalidReviewError 

@click.group()
def cli():
    pass

@cli.command()
def add():
    click.echo("add: not implemented yet")

@cli.command()
def due():
    click.echo("due: not implemented yet")

@cli.command()
def review():
    click.echo("echo: no implemented yet")

if __name__ == "__main__":
    cli()