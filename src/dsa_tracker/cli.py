import click
from datetime import date
from .db import Database, SCHEMA_SQL, get_db_path, stream_problems, stream_reviews
from .models import Problem
from .scheduler import next_box, next_review_date, write_json_file
from .exceptions import ProblemNotFoundError, InvalidReviewError 

@click.group()
def cli():
    pass

# ADD

@cli.command()
@click.argument("title")
@click.option("--diff", type=click.Choice(["Easy", "Medium", "Hard"]), default="Medium", help="Easy/Medium/Hard")
def add(title, diff):
    review_date=next_review_date(1)
    with Database(str(get_db_path())) as cur:
        cur.executescript(SCHEMA_SQL)
        cur.execute(
            "INSERT into problems (title, difficulty, tags, box, next_review) VALUES (?, ?, ?, ?, ?)",
            (title, diff, "", 1, review_date.isoformat())
        )
    click.echo(f"Added: {title} ({diff})")

# LIST

@cli.command(name="list")
@click.argument("table")
def list_dsa(table):
    today = date.today().isoformat()
    choice = table.lower()
    with Database(str(get_db_path())) as cur:
        cur.executescript(SCHEMA_SQL)

        match choice:
            case "p":
                cur.execute("SELECT id, title, difficulty, tags, box, next_review FROM problems")
            case "r":
                cur.execute("SELECT id, problem_id, reviewed_at, result FROM reviews")
            case "d":
                cur.execute("SELECT id, title, difficulty, tags, box, next_review FROM problems WHERE next_review <= ?",
                    (today,),
                )
            case _:
                click.echo(f"Invalid Option `{choice}`")
                return

        rows = cur.fetchall()

    if not rows:
            click.echo("No Data Found!")
    else:
        match choice:
            case "p" | "d":
                for row in rows: 
                    click.echo(f"[{row[0]}] {row[1]} ({row[2]}) — box {row[4]}, due {row[5]}")
            case "r":
                for row in rows:
                    click.echo(f"[{row[0]}] Problem ID:{row[1]}, Reviewd At: {row[2]}, Result: {row[3]}")


# REVIEW

@cli.command()
@click.argument("problem_id", type=int)
@click.option("--result", type=click.Choice(["correct", "wrong"]), required=True)
def review(problem_id, result):
    try:
        with Database(str(get_db_path())) as cur:
            cur.executescript(SCHEMA_SQL)
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
            cur.execute("INSERT into reviews (problem_id, reviewed_at, result) VALUES(?, ?, ?)",
                (problem_id, date.today().isoformat(), result,)
            )
    except ProblemNotFoundError as e:
        raise click.ClickException(str(e))
    click.echo(f"Problem {problem_id}: box {current_box} -> {new_box}, next review {new_date}")

@cli.command()
def stats():
    with Database(str(get_db_path())) as cur:
        cur.executescript(SCHEMA_SQL)

        cur.execute("SELECT COUNT(*) FROM reviews")
        total = cur.fetchone()

        cur.execute("SELECT COUNT(*) FROM reviews WHERE result = ?",
            ("correct",)
        )
        correct = cur.fetchone()

        if total[0] == 0:
            click.echo("No Reviews to evaluate from!")
        else:
            rate = (correct[0] / total[0]) * 100
            click.echo(f"The current success rate is: {rate}% [{correct[0]}/{total[0]}]")

@cli.command()
@click.option("--out", default="export.json", help="Output file path")
def export(out):
    with Database(str(get_db_path())) as cur:
        cur.executescript(SCHEMA_SQL)
        problems = list(stream_problems(cur)) 
        reviews = list(stream_reviews(cur)) 
    write_json_file(out, [{"problems": problems,"reviews": reviews}])
    click.echo(f"Exported {len(problems)} problems to {out}")


if __name__ == "__main__":
    cli()