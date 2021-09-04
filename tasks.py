from invoke import task


@task
def lint(c):
    c.run("python -m flake8 src/.", pty=True)
    c.run("python -m black --check .", pty=True)


@task
def test(c):
    c.run("python -m pytest -vv", pty=True)
