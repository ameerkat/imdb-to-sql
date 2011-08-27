from tosql import DatabaseTypes, executescript, get_schema_prefix
from settings import Database, Options

def mk_index(name):
	return "%s/%s.index.sql" % (Options.schema_dir, name)

def create_indices(cursor):
	executescript(open(mk_index(get_schema_prefix(Database.type))), debug = True)

if __name__ == "__main__":
	conn, cursor = connect_db(Database)
	create_indices(cursor)

