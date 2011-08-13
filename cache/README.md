# Cache
This is the folder that cached dictionaries get dumped to if you use the cache
option in the script. This is to allow processing of files that depend on
eachother (e.g. the actors file and the aka-names file) without reprocessing
the whole thing and without loading it from the database again (maintaining
the speed optimizations)
