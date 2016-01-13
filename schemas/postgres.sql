SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: acted_in; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE acted_in (
    idacted_in integer NOT NULL,
    idmovies integer NOT NULL,
    idseries integer,
    idactors integer NOT NULL,
    "character" character varying(1023) NOT NULL,
    billing_position integer
);



--
-- Name: acted_in_idacted_in_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE acted_in_idacted_in_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: acted_in_idacted_in_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE acted_in_idacted_in_seq OWNED BY acted_in.idacted_in;


--
-- Name: actors; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actors (
    idactors integer NOT NULL,
    lname character varying(1023) NOT NULL,
    fname character varying(1023) NOT NULL,
    mname character varying(1023),
    gender integer,
    number integer
);



--
-- Name: actors_idactors_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE actors_idactors_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: actors_idactors_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE actors_idactors_seq OWNED BY actors.idactors;


--
-- Name: aka_names; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE aka_names (
    idaka_names integer NOT NULL,
    idactors integer NOT NULL,
    name character varying(1023) NOT NULL
);



--
-- Name: aka_names_idaka_names_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE aka_names_idaka_names_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: aka_names_idaka_names_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE aka_names_idaka_names_seq OWNED BY aka_names.idaka_names;


--
-- Name: aka_titles; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE aka_titles (
    idaka_titles integer NOT NULL,
    idmovies integer NOT NULL,
    title character varying(1023) NOT NULL,
    location character varying(511),
    year integer
);



--
-- Name: aka_titles_idaka_titles_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE aka_titles_idaka_titles_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: aka_titles_idaka_titles_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE aka_titles_idaka_titles_seq OWNED BY aka_titles.idaka_titles;


--
-- Name: genres; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE genres (
    idgenres integer NOT NULL,
    genre character varying(127) NOT NULL
);



--
-- Name: genres_idgenres_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE genres_idgenres_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: genres_idgenres_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE genres_idgenres_seq OWNED BY genres.idgenres;


--
-- Name: keywords; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE keywords (
    idkeywords integer NOT NULL,
    keyword character varying(127) NOT NULL
);



--
-- Name: keywords_idkeywords_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE keywords_idkeywords_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: keywords_idkeywords_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE keywords_idkeywords_seq OWNED BY keywords.idkeywords;


--
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE movies (
    idmovies integer NOT NULL,
    title character varying(1023) NOT NULL,
    year integer NOT NULL,
    number integer,
    type integer,
    location character varying(127),
    language character varying(127)
);



--
-- Name: movies_genres; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE movies_genres (
    idmovies_genres integer NOT NULL,
    idmovies integer NOT NULL,
    idgenres integer NOT NULL,
    idseries integer
);



--
-- Name: movies_genres_idmovies_genres_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE movies_genres_idmovies_genres_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: movies_genres_idmovies_genres_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE movies_genres_idmovies_genres_seq OWNED BY movies_genres.idmovies_genres;


--
-- Name: movies_idmovies_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE movies_idmovies_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: movies_idmovies_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE movies_idmovies_seq OWNED BY movies.idmovies;


--
-- Name: movies_keywords; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE movies_keywords (
    idmovies_keywords integer NOT NULL,
    idmovies integer NOT NULL,
    idkeywords integer NOT NULL,
    idseries integer
);



--
-- Name: movies_keywords_idmovies_keywords_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE movies_keywords_idmovies_keywords_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: movies_keywords_idmovies_keywords_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE movies_keywords_idmovies_keywords_seq OWNED BY movies_keywords.idmovies_keywords;


--
-- Name: series; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE series (
    id_series integer NOT NULL,
    idmovies integer NOT NULL,
    name character varying(1023),
    season integer,
    number integer
);



--
-- Name: series_id_series_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE series_id_series_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: series_id_series_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE series_id_series_seq OWNED BY series.id_series;


--
-- Name: idacted_in; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE acted_in ALTER COLUMN idacted_in SET DEFAULT nextval('acted_in_idacted_in_seq'::regclass);


--
-- Name: idactors; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE actors ALTER COLUMN idactors SET DEFAULT nextval('actors_idactors_seq'::regclass);


--
-- Name: idaka_names; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE aka_names ALTER COLUMN idaka_names SET DEFAULT nextval('aka_names_idaka_names_seq'::regclass);


--
-- Name: idaka_titles; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE aka_titles ALTER COLUMN idaka_titles SET DEFAULT nextval('aka_titles_idaka_titles_seq'::regclass);


--
-- Name: idgenres; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE genres ALTER COLUMN idgenres SET DEFAULT nextval('genres_idgenres_seq'::regclass);


--
-- Name: idkeywords; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE keywords ALTER COLUMN idkeywords SET DEFAULT nextval('keywords_idkeywords_seq'::regclass);


--
-- Name: idmovies; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE movies ALTER COLUMN idmovies SET DEFAULT nextval('movies_idmovies_seq'::regclass);


--
-- Name: idmovies_genres; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE movies_genres ALTER COLUMN idmovies_genres SET DEFAULT nextval('movies_genres_idmovies_genres_seq'::regclass);


--
-- Name: idmovies_keywords; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE movies_keywords ALTER COLUMN idmovies_keywords SET DEFAULT nextval('movies_keywords_idmovies_keywords_seq'::regclass);


--
-- Name: id_series; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE series ALTER COLUMN id_series SET DEFAULT nextval('series_id_series_seq'::regclass);


--
-- Name: acted_in_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY acted_in
    ADD CONSTRAINT acted_in_pkey PRIMARY KEY (idacted_in);


--
-- Name: actors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (idactors);


--
-- Name: aka_names_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY aka_names
    ADD CONSTRAINT aka_names_pkey PRIMARY KEY (idaka_names);


--
-- Name: aka_titles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY aka_titles
    ADD CONSTRAINT aka_titles_pkey PRIMARY KEY (idaka_titles);


--
-- Name: genres_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY genres
    ADD CONSTRAINT genres_pkey PRIMARY KEY (idgenres);


--
-- Name: keywords_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY keywords
    ADD CONSTRAINT keywords_pkey PRIMARY KEY (idkeywords);


--
-- Name: movies_genres_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY movies_genres
    ADD CONSTRAINT movies_genres_pkey PRIMARY KEY (idmovies_genres);


--
-- Name: movies_keywords_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY movies_keywords
    ADD CONSTRAINT movies_keywords_pkey PRIMARY KEY (idmovies_keywords);


--
-- Name: movies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (idmovies);


--
-- Name: series_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY series
    ADD CONSTRAINT series_pkey PRIMARY KEY (id_series);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;