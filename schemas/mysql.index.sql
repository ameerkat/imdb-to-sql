-- note this indexing will take a VERY long time (several hours)
-- acted_in
ALTER TABLE `acted_in` ADD INDEX `ACTED_IN_IDSERIES_INDEX` (`idseries`);
ALTER TABLE `acted_in` ADD INDEX `ACTED_IN_IDMOVIES_INDEX` (`idmovies`);
ALTER TABLE `acted_in` ADD INDEX `ACTED_IN_IDACTORS_INDEX` (`idactors`);

-- actors
ALTER TABLE `actors` ADD INDEX `ACTORS_LASTNAME_INDEX16` (`lname`(16));
ALTER TABLE `actors` ADD INDEX `ACTORS_FIRSTNAME_INDEX16` (`fname`(16));

-- aka_names
ALTER TABLE `aka_names` ADD INDEX `AKA_NAMES_IDACTORS_INDEX` (`idactors`);

-- aka_titles
ALTER TABLE `aka_titles` ADD INDEX `AKA_TITLES_IDMOVIES_INDEX` (`idmovies`);

-- movies
ALTER TABLE `movies` ADD INDEX `MOVIES_TITLE_INDEX16` (`title`(16));

-- series
ALTER TABLE `series` ADD INDEX `SERIES_IDMOVIES_INDEX` (`idmovies`);
ALTER TABLE `series` ADD INDEX `SERIES_NAME_INDEX16` (`name`(16));

