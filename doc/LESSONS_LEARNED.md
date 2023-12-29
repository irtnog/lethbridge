# Lessons Learned

## Release engineering

https://www.bitecode.dev/p/relieving-your-python-packaging-pain

https://www.bitecode.dev/p/why-not-tell-people-to-simply-use

isort works differently when the project home directory is renamed.

## Working with bad data

TODO

## Dates and times in the Spansh dumps

The Spansh dumps use two different date/time formats:

- `%Y-%m-%d %H:%M:%S+00`, used in `date` and `updateTime` fields

- `%Y-%m-%dT%H:%M:%S`, used in `timestamps` fields

Marshmallow et al seem to handle this without difficulty, but note this answer to ["SQLAlchemy DateTime timezone"](https://stackoverflow.com/questions/414952/sqlalchemy-datetime-timezone#462028).  It may be necessary in production deployments to set the timezone to UTC in the PostgreSQL startup or connection options.

## Preserving JSON floating point precision

Python's [`float`](https://docs.python.org/3/library/functions.html#float) data type cannot store source data unaltered.  Fortunately, the [`decimal`](https://docs.python.org/3/library/decimal.html) module along with SQLAlchemy's [`Numeric`](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric) type seem to do the right thing on PostgreSQL if the unit tests are to be believed.  Why those same tests fail on SQLite requires further investigation.

## Backing Up Docker Volumes

https://docs.docker.com/storage/volumes/#back-up-restore-or-migrate-data-volumes

The `--volumes-from` flag copies all the volume mounts from the named container to the one you're about to run, so the backup command for the Docker Compose project looks like this:

```
docker run -it --rm --volumes-from lethbridge-db-1 -v /home/xenophonf/src/lethbridge/out:/backup ubuntu tar cvzf /backup/backup.tgz /var/lib/postgresql/data
```
