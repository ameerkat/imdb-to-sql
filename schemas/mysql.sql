SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `imdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `acted_in`
--

CREATE TABLE IF NOT EXISTS `acted_in` (
  `idacted_in` int(11) NOT NULL AUTO_INCREMENT,
  `idmovies` int(11) NOT NULL,
  `idseries` int(11) DEFAULT NULL,
  `idactors` int(11) NOT NULL,
  `character` varchar(1023) NOT NULL,
  `billing_position` int(11) DEFAULT NULL,
  PRIMARY KEY (`idacted_in`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `actors`
--

CREATE TABLE IF NOT EXISTS `actors` (
  `idactors` int(11) NOT NULL AUTO_INCREMENT,
  `lname` varchar(1023) NOT NULL,
  `fname` varchar(1023) NOT NULL,
  `mname` varchar(1023) DEFAULT NULL,
  `gender` int(11) NOT NULL,
  `number` int(11) DEFAULT NULL,
  PRIMARY KEY (`idactors`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `aka_names`
--

CREATE TABLE IF NOT EXISTS `aka_names` (
  `idaka_names` int(11) NOT NULL AUTO_INCREMENT,
  `idactors` int(11) NOT NULL,
  `name` varchar(1023) NOT NULL,
  PRIMARY KEY (`idaka_names`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `aka_titles`
--

CREATE TABLE IF NOT EXISTS `aka_titles` (
  `idaka_titles` int(11) NOT NULL AUTO_INCREMENT,
  `idmovies` int(11) NOT NULL,
  `title` varchar(1023) NOT NULL,
  `location` varchar(127) DEFAULT NULL,
  `year` year(4) DEFAULT NULL,
  PRIMARY KEY (`idaka_titles`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `genres`
--

CREATE TABLE IF NOT EXISTS `genres` (
  `idgenres` int(11) NOT NULL AUTO_INCREMENT,
  `genre` varchar(127) NOT NULL,
  PRIMARY KEY (`idgenres`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `keywords`
--

CREATE TABLE IF NOT EXISTS `keywords` (
  `idkeywords` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(127) NOT NULL,
  PRIMARY KEY (`idkeywords`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE IF NOT EXISTS `movies` (
  `idmovies` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(1023) NOT NULL,
  `year` year(4) NOT NULL,
  `number` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `location` varchar(127) DEFAULT NULL,
  `language` varchar(127) DEFAULT NULL,
  PRIMARY KEY (`idmovies`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `movies_genres`
--

CREATE TABLE IF NOT EXISTS `movies_genres` (
  `idmovies_genres` int(11) NOT NULL AUTO_INCREMENT,
  `idmovies` int(11) NOT NULL,
  `idgenres` int(11) NOT NULL,
  `idseries` int(11) DEFAULT NULL,
  PRIMARY KEY (`idmovies_genres`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `movies_keywords`
--

CREATE TABLE IF NOT EXISTS `movies_keywords` (
  `idmovies_keywords` int(11) NOT NULL AUTO_INCREMENT,
  `idmovies` int(11) NOT NULL,
  `idkeywords` int(11) NOT NULL,
  `idseries` int(11) DEFAULT NULL,
  PRIMARY KEY (`idmovies_keywords`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `series`
--

CREATE TABLE IF NOT EXISTS `series` (
  `idseries` int(11) NOT NULL AUTO_INCREMENT,
  `idmovies` int(11) NOT NULL,
  `name` varchar(1023) DEFAULT NULL,
  `season` int(11) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  PRIMARY KEY (`idseries`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
