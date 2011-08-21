# Schemas
The schema files is a file containing the appropriate sql queries to execute
in order to construct a database appropriate for dumping the imdb data to
according to the script. The format of the file names must be followed in order
to load properly, the format is `database_type.sql` for normal schema and
`database_type.use_dict.sql` for the versions used when using the hashtables
to improve performance. The only difference between these two usually is 
whether or not to autoincrement the key field.
