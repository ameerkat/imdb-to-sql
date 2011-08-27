from tosql import DatabaseTypes, Database, Options, executescript, get_schema_prefix

def mk_index(name):
	return "%s/%s.index.sql" % (Options.schema_dir, name)

def create_indices(cursor):
	executescript(open(mk_index(get_schema_prefix(Database.type))), debug = True)

if __name__ == "__main__":
		
	create_indices(cursor)

