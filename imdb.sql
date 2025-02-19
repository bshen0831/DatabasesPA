/*

DROP DATABASE IF EXISTS moviedb;
CREATE DATABASE moviedb;
USE moviedb;
*/
DROP TABLE IF EXISTS moviedb.MotionPicture;
CREATE TABLE moviedb.MotionPicture (
  id INT NOT NULL,
  NAME VARCHAR(255),
  genre VARCHAR(255),
  rating FLOAT CHECK (rating >= 0 AND rating <= 10),
  production VARCHAR(255),
  budget INT CHECK (budget > 0),
  PRIMARY KEY (id));

DROP TABLE IF Exists moviedb.Movie;
CREATE TABLE moviedb.Movie(
    mpid INT NOT NULL,
    boxoffice_collection FLOAT CHECK (boxoffice_collection >= 0),
    PRIMARY KEY (mpid),
    FOREIGN KEY (mpid) REFERENCES moviedb.MotionPicture(id)  ON DELETE CASCADE
);

DROP TABLE IF Exists moviedb.Series;
CREATE TABLE moviedb.Series(
    mpid INT NOT NULL,
    season_count INT CHECK (season_count >= 1),
    PRIMARY KEY (mpid),
    FOREIGN KEY (mpid) REFERENCES moviedb.MotionPicture(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS moviedb.Users;
CREATE TABLE moviedb.Users (
    email VARCHAR(255) NOT NULL,
    NAME VARCHAR(255),
    age INT,
    PRIMARY KEY (email));

DROP TABLE IF EXISTS moviedb.Likes;
CREATE TABLE moviedb.Likes (
  mpid INT NOT NULL,
  uemail VARCHAR(255) NOT NULL,
  PRIMARY KEY (uemail, mpid ),
  FOREIGN KEY (uemail) REFERENCES moviedb.Users(email),
  FOREIGN KEY (mpid) REFERENCES moviedb.MotionPicture(id));


DROP TABLE IF Exists moviedb.People;
CREATE TABLE moviedb.People(
    id INT NOT NULL,
    NAME VARCHAR(255),
    nationality VARCHAR(255),
    dob DATE,
    gender CHAR(1),
    PRIMARY KEY (id) 
);

DROP TABLE IF Exists moviedb.Role;
CREATE TABLE moviedb.Role(
    mpid INT NOT NULL,
    pid INT NOT NULL,
    role_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (mpid, pid),
    FOREIGN KEY (mpid) REFERENCES moviedb.MotionPicture(id),
    FOREIGN KEY (pid) REFERENCES moviedb.People(id)
);

DROP TABLE IF Exists moviedb.Award;
CREATE TABLE moviedb.Award(
    mpid INT NOT NULL,
    pid INT NOT NULL,
    award_name VARCHAR(255) NOT NULL,
    award_year INT NOT NULL,
    PRIMARY KEY (id, pid, award_name, award_year),
    FOREIGN KEY (mpid) REFERENCES moviedb.MotionPicture(id),
    FOREIGN KEY (pid) REFERENCES moviedb.People(id)
);

DROP TABLE IF Exists moviedb.Genre;
CREATE TABLE moviedb.Genre(
    mpid INT NOT NULL,
    genre_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (mpid, genre_name),
    FOREIGN KEY (mpid) REFERENCES moviedb.MotionPicture(id)
);

DROP TABLE IF Exists moviedb.Location;
CREATE TABLE moviedb.Location(
    mpid INT NOT NULL,
    zip INT NOT NULL,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    PRIMARY KEY (mpid, zip),
    FOREIGN KEY (mpid) REFERENCES moviedb.MotionPicture(id) ON DELETE CASCADE
);