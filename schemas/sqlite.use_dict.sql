create table actors (
	idactors integer primary key,
	lname text,
	fname text, 
	mname text, 
	number integer,
	gender integer);

create table movies (
	idmovies integer primary key,
	title text,
	year integer, 
	type integer, 
	number integer,
	location text,
	language text);

create table series (
	idseries integer primary key,
	idmovies integer,
	name text,
	season integer,
	number integer);

create table aka_names (
	idaka_names integer primary key autoincrement,
	idactors integer,
	name text);

create table aka_titles (
	idaka_titles integer primary key autoincrement,
	idmovies integer,
	title text,
	location text,
	year integer);

create table acted_in (
	idacted_in integer primary key autoincrement,
	idmovies integer,
	idseries integer,
	idactors integer,
	character text,
	billing_position integer);

create table genres (
	idgenres integer primary key,
	genre text);

create table movies_genres (
	idmovies_genres integer primary key autoincrement,
	idmovies integer,
	idgenres integer);

create table keywords (
	idkeywords integer primary key,
	keyword text);

create table movies_keywords (
	idmovies_keywords integer primary key autoincrement,
	idmovies integer,
	idseries integer,
	idkeywords integer);

