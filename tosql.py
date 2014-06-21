# Converts the IMDB database *.list into a SQLite datbase
# Ameer Ayoub <ameer.ayoub@gmail.com>
# @todo make the whole thing database agnostic so we can switch

import re
from types import StringType
import os
from numerals import rntoi
import time
import cPickle as pickle
from settings import Database, Options, DatabaseTypes

def get_schema_prefix(type_d):
	if type_d == DatabaseTypes.SQLITE:
		return "sqlite"
	elif type_d == DatabaseTypes.MYSQL:
		return "mysql"
	elif type_d == DatabaseTypes.POSTGRES:
		return "postgres"
	else:
		return None

dicts = {}
counts = {}

def mk(file_name):
	"""utility function that turns a list name into a openable file name/path"""
	return Options.list_dir+'/'+file_name+Options.file_extension

	
# Precompile the regexes
class ParseRegexes:
	# raw regex strings for reference e.g. regex buddy copy paste
	raw_acted_in = """"?([^"]*?)"?\s\(((\?{4}|\d+)/?(\w+)?).*?\)(\s*\((T?VG?)\))?
		(\s*\((\w*)\))?(\s*\{([^\(]*?)(\s*\(\#(\d+)\.(\d+)\))?\})?
		(\s*\[(.*)\])?(\s*\<(\d+)\>)?"""
	raw_name = """('.+')?\s*(([^,']*),)?\s*([^\(]+)(\((\w+)\))?"""
	raw_movies = """"?([^"]*?)"?\s\(((\?{4}|\d+)/?(\w+)?).*?\)(\s*\((T?VG?)\))?
		(\s*\{([^\(]*?)(\s*\(\#(\d+)\.(\d+)\))?\})?.*"""
	raw_aka_name = """\s*\(aka ([^\)]+)\)"""
	raw_aka_title_title = """\"?([^\"]*)\"?\s*\((\d{4}|\?{4})(/([\w]*))?\)\s*(\((T?VG?)\))?"""
	raw_title_genre = """\"?([^\"]*)\"?\s*\((\d{4}|\?{4})(/([\w]*))?\)\s*(\((T?VG?)\))?\s*(\w+)"""
	raw_aka_title_alias = """\(aka\s\"?([^\"]*)\"?\s\((\d{4}|\?{4})\)\s*\)\s*(\(([^\)]*)\))?\s*(\(([^\)]*)\))?"""
	# compiled regex patterns for use
	name = re.compile("""
		('.+')?\s*				# nickname (optional, group 1)
		(([^,']*),)?\s*			# last name (optional, group 3)
		([^\(]+)				# first name (required, group 4)
		(\((\w+)\))?			# actor number (optional, group 6)
		""", re.VERBOSE)
	acted_in = re.compile("""
		"?([^"]*?)"?\s			# title (required, group 1) surrounded by quotations if it's a tv show
		\(((\?{4}|\d+)/?(\w+)?).*?\)
								# the year (required, group 3), followed by `/ROMAN_NUMERAL` 
								# (optional, group 4) if multiple in same year
		(\s*\((T?VG?)\))?		# special code (optional, group 6), one of 'TV', 'V', 'VG'
		(\s*\((\w*)\))?			# information regarding part (optional, group 8), e.g. 'voice', 'likeness'
		(\s*\{([^\(]*?)(\s*\(\#(\d+)\.(\d+)\))?\})?
								# episode information: episode title (optional, group 10), within that
								# episode series (optional, group 12) and episode number 
								# (optional, group 13) information. The episode series and number are
								# optional within the optional group.
		(\s*\[(.*)\])?			# character name (optional, group 15) (surrounded by '[' and ']')
		(\s*\<(\d+)\>)?			# billing position (optional, group 17) (surrounded by '<' and '>')
		""", re.VERBOSE)
	movies = re.compile(""""
		?([^"]*?)"?\s			# title (required, group 1) surrounded by quotations if it's a tv show
		\(((\?{4}|\d+)/?(\w+)?).*?\)
								# the year (required, group 3), followed by `/ROMAN_NUMERAL` 
								# (optional, group 4) if multiple in same year
		(\s*\((T?VG?)\))?		# special code (optional, group 6), one of 'TV', 'V', 'VG'
		(\s*\{([^\(]*?)(\s*\(\#(\d+)\.(\d+)\))?\})?
								# episode information: episode title (optional, group 8), within that
								# episode series (optional, group 10) and episode number 
								# (optional, group 11) information. The episode series and number are
								# optional within the optional group.
		.*						# the rest of the line, usually the redundant year/year range
								# (optional, ungrouped)
		""", re.VERBOSE)
	aka_name = re.compile("""
		\s*\(aka ([^\)]+)\)		# alias name (required, group 1)
		""", re.VERBOSE)
	aka_title_alias = re.compile("""
		\(aka\s\"?([^\"]*)\"?\s	# title (required, group 1)
		\((\d{4}|\?{4})\)\s*\)\s*
								# year (required, group 2)
		(\(([^\)]*)\))?\s*		# location (required, group 4)
		(\(([^\)]*)\))?			# reason (optional, group 6)
		""", re.VERBOSE)
	aka_title_title = re.compile("""
		\"?([^\"]*)\"?\s*		# title (required, group 1)
		\((\d{4}|\?{4})			# year (required, group 2)
		(/([\w]*))?\)\s*		# number (optional, group 4)
		(\((T?VG?)\))?			# code (optional, group 6)
		""", re.VERBOSE)
	title_genre = re.compile("""
		\"?([^\"]*)\"?\s*		# title (required, group 1)
		\((\d{4}|\?{4})			# year (required, group 2)
		(/([\w]*))?\)\s*		# number (optional, group 4)
		(\((T?VG?)\))?\s*		# code (optional, group 6)
		(\w+)					# genre (required, group 7)
		""", re.VERBOSE)


# Enum Classes
# Naming conventions if `Table``Column`
class ActorsGender:
	MALE 	= 1
	FEMALE 	= 0

class MoviesType:
	TV 	= 0
	V 	= 1
	VG 	= 2
	M 	= 3		# there's no code for this, this is default Movie
	@staticmethod
	def from_str(type_string):
		"""converts a type string to a type enum"""
		global type_enum
		if type_string == "V":
			return MoviesType.V
		elif type_string == "VG":
			return MoviesType.VG
		elif type_string == "TV":
			return MoviesType.TV
		else:
			return MoviesType.M


def mk_schema(name, use_dict = False):
	if use_dict:
		return "%s/%s.use_dict.sql" % (Options.schema_dir, name)
	else:
		return "%s/%s.sql" % (Options.schema_dir, name)
	

def mk_cache(name):
	return "%s/%s.cache" % (Options.cache_dir, name)


def mk_drop(name):
	return "%s/%s.drop.sql" % (Options.schema_dir, name)


def executescript(c, of, debug = False):
	"""Executes a SQL script by processing out comments and executing each sql
	command individually."""
	query_list = []
	query_list_candidates = of.readlines()
	for line in query_list_candidates:
		# process out comment lines
		if line.startswith("--"):
			pass
		else:
			if line.strip() != "":
				query_list.append(line.strip())
	query_list = " ".join(query_list).split(';')
	for query in query_list:
		if query.strip():
			if debug:
				print "executescript [status] : executing query:\n\t%s\n" % (query.strip())
			c.execute(query.strip())


def create_tables(c, drop_all = False):
	""" Create Tables
	As per schema (refer to imdb.db.png (image) or imdb.mwb (mysql workbench))
	Things that are chars are instead integers which we can use an in program
	defined enum (integers) since chars are unavailable in sqlite and text would
	be unnecessary."""
	print "create_tables [status]: create tables triggered."
	autoincrement = " autoincrement"
	global Options, Database
	if drop_all:
		print "create_tables [status]: dropping tables initiated."
		if Database.type == DatabaseTypes.SQLITE:
			drop_sql = open(mk_drop("sqlite")).read()
		elif Database.type == DatabaseTypes.MYSQL:
			drop_sql = open(mk_drop("mysql")).read()
		elif Database.type == DatabaseTypes.POSTGRES:
			drop_sql = open(mk_drop("postgres")).read()
		drop_list = drop_sql.split(";")
		for line in drop_list:
			query = line.strip()
			if query:
				c.execute(line)
		print "create_tables [status]: dropping tables complete."
	if Database.type == DatabaseTypes.SQLITE:
		dbf = open(mk_schema("sqlite", Options.use_dict))
		query_list = dbf.read()
		c.executescript(query_list)
	elif Database.type == DatabaseTypes.MYSQL:
		dbf = open(mk_schema("mysql", Options.use_dict))
		executescript(c, dbf)
	elif Database.type == DatabaseTypes.POSTGRES:
		dbf = open(mk_schema("postgres", Options.use_dict))
		executescript(c, dbf)

def quote_escape(string):
	if string:
		return string.replace("\"", "\"\"").replace("\'", "\'\'").replace("\\", "/")
	else:
		return None

# @todo optimize the query building functions by using lists/join
def build_select_query(name, param_dict):
	if not param_dict:
		print "build_select_query: error param dictionary is empty!"
		return None
	select_query = "SELECT id" + name + " FROM " + name + " WHERE "
	for k,v in param_dict.items():
		if v:
			if isinstance(v, StringType):
				select_query += k + "=\"" + quote_escape(v) + "\" AND "
			else:
				select_query += k + "=" + str(v) + " AND "
	# remove trailing AND
	select_query = select_query[:-4] + "LIMIT 1"
	if Options.query_debug:
		print select_query
	return select_query


def build_insert_query(name, param_dict, quote_keys = False):
	global Database
	if not param_dict:
		print "build_insert_query: [error] param dictionary is empty!"
		return None
	insert_query_front = "INSERT INTO " + name + " ("
	insert_query_end = ") VALUES ("
	for k,v in param_dict.items():
		if v:
			if quote_keys:
				insert_query_front += "`" + k + "`, "
			else:
				insert_query_front += k + ", "
			if isinstance(v, StringType):
				# surround with quotes if string
				insert_query_end += "\'" + quote_escape(v) + "\', "
			else:
				insert_query_end +=  str(v)  + ", "
	# remove the trailing comma/spaces with [:-2]
	insert_query = insert_query_front[:-2] + insert_query_end[:-2] + ")"
	if Database.encoding:
		# preconvert to db encoding to avoid db errors, especially from postgres / utf-8
		insert_query = insert_query.decode(Database.encoding, errors='ignore')
	if Options.query_debug:
		print insert_query
	return insert_query

	
def unpack_dict(param_dict):
	return tuple(sorted(param_dict.items()))
	

def select_or_insert(connection_cursor, name, param_dict, skip_lookup = False, supress_output = False):
	"""selects or inserts a row into the database, returning the appropriate id field
	note this makes the assumption the id name is id`table_name` which is the case for the schema
	defined above"""
	global dicts, counts
	row = None
	unpacked = unpack_dict(param_dict)
	select_query = build_select_query(name, param_dict)
	if not skip_lookup:
		if Options.use_dict:
			if name in dicts:
				if unpacked in dicts[name]:
					return dicts[name][unpacked]
			else:
				# run query anyway because not in dicts
				connection_cursor.execute(select_query)
				row = connection_cursor.fetchone()
		else:
			connection_cursor.execute(select_query)
			row = connection_cursor.fetchone()
	if row:
		return row[0]
	else:
		# be careful if you use multi threading here later, will have to lock
		rv = 0
		if Options.use_dict:
			if name in dicts:
				dicts[name][unpacked] = counts[name]
				param_dict["id"+name] = counts[name]
				rv = counts[name]
				counts[name] += 1
		connection_cursor.execute(build_insert_query(name, param_dict))
		if Options.use_dict and not supress_output:
			if name in dicts:
				return rv
		if not supress_output:
			connection_cursor.execute(select_query)
			row = connection_cursor.fetchone()
			if row:
				return row[0]
			else:
				print "select_or_insert: [error] could not insert : ", param_dict
				return None
		else:
			return None


def select(connection_cursor, name, param_dict, dict_only = False):
	"""selects a row from the database, returning the appropriate id field
	note this makes the assumption the id name is id`table_name` which is the 
	case for the schema defined above"""
	global dicts
	unpacked = unpack_dict(param_dict)
	if Options.use_dict:
		if name in dicts:
			if unpacked in dicts[name]:
				return dicts[name][unpacked]
			elif dict_only:
				return None
	select_query = build_select_query(name, param_dict)
	connection_cursor.execute(select_query)
	row = connection_cursor.fetchone()
	if row:
		return row[0]
	else:
		return None

		
def save_dict(name):
	global dicts, counts
	pfd_path = mk_cache("%s.dict"%(name))
	pfc_path = mk_cache("%s.count"%(name))
	pfd = pickle.Pickler(open(pfd_path, "wb"))
	pfd.fast = True
	pfd.dump(dicts[name])	
	pfc = pickle.Pickler(open(pfc_path, "wb"))
	pfc.fast = True
	pfc.dump(counts[name])
	

def load_dict(name, force_load = False):
	global dicts, counts
	if len(dicts[name]) > 0 and not force_load:
		return False
	else:
		pfd_path = mk_cache("%s.dict"%(name))
		pfc_path = mk_cache("%s.count"%(name))
		if os.path.exists(pfd_path) and os.path.exists(pfc_path):
			pfd = pickle.Unpickler(open(pfd_path, "rb"))
			dicts[name] = pfd.load()
			pfc = pickle.Unpickler(open(pfc_path, "rb"))
			counts[name] = pfc.load()
			return True
		else:
			return False


def connect_db(db, create_tables_enabled = False):
	# Create tables enabled is there to provide a hard switch to stopping
	# tables from being created, in the case of getting a connection to do
	# indexing we don't want to accidently clear the database
	# Initialize Database
	conn = None
	c = None
	if db.type == DatabaseTypes.SQLITE:
		sqlite3 = __import__("sqlite3")
		exists = os.path.exists(Database.database)
		# Since it's sqlite we just remove the old file, if this was an actual
		# db we would drop from all the tables
		if db.clear_old_db and exists:
			os.remove(db.database)
		conn = sqlite3.connect(db.database)
		c = conn.cursor()
		if (db.clear_old_db or not exists) and create_tables_enabled:
			create_tables(c)
	elif db.type == DatabaseTypes.MYSQL:
		MySQLdb = __import__("MySQLdb")
		conn = MySQLdb.connect(host = db.host, db = db.database, user = db.user, passwd = db.password)
		c = conn.cursor()
		if create_tables_enabled:		
			create_tables(c, drop_all = db.clear_old_db)
	elif db.type == DatabaseTypes.POSTGRES:
		psycopg2 = __import__("psycopg2")
		conn = psycopg2.connect(host = db.host, database = db.database, user = db.user, password = db.password)
		c = conn.cursor()
		if create_tables_enabled:
			create_tables(c, drop_all = db.clear_old_db)
	else:
		print "__main__ [error]: unknown database type #%d." % (db.type)
		quit()
	return conn, c


if __name__ == "__main__":
	if Options.show_time:
		start = time.clock()
	if Options.use_native:
		parse = __import__("native.parse").parse
	if Options.use_dict:
		dicts["actors"] = {}
		dicts["movies"] = {}
		dicts["series"] = {}
		dicts["genres"] = {}
		dicts["keywords"] = {}
		counts["actors"] = 1
		counts["movies"] = 1
		counts["series"] = 1
		counts["genres"] = 1
		counts["keywords"] = 1
	
	process_flags = { 
		"actors": False,
		"movies": False,
		"aka_names": False,
		"aka_titles": False,
		"genres": False,
		"keywords": False
	}
	
	conn, c = connect_db(Database, create_tables_enabled = True)
	
	if Options.use_native:
		print "__main__ [status]: using native c parsing code."
	else:
		print "__main__ [status]: using python regex parsing code."
	# Read in data from raw list files
	
	#
	# Actors/Actresses List File
	# Dependencies : None
	# Updates : Actors, Movies, Series
	#
	if process_flags["actors"] or Options.proc_all:
		files_to_process = ["actresses", "actors"]
		#files_to_process = ["actors.test"]
		for file in files_to_process:
			current_file = mk(file)
			current_gender = ActorsGender.MALE if file=="actors" else ActorsGender.FEMALE
			f = open(current_file)
			# Skip over the information at the beginning and get to the actual data list
			line_number = 1 
			line = f.readline()
			while(line and line != "----			------\n"):
				line = f.readline()
				line_number += 1
			new_actor = True
			for line in f:
				if Options.show_progress and (line_number%Options.progress_count == 0):
					print "__main__ [status]: processing line", line_number
				if Options.commit_count != -1 and (line_number%Options.commit_count == 0):
					conn.commit()
				line_number += 1
				if line == "\n":
					new_actor = True
					continue
				elif line == "-----------------------------------------------------------------------------\n":
					# this is the last valid line before there is a bunch of junk
					break
				if new_actor:
					# reset all names to defaults
					current_lastname = ""
					current_firstname = ""
					current_nickname = ""
					current_number = 0
					# use regex to parse out name parts
					name = line.split('\t')[0]
					if Options.use_native:
						m = parse.actor(name)
						if not m:
							print("__main__ [error]: while processing " + current_file + "[" + str(line_number) + "]: " +
								"invalid name : " + name)
						else:
							current_nickname = m[0]
							current_lastname = m[1]
							current_firstname = m[2]
							current_number = rntoi(m[3])
					else:
						m = re.match(ParseRegexes.name, name)
						if not m:
							print("__main__ [error]: while processing " + current_file + "[" + str(line_number) + "]: " +
							"invalid name : " + name)
						else:
							current_nickname = m.group(1)
							current_lastname = m.group(3)
							current_firstname = m.group(4).strip() # only required field
							current_number = rntoi(m.group(6))
					current_actor = select_or_insert(c, "actors", {"lname" : current_lastname, 
						"fname" : current_firstname, "mname": current_nickname, "gender": current_gender,
						"number": current_number}, skip_lookup = True)
				# process line
				if new_actor:
					new_actor = False
					to_process = line.split('\t')[-1].strip() # use the rest of the line if we read in actor data
				else:
					to_process = line.strip()
				good = False
				n = None
				if Options.use_native:
					n = parse.acted_in(to_process)
					if n:
						good = True
						title = n[0]
						try:
							year = int(n[1]) # there always has to be a year
						except ValueError:
							print("__main__ [error]: while processing " + current_file + "[" + str(line_number) + "]: " +
							"year not valid integer value: \n\"" + to_process +"\"\n--> \t"),
							print n,
							quit()
						number = rntoi(n[2]) # in roman numerals, needs to be converted
						special_code = MoviesType.from_str(n[3])
						special_information = n[4]
						episode_title = n[5]
						character_name = n[8]
						try:
							episode_series = int(n[6]) if n[6] else None
							episode_number = int(n[7]) if n[7] else None
							billing_position = int(n[9]) if n[9] else None
						except ValueError:
							print("__main__ [error]: while processing " + current_file + "[" + str(line_number) + "]: " +
							" not valid integer value: \n\"" + to_process +"\"\n--> \t"),
							print n,
				else:
					n = re.match(ParseRegexes.acted_in, to_process)
					if n:
						good = True
						title = n.group(1)
						try:
							if n.group(3) == "????":
								year = 0
							else:					
								year = int(n.group(3)) # there always has to be a year
						except ValueError:
							print("__main__ [error]: while processing " + current_file + "[" + str(line_number) + "]: " +
							"year not valid integer value: " + to_process)
							quit()
						number = rntoi(n.group(4)) # in roman numerals, needs to be converted
						special_code = MoviesType.from_str(n.group(6))
						special_information = n.group(8)
						episode_title = n.group(10)
						episode_series = int(n.group(12)) if n.group(12) else None
						episode_number = int(n.group(13)) if n.group(13) else None
						character_name = n.group(15)
						billing_position = int(n.group(17)) if n.group(17) else None
				if good:
					current_movie = select_or_insert(c, "movies", {"title": title, "year": year, 
						"number": number, "type": special_code})
					current_series = None
					if episode_title:
						current_series = select_or_insert(c, "series", {"idmovies": current_movie,
							"name": episode_title, "season": episode_series, "number": episode_number})
					# insert into the db the acted in information
					select_or_insert(c, "acted_in", {"idmovies": current_movie, "idseries": current_series,
						"idactors": current_actor, "character": character_name, "billing_position":
						billing_position}, skip_lookup = True, supress_output = True)
				else:
					print("__main__ [error]: while processing" + current_file + "[" + str(line_number) + "]: " +
					"invalid info: " + to_process)
					if Options.use_native:
						print "parsed as: ", n
			f.close()
			conn.commit()
			print "__main__ [status]: processing of", current_file, "complete."
		if Options.use_cache and Options.use_dict:
			save_dict("actors")
			save_dict("movies")
			save_dict("series")
		
	#
	# Movies List
	# Dependencies : Movies, Series
	# Updates : Movies, Series
	#
	if process_flags["movies"] or Options.proc_all:
		current_file = mk("movies")
		if Options.use_cache and Options.use_dict:
			load_dict("movies")
			load_dict("series")
		f = open(current_file)
		line_number = 1 
		# Skip over the information at the beginning and get to the actual data list
		line = f.readline()
		while(line and line != "===========\n"):
			line = f.readline()
			line_number += 1
		f.readline() # skip over the blank line inbetween movie list and header
		line_number += 1
		for line in f:
			if Options.show_progress and (line_number%Options.progress_count == 0):
				print "__main__ [status]: processing line", line_number
			if Options.commit_count != -1 and (line_number%Options.commit_count == 0):
				conn.commit()
			line_number += 1
			if line == "-----------------------------------------------------------------------------\n":
				# this is the last valid line before there is a bunch of junk
				break
			m = re.match(ParseRegexes.movies, line)
			if not m:
				print("__main__ [error]: while processing " + current_file + "[" + str(line_number) + "]: " +
				"invalid movie : " + line)
			else:
				title = m.group(1)
				try:
					if m.group(3) == "????":
						year = 0
					else:					
						year = int(m.group(3)) # there always has to be a year
				except ValueError:
					print("__main__ [error]: while processing " + current_file + "[" + str(line_number) + "]: " +
					"year not valid integer value: " + line)
					quit()
				number = rntoi(m.group(4)) # in roman numerals, needs to be converted
				special_code = MoviesType.from_str(m.group(6))
				episode_title = m.group(8)
				episode_series = int(m.group(10)) if m.group(10) else None
				episode_number = int(m.group(11)) if m.group(11) else None
				current_movie = select_or_insert(c, "movies", {"title": title, "year": year, 
					"number": number, "type": special_code})
				if episode_title:
					select_or_insert(c, "series", {"idmovies": current_movie,
						"name": episode_title, "season": episode_series, "number": episode_number},
						supress_output = True)
		f.close()
		conn.commit()
		if Options.use_cache and Options.use_dict:
			save_dict("movies")
			save_dict("series")
		print "__main__ [status]: processing of", current_file, "complete."

	#
	# Aka-Names List File
	# Dependencies : Actors
	# Updates : None 
	#
	if process_flags["aka_names"] or Options.proc_all:
		current_file = mk("aka-names")		
		if Options.use_cache and Options.use_dict:
			print "__main__ [status]: loading actors cache file."
			if load_dict("actors"):
				print "__main__ [status]: loaded actors dictionary cache file."
			else:
				print "__main__ [warning]: failed to load actors dictionary cache file."
		f = open(current_file)
		# Skip over the information at the beginning and get to the actual data list
		line_number = 1 
		line = f.readline()
		while(line and line != "==============\n"):
			line_number += 1
			line = f.readline()
		new_actor = True
		is_valid = True
		for line in f:
			if Options.show_progress and (line_number%Options.progress_count == 0):
				print "__main__ [status]: processing line", line_number
			if Options.commit_count != -1 and (line_number%Options.commit_count == 0):
				conn.commit()
			line_number += 1
			if line == "\n":
				new_actor = True
				continue
			if new_actor:
				# reset all names to defaults
				current_lastname = ""
				current_firstname = ""
				current_nickname = ""
				current_number = 0
				# use regex to parse out name parts
				name = line.strip()
				if Options.use_native:
					m = parse.actor(name)
					if not m:
						print("__main__ [error]: while processing " + current_file + "[" + str(line_number) + "]: " +
							"invalid name : " + name)
					else:
						current_nickname = m[0]
						current_lastname = m[1]
						current_firstname = m[2]
						current_number = rntoi(m[3])
				else:
					m = re.match(ParseRegexes.name, name)
					if not m:
						print("__main__ [error]: while processing " + current_file + "[" + str(line_number) + "]: " +
						"invalid name : " + name)
					else:
						current_nickname = m.group(1)
						current_lastname = m.group(3)
						current_firstname = m.group(4).strip()
						current_number = rntoi(m.group(6))
				# try male default
				current_actor = None
				dict_only_search = True if Options.use_dict else False
				current_actor = select(c, "actors", {"lname" : current_lastname, 
					"fname" : current_firstname, "mname": current_nickname, "gender": ActorsGender.MALE,
					"number": current_number}, dict_only_search)
				if not current_actor:
					# try female
					current_actor = select(c, "actors", {"lname" : current_lastname, 
					"fname" : current_firstname, "mname": current_nickname, "gender": ActorsGender.FEMALE,
					"number": current_number}, dict_only_search)
				new_actor = False
				if current_actor:
					is_valid = True
					continue
				else:
					is_valid = False
					continue
			# process line
			to_process = line.strip()
			if is_valid:
				n = re.match(ParseRegexes.aka_name, to_process)
				if n:
					name = n.group(1)
					select_or_insert(c, "aka_names", {"idactors": current_actor,
					"name" : name}, skip_lookup = True, supress_output = True)
				else:
					print("__main__ [error]: while processing %s [%d]: invalid alias: " % (current_file, line_number, to_process))
					#supress alias names errors
		f.close()
		conn.commit()
		print "__main__ [status]: processing of", current_file, "complete."

	
	#
	# Aka-Titles List File
	# Dependencies : Movies
	# Updates : None
	#
	if process_flags["aka_titles"] or Options.proc_all:
		current_file = mk("aka-titles")
		if Options.use_cache and Options.use_dict:
			print "__main__ [status]: loading movies cache file."
			if load_dict("movies"):
				print "__main__ [status]: loaded movies dictionary cache file."
			else:
				print "__main__ [warning]: failed to load movies dictionary cache file."
		f = open(current_file)
		# Skip over the information at the beginning and get to the actual data list
		line_number = 1 
		line = f.readline()
		while(line and line != "===============\n"):
			line = f.readline()
			line_number += 1
		new_movie = True
		is_valid = True
		for line in f:
			if Options.show_progress and (line_number%Options.progress_count == 0):
				print "__main__ [status]: processing line", line_number
			if Options.commit_count != -1 and (line_number%Options.commit_count == 0):
				conn.commit()
			line_number += 1
			if line == "\n":
				new_movie = True
				continue
			if new_movie:
				# reset all info to defaults
				current_title = ""
				current_year = -1
				current_number = None
				current_special_code = MoviesType.M
				# use regex to parse out movie title parts
				title = line.strip()
				m = re.match(ParseRegexes.aka_title_title, title)
				if m:
					current_title = m.group(1)
					current_year = -1
					if m.group(2) and m.group(2) == "????":
						current_year = 0
					elif m.group(2):
						current_year = int(m.group(2))
					number = rntoi(m.group(4)) if m.group(4) else None
					special_code = MoviesType.from_str(m.group(6))
				else:
					print("__main__ [error]: while processing " + current_file + "[" + str(line_number) + "]: " +
					"invalid title : " + title)
				dict_only_search = True if Options.use_dict else False
				current_movie = select(c, "movies", {"title" : current_title, 
					"year" : current_year, "type": current_special_code, "number": current_number}, dict_only_search)
				if current_movie:
					is_valid = True
					new_movie = False
					continue
				else:
					is_valid = False
					new_movie = False
					continue
			# process line
			if is_valid:
				to_process = line.strip()
				n = re.match(ParseRegexes.aka_title_alias, to_process)
				if n:
					title = n.group(1)
					year = -1
					if n.group(2) and n.group(2) == "????":
						year = 0
					elif n.group(2):
						year = int(n.group(2))
					location = n.group(4)
					# skip over reason field
					select_or_insert(c, "aka_titles", {"idmovies": current_movie,
					"title": title, "year": year, "location": location},
					skip_lookup = True, supress_output = True)
				else:
					print("__main__ [error]: while processing %s [%d]: invalid alias: %s" % (current_file, line_number, to_process))
		f.close()
		conn.commit()
		print "__main__ [status]: processing of", current_file, "complete."
		

	#
	# Movies Genres
	# Dependencies : Movies
	# Updates : Genres
	#
	if process_flags["genres"] or Options.proc_all:
		current_file = mk("genres")
		if Options.use_cache and Options.use_dict:
			print "__main__ [status]: loading movies cache file."
			if load_dict("movies"):
				print "__main__ [status]: loaded movies dictionary cache file."
			else:
				print "__main__ [warning]: failed to load movies dictionary cache file."
		f = open(current_file)
		# Skip over the information at the beginning and get to the actual data list
		line_number = 1 
		line = f.readline()
		while(line and line != "8: THE GENRES LIST\n"):
			line = f.readline()
			line_number += 1
		line = f.readline() # read over the seperator line
		line_number += 1
		for line in f:
			if Options.show_progress and (line_number%Options.progress_count == 0):
				print "__main__ [status]: processing line", line_number
			if Options.commit_count != -1 and (line_number%Options.commit_count == 0):
				conn.commit()
			line_number += 1
			if line == "\n":
				continue
			else:
				# reset all info to defaults
				current_title = ""
				current_year = -1
				current_number = None
				current_special_code = MoviesType.M
				current_genre = None
				# use regex to parse out movie title parts
				title = line.strip()
				m = re.match(ParseRegexes.title_genre, title)
				if m:
					current_title = m.group(1)
					current_year = -1
					if m.group(2) and m.group(2) == "????":
						current_year = 0
					elif m.group(2):
						current_year = int(m.group(2))
					number = rntoi(m.group(4)) if m.group(4) else None
					special_code = MoviesType.from_str(m.group(6))
					genre = m.group(7)
					dict_only_search = True if Options.use_dict else False
					current_movie = select(c, "movies", {"title" : current_title, 
					"year" : current_year, "type": current_special_code, "number": current_number}, dict_only_search)
					current_genre = select_or_insert(c, "genres", {"genre": genre})
					if current_movie and current_genre:
						select_or_insert(c, "movies_genres", {"idmovies": current_movie, "idgenres": current_genre},
						skip_lookup = True, supress_output = True)
					else:
						#print("__main__ [error]: while processing %s [%d]: movie/genre lookup failed: %s" % (current_file, line_number, title))
						pass
				else:
					#print("__main__ [error]: while processing %s [%d]: invalid title/genre: %s" % (current_file, line_number, title))
					pass
		f.close()
		conn.commit()
		if Options.use_cache and Options.use_dict:
			save_dict("genres")
		print "__main__ [status]: processing of", current_file, "complete."

		
	#
	# Movies Keywords
	# Dependencies : Movies
	# Updates : None
	#
	if process_flags["keywords"] or Options.proc_all:
		current_file = mk("keywords")
		if Options.use_cache and Options.use_dict:
			print "__main__ [status]: loading movies cache file."
			if load_dict("movies"):
				print "__main__ [status]: loaded movies dictionary cache file."
			else:
				print "__main__ [warning]: failed to load movies dictionary cache file."
		f = open(current_file)
		# Skip over the information at the beginning and get to the actual data list
		line_number = 1 
		line = f.readline()
		while(line and line != "8: THE KEYWORDS LIST\n"):
			line = f.readline()
			line_number += 1
		line = f.readline() # read over the seperator line
		line_number += 1
		for line in f:
			if Options.show_progress and (line_number%Options.progress_count == 0):
				print "__main__ [status]: processing line", line_number
			if Options.commit_count != -1 and (line_number%Options.commit_count == 0):
				conn.commit()
			line_number += 1
			if line == "\n":
				continue
			else:
				# reset all info to defaults
				current_title = ""
				current_year = -1
				current_number = None
				current_special_code = MoviesType.M
				current_keyword = None
				# use regex to parse out movie title parts
				title = line.strip()
				m = re.match(ParseRegexes.title_genre, title)
				if m:
					current_title = m.group(1)
					current_year = -1
					if m.group(2) and m.group(2) == "????":
						current_year = 0
					elif m.group(2):
						current_year = int(m.group(2))
					number = rntoi(m.group(4)) if m.group(4) else None
					special_code = MoviesType.from_str(m.group(6))
					keyword = m.group(7)
					dict_only_search = True if Options.use_dict else False
					current_movie = select(c, "movies", {"title" : current_title, 
					"year" : current_year, "type": current_special_code, "number": current_number}, dict_only_search)
					current_keyword = select_or_insert(c, "keywords", {"keyword": keyword})
					if current_movie and current_keyword:
						select_or_insert(c, "movies_keywords", {"idmovies": current_movie, "idkeywords": current_keyword},
						skip_lookup = True, supress_output = True)
					else:
						#print("__main__ [error]: while processing %s [%d]: movie/genre lookup failed: %s" % (current_file, line_number, title))
						pass
				else:
					#print("__main__ [error]: while processing %s [%d]: invalid title/genre: %s" % (current_file, line_number, title))
					pass
		f.close()
		conn.commit()
		if Options.use_cache and Options.use_dict:
			save_dict("keywords")
		print "__main__ [status]: processing of", current_file, "complete."


	c.close()
	conn.close()
	if Options.show_time:
		print "__main__ [status]: total time:", time.clock() - start, "seconds."

