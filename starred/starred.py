#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collections import OrderedDict
from io import BytesIO

import click
from github3 import GitHub
from github3.exceptions import NotFoundError

from starred import VERSION


header = '''
# Starred

## Usage

```bash
$ starred --help

Usage: starred [OPTIONS]

    Creating your own Awesome List used GitHub stars.

    Example:
      starred --username brighteyed --sort > README.md

Options:
    --username TEXT    GitHub username
    --token TEXT       GitHub token
    --sort             sort by language
    --repository TEXT  repository name
    --message TEXT     commit message
    --version          Show the version and exit.
    --help             Show this message and exit.
```

## Demo

```bash
# Automatically create the repository
$ export GITHUB_TOKEN=yourtoken
$ starred --username yourname --repository awesome-stars --sort
```

## Stars

> A curated list of my GitHub stars

'''


html_escape_table = {
    ">": "&gt;",
    "<": "&lt;",
}


def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c, c) for c in text)


@click.command()
@click.option('--username', envvar='USER', help='GitHub username')
@click.option('--token', envvar='GITHUB_TOKEN', help='GitHub token')
@click.option('--sort',  is_flag=True, help='sort by language')
@click.option('--repository', default='', help='repository name')
@click.option('--message', default='update stars', help='commit message')
@click.version_option(version=VERSION, prog_name='starred')
def starred(username, token, sort, repository, message):
    """
    Creating your own Awesome List used GitHub stars.

    Example:
        starred --username brighteyed --sort > README.md
    """
    if repository:
        if not token:
            click.secho('Error: create repository need set --token', fg='red')
            return
        file = BytesIO()
        sys.stdout = file
    else:
        file = None

    gh = GitHub(token=token)
    stars = gh.starred_by(username)
    click.echo(header)
    repo_dict = {}

    for s in stars:
        language = s.language or 'Others'
        description = html_escape(s.description).replace('\n', '') if s.description else ''
        if language not in repo_dict:
            repo_dict[language] = []
        repo_dict[language].append([s.full_name, s.html_url, description.strip()])

    if sort:
        repo_dict = OrderedDict(sorted(repo_dict.items(), key=lambda l: l[0]))

    for language in repo_dict.keys():
        data = u'  - [{}](#{})'.format(language, '-'.join(language.lower().split()))
        click.echo(data)
    click.echo('')

    for language in repo_dict:
        click.echo('## {} \n'.format(language))
        for repo in repo_dict[language]:
            data = u'- [{}]({}) – {}'.format(*repo)
            click.echo(data)
        click.echo('')

    if file:
        try:
            rep = gh.repository(username, repository)
            readme = rep.readme()
            readme.update(message, file.getvalue())
        except NotFoundError:
            print("Repository not found")


if __name__ == '__main__':
    starred()
