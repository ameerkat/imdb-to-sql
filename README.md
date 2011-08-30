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
script should notify you as it processes the various files. There is also a script
called `index.py` that will let you add the indices to the database after adding
all the data. This script relies on components of the tosql script so the tosql script
must be in the same directory or on the path. Full indexing either in database or
through an external data structure will be added soon to allow autocomplete
and partial title searches.

# Dependencies
SQLite support is builtin for python 2.5+ so no additional modules are necessary
to convert to a SQLite database. Postgres support is offered through [psycopg2](http://initd.org/psycopg/)
by default. Note that you can use any database adapter you like in reality
for postgres or otherwise provided it is [DB-API2](http://www.python.org/dev/peps/pep-0249/)
compliant and provided you create a schema set for it in the schema folder see
more details below. MySQL support is provided through [MySQLdb](http://sourceforge.net/projects/mysql-python/)

## Using another DB-API2 client database adapter
As stated above you may use any [DB-API2](http://www.python.org/dev/peps/pep-0249/)
 compliant adapter given you edit the script file and provide the schemas in the following way:

1. Create a variable for the database type in the `DatabaseTypes` class.
2. Add a condition to the `create_tables` function to drop and create
your database. You may use the function `executescript` on open cursor/files
to execute full SQL files, similar to the builtin capabilities of sqlite's
`executescript` function.
3. Add appropriate drop and create schemas to the schema folder, see
the readme in the schema folder for naming conventions. In general these files
are `db_name.sql`, `db_name.use_dict.sql` and `db_name.drop.sql`
4. Add appropriate loading code to the start of the `__main__` section of the
code, use the Database class to read in database parameters such as host, 
user name/password and database names. Do not put an `import` statement at the
top of the file, use the `__import__` function to load the database driver only
if necessary and your database type is being used.

