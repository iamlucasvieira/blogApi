"""Nox sessions."""

from nox_poetry import session


@session(python=["3.10"])
def tests(session):
    session.install("pytest")
    session.run("pytest")


@session(python=["3.10"])
def lint(session):
    session.install('flake8')
    session.run('flake8')


@session(python=["3.10"])
def mypy(session):
    session.install('mypy', "sqlalchemy-stubs")
    session.run('mypy', "app")
