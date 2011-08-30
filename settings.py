class DatabaseTypes:
	SQLITE		= 0
	MYSQL 		= 1
	POSTGRES	= 2

# script configuration
# database options
class Database:
	type 		= DatabaseTypes.SQLITE# database type, one of DatabaseTypes
	database 	= "imdb_data"			# database name
	encoding 	= "utf-8"				# used to pre-encode the queries to drop any invalid characters
										# for the database type
	host 		= "127.0.0.1"			# database host
	user 		= "postgres"			# database username
	password 	= "password"			# database password
	clear_old_db = False				# clear old database information if exists

# general options
class Options:
	list_dir 			= "./db_dump"	# directory of the imdb list files
	file_extension 		= ".list"		# file extension for the imdb list files
	query_debug 		= False			# show log of all sql queries at construction time
	show_progress 		= True			# show progress (at all)
	progress_count 		= 10000			# show progress every _n_ lines
	commit_count 		= 10000			# commit every _n_ lines, -1 means only on completion
										# database will commit on completion of each file regardless
	show_time 			= True			# show the total time taken to complete
	use_native			= False			# use native parsing operations instead of regex
	use_dict			= True			# use a dictionary to generate and cache db id's in program
	use_cache			= True			# cache the dictionaries to the disk, must be enabled if you 
										# you want to convert only some files and you want to use dict
	schema_dir			= "schemas"		# directory to load the db schemas from
	cache_dir			= "cache"		# directory to load the dictionary caches from if applicable
	proc_all			= True			# overrides the individual process directives

