import click
from db import Database, SCHEMA_SQL
from datetime import date
from models import Problem
from scheduler import next_box, next_review_date
from exceptions import ProblemNotFoundError, InvalidReviewError 

@click.group()
def cli():
    pass

@cli.command()
@click.argument("title")
@click.option("--diff", type=click.Choice(["Easy", "Medium", "Hard"]), default="Medium", help="Easy/Medium/Hard")
def add(title, diff):
    review_date=next_review_date(1)
    with Database("tracker.db") as cur:
        cur.execute(SCHEMA_SQL)
        cur.execute(
            "INSERT into problems (title, difficulty, tags, box, next_review) VALUES (?, ?, ?, ?, ?)",
            (title, diff, "", 1, review_date.isoformat())
        )
    click.echo(f"Added: {title} ({diff})")
@cli.command()
def due():
    today = date.today().isoformat()
    with Database("tracker.db") as cur:
        cur.execute(SCHEMA_SQL)
        cur.execute("SELECT id, title, difficulty, tags, box, next_review FROM problems WHERE next_review <= ?",
            (today,),
        )
        rows = cur.fetchall()

    if not rows:
        click.echo("Nothing Due Today!")
        return
    else:
        for row in rows: 
            click.echo(f"[{row[0]}] {row[1]} ({row[2]}) — box {row[4]}, due {row[5]}")

@cli.command()
@click.argument("problem_id", type=int)
@click.option("--result", type=click.Choice(["correct", "wrong"]), required=True)
def review(problem_id, result):
    try:
        with Database("tracker.db") as cur:
            cur.execute(SCHEMA_SQL)
            cur.execute("SELECT box FROM problems WHERE id = ?", (problem_id,))
            row=cur.fetchone()

            if row is None:
                raise ProblemNotFoundError(f"No problem with id {problem_id}")

            current_box = row[0]
            new_box = next_box(current_box, result)
            new_date = next_review_date(new_box).isoformat()

            cur.execute("UPDATE problems SET box = ?, next_review = ? WHERE id = ?",
                (new_box, new_date, problem_id)
            )
    except ProblemNotFoundError as e:
        raise click.ClickException(str(e))
    click.echo(f"Problem {problem_id}: box {current_box} -> {new_box}, next review {new_date}")

if __name__ == "__main__":
    cli()