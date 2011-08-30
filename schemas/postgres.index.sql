-- acted_in
CREATE INDEX "ACTED_IN_IDSERIES_INDEX" ON acted_in USING btree (idseries);
CREATE INDEX "ACTED_IN_IDMOVIES_INDEX" ON acted_in USING btree (idmovies);
CREATE INDEX "ACTED_IN_IDACTORS_INDEX" ON acted_in USING btree (idactors);

-- actors
-- not sure how to do partial text searching

-- aka_names
CREATE INDEX "AKA_NAMES_IDACTORS_INDEX" on aka_names USING btree (idactors);

-- aka_titles
CREATE INDEX "AKA_TITLES_IDMOVIES_INDEX" on aka_titles USING btree (idmovies);

-- movies
-- same comment with actors about partial searching

-- series
CREATE INDEX "SERIES_IDMOVIES_INDEX" on series USING btree (idmovies);

