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
    "character" character varying(255),
    billing_position integer
);


ALTER TABLE public.acted_in OWNER TO postgres;

--
-- Name: acted_in_idacted_in_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE acted_in_idacted_in_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.acted_in_idacted_in_seq OWNER TO postgres;

--
-- Name: acted_in_idacted_in_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE acted_in_idacted_in_seq OWNED BY acted_in.idacted_in;


--
-- Name: actors; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actors (
    idactors integer NOT NULL,
    lname character varying(255),
    fname character varying(255) NOT NULL,
    mname character varying(255),
    gender integer,
    number integer
);


ALTER TABLE public.actors OWNER TO postgres;

--
-- Name: aka_names; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE aka_names (
    idaka_names integer NOT NULL,
    idactors integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.aka_names OWNER TO postgres;

--
-- Name: aka_names_idaka_names_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE aka_names_idaka_names_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.aka_names_idaka_names_seq OWNER TO postgres;

--
-- Name: aka_names_idaka_names_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE aka_names_idaka_names_seq OWNED BY aka_names.idaka_names;


--
-- Name: genres; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE genres (
    idgenres integer NOT NULL,
    genre character varying(63) NOT NULL
);


ALTER TABLE public.genres OWNER TO postgres;

--
-- Name: idaka_titles; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE aka_titles (
    idaka_titles integer NOT NULL,
    idmovies integer NOT NULL,
    title character varying(255) NOT NULL,
    location character varying(63),
    year integer
);


ALTER TABLE public.aka_titles OWNER TO postgres;

--
-- Name: idaka_titles_idaka_titles_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE aka_titles_idaka_titles_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.aka_titles_idaka_titles_seq OWNER TO postgres;

--
-- Name: idaka_titles_idaka_titles_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE aka_titles_idaka_titles_seq OWNED BY aka_titles.idaka_titles;


--
-- Name: keywords; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE keywords (
    idkeywords integer NOT NULL,
    keyword character varying(63) NOT NULL
);


ALTER TABLE public.keywords OWNER TO postgres;

--
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE movies (
    idmovies integer NOT NULL,
    title character varying(255) NOT NULL,
    year integer,
    number integer,
    type integer,
    location character varying(63),
    language character varying(63)
);


ALTER TABLE public.movies OWNER TO postgres;

--
-- Name: movies_genres; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE movies_genres (
    idmovies_genres integer NOT NULL,
    idmovies integer NOT NULL,
    idgenres integer NOT NULL,
    idseries integer
);


ALTER TABLE public.movies_genres OWNER TO postgres;

--
-- Name: movies_genres_idmovies_genres_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE movies_genres_idmovies_genres_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_genres_idmovies_genres_seq OWNER TO postgres;

--
-- Name: movies_genres_idmovies_genres_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE movies_genres_idmovies_genres_seq OWNED BY movies_genres.idmovies_genres;


--
-- Name: movies_keywords; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE movies_keywords (
    idmovies_keywords integer NOT NULL,
    idmovies integer NOT NULL,
    idkeywords integer NOT NULL,
    idseries integer
);


ALTER TABLE public.movies_keywords OWNER TO postgres;

--
-- Name: movies_keywords_idmovies_keywords_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE movies_keywords_idmovies_keywords_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_keywords_idmovies_keywords_seq OWNER TO postgres;

--
-- Name: movies_keywords_idmovies_keywords_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE movies_keywords_idmovies_keywords_seq OWNED BY movies_keywords.idmovies_keywords;


--
-- Name: series; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE series (
    idseries integer NOT NULL,
    idmovies integer NOT NULL,
    name character varying(255),
    season integer,
    number integer
);


ALTER TABLE public.series OWNER TO postgres;

--
-- Name: idacted_in; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE acted_in ALTER COLUMN idacted_in SET DEFAULT nextval('acted_in_idacted_in_seq'::regclass);


--
-- Name: idaka_names; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE aka_names ALTER COLUMN idaka_names SET DEFAULT nextval('aka_names_idaka_names_seq'::regclass);


--
-- Name: idaka_titles; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE aka_titles ALTER COLUMN idaka_titles SET DEFAULT nextval('aka_titles_idaka_titles_seq'::regclass);


--
-- Name: idmovies_genres; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE movies_genres ALTER COLUMN idmovies_genres SET DEFAULT nextval('movies_genres_idmovies_genres_seq'::regclass);


--
-- Name: idmovies_keywords; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE movies_keywords ALTER COLUMN idmovies_keywords SET DEFAULT nextval('movies_keywords_idmovies_keywords_seq'::regclass);


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
-- Name: genres_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY genres
    ADD CONSTRAINT genres_pkey PRIMARY KEY (idgenres);


--
-- Name: idaka_titles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY aka_titles
    ADD CONSTRAINT aka_titles_pkey PRIMARY KEY (idaka_titles);


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
    ADD CONSTRAINT series_pkey PRIMARY KEY (idseries);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;

