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
