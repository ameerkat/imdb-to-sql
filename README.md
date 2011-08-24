# IMDB DB Converter
The file tosql.py converts (some of) the raw `*.list` files to a sql database 
define by the schema below. The schemas folder contains the appropriate 
sql commands to construct the database for the supported databases (see
the `DatabaseTypes` class in the tosql.py script). The script currently 
supports conversion to sqlite and postgres sql databases.

![database schema used by the conversion script](https://github.com/ameerkat/imdb-to-sql/raw/master/db_schema.png)

# Usage
To use first configure the script by going to the top of the script and modifying
the Database and Options classes. Once configured run `python tosql.py`, the
script should notify you as it processes the various files.

# Dependencies
SQLite support is builtin for python 2.5+ so no additional modules are necessary
to convert to a SQLite database. Postgres support is offered through [psycopg2](http://initd.org/psycopg/)
by default. Note that you can use any database adapter you like in reality
for postgres or otherwise provided it is [DB-API2](http://www.python.org/dev/peps/pep-0249/)
compliant and provided you create a schema set for it in the schema folder and
that you put in the code to load the schema given the database type in the
`create_tables` function. You may have to create your own drop table query
specific for the database if it does not support the `DROP TABLE IF EXISTS`
syntax.

