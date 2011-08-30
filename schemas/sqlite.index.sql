-- acted_in
CREATE INDEX IF NOT EXISTS "ACTED_IN_IDSERIES_INDEX" ON acted_in (idseries);
CREATE INDEX IF NOT EXISTS "ACTED_IN_IDMOVIES_INDEX" ON acted_in (idmovies);
CREATE INDEX IF NOT EXISTS "ACTED_IN_IDACTORS_INDEX" ON acted_in (idactors);

-- actors
-- not sure how to do partial text searching

-- aka_names
CREATE INDEX IF NOT EXISTS "AKA_NAMES_IDACTORS_INDEX" on aka_names (idactors);

-- aka_titles
CREATE INDEX IF NOT EXISTS "AKA_TITLES_IDMOVIES_INDEX" on aka_titles (idmovies);

-- movies
-- same comment with actors about partial searching

-- series
CREATE INDEX IF NOT EXISTS "SERIES_IDMOVIES_INDEX" on series (idmovies);

