# Harbour Bookings (toy project)

A deliberately small, fictional hotel-booking API. It is the second repository for testing the
multi-project version of the [issue triage desk](https://github.com/janiduc/issue-triage-poc),
next to [bluefin-shop](https://github.com/janiduc/bluefin-shop). It has its own areas (bookings,
payments, notifications), its own seed issues and its own answer key, so a triage desk serving
both repositories can be checked for keeping them apart.

All data is in memory and invented, and it contains bugs on purpose (see `KNOWN_BUGS.md`).

## Run it

```bash
pip install -r requirements.txt
python app.py
```

The API listens on http://127.0.0.1:5060. Tests: `python -m unittest`.

## Seed issues

`issues/seed_issues.json` holds 8 issues: five bug reports, one vague report, a feature request
and a question. To create them on GitHub, set `GITHUB_TOKEN` (fine-grained, *Issues: read and
write* on this repository) and `GITHUB_REPO=owner/harbour-bookings`, then:

```bash
python scripts/file_issues.py --dry-run
python scripts/file_issues.py
```

## Connecting the triage desk

As administrator, under **Projects**, add a project: tracker GitHub, repository
`owner/harbour-bookings`, the name of the environment variable that holds its token (for example
`GITHUB_TOKEN_HARBOUR`), and the modules `bookings, payments, notifications, other`. Then add
members and press **Import**.
