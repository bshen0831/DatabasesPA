DROP DATABASE IF EXISTS IMDB;
CREATE DATABASE IMDB;
USE IMDB;

-- create table customers
DROP TABLE IF EXISTS IMDB.MotionPicture;
CREATE TABLE IMDB.MotionPicture (
  mpid INT NOT NULL,
  NAME VARCHAR,
  genre VARCHAR,
  rating FLOAT CHECK (rating >= 0 AND rating <= 10),
  production VARCHAR NULL,
  budget INT CHECK (budget > 0),
  PRIMARY KEY (mpid));

DROP TABLE IF Exists IMDB.Movie;
CREATE TABLE IMDB.Movie(
    mpid INT NOT NULL,
    boxoffice_collection FLOAT CHECK (boxoffice_collection >= 0),
    PRIMARY KEY (mpid),
    FOREIGN KEY (mpid) REFERENCES IMDB.MotionPicture(mpid)
);

DROP TABLE IF Exists IMDB.Series;
CREATE TABLE IMDB.Series(
    mpid INT NOT NULL,
    season_count INT CHECK (season_count >= 1),
    PRIMARY KEY (mpid),
    FOREIGN KEY (mpid) REFERENCES IMDB.MotionPicture(mpid)
);

DROP TABLE IF EXISTS IMDB.Users;
CREATE TABLE IMDB.Users (
  email VARCHAR NOT NULL,
    NAME VARCHAR,
    age INT,
  PRIMARY KEY (email));

DROP TABLE IF EXISTS IMDB.Likes;
CREATE TABLE IMDB.Likes (
  NAME VARCHAR NOT NULL,
  email VARCHAR NOT NULL,
  PRIMARY KEY (email, NAME )
  FOREIGN KEY (email) REFERENCES IMDB.Users(email)
  FOREIGN KEY (NAME) REFERENCES IMDB.MotionPicture(NAME));

DROP TABLE IF EXISTS IMDB.Movie;
CREATE TABLE IMDB.Movie (
  mpid INT NOT NULL,
  boxoffice_collection FLOAT CHECK (boxoffice_collection >= 0),
  PRIMARY KEY (mpid )
  FOREIGN KEY (mpid) REFERENCES IMDB.MotionPicture(id));

DROP TABLE IF Exists IMDB.People;
CREATE TABLE IMDB.People(
    pid INT NOT NULL,
    NAME VARCHAR,
    nationality VARCHAR,
    dob DATE,
    gender CHAR(1),
    PRIMARU KEY (pid) 
);

DROP TABLE IF Exists IMDB.Role;
CREATE TABLE IMDB.Role(
    mpid INT NOT NULL,
    pid INT NOT NULL,
    role_name VARCHAR NOT NULL,
    PRIMARY KEY (mpid, pid),
    FOREIGN KEY (mpid) REFERENCES IMDB.MotionPicture(mpid),
    FOREIGN KEY (pid) REFERENCES IMDB.People(pid)
);

DROP TABLE IF Exists IMDB.Award;
CREATE TABLE IMDB.Award(
    mpid INT NOT NULL,
    pid INT NOT NULL,
    award_name VARCHAR NOT NULL,
    award_year INT NOT NULL,
    PRIMARY KEY (mpid, pid, award_name, award_year),
    FOREIGN KEY (mpid) REFERENCES IMDB.MotionPict;;ure(mpid),
    FOREIGN KEY (pid) REFERENCES IMDB.People(pid)
);

DROP TABLE IF Exists IMDB.Genre;
CREATE TABLE IMDB.Gengre(
    mpid INT NOT NULL,
    genre_name VARCHAR NOT NULL,
    PRIMARY KEY (mpid, genre_name),
    FOREIGN KEY (mpid) REFERENCES IMDB.MotionPicture(mpid)
);

DROP TABLE IF Exists IMDB.Location;
CREATE TABLE IMDB.Location(
    mpid INT NOT NULL,
    zip INT NOT NULL,
    city VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    PRIMARY KEY (mpid, zip),
    FOREIGN KEY (mpid) REFERENCES IMDB.MotionPicture(mpid),
    ON DELETION CASCADE
);