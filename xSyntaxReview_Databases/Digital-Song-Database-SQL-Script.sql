CREATE TABLE "Artist" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
    "name" TEXT);

CREATE TABLE "Album" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
    artist_id INTEGER,
    "title" TEXT);

CREATE TABLE "Genre" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
    "name" TEXT);

CREATE TABLE "Track" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
    album_id INTEGER, genre_id INTEGER, len INTEGER, rating INTEGER, 
    "title" TEXT, "count" INTEGER);

INSERT INTO Artist (name) VALUES ('Kendrick Lamar');
INSERT INTO Artist (name) VALUES ('Buckethead');
INSERT INTO Artist (name) VALUES ('Led Zepplin');
INSERT INTO Artist (name) VALUES ('AC/DC');

INSERT INTO Genre (name) VALUES ('Hip-Hop/Rap');
INSERT INTO Genre (name) VALUES ('Rock');
INSERT INTO Genre (name) VALUES ('Metal');


SELECT * FROM Artist;
SELECT * FROM Genre;

----------------------------------------------------------------------


INSERT INTO Album (title, artist_id) VALUES ('To Pimp A Butterfly', 1);
INSERT INTO Album (title, artist_id) VALUES ('Hollowed Out', 2);
INSERT INTO Album (title, artist_id) VALUES ('Led Zeppelin IV', 3);
INSERT INTO Album (title, artist_id) VALUES ('Back in Black', 4);

SELECT * FROM Album;

INSERT INTO Track (title, rating, len, count, album_id, genre_id) 
    VALUES ('Misty Mountain Hop', 5, 297, 0, 3, 2) ;
INSERT INTO Track (title, rating, len, count, album_id, genre_id) 
    VALUES ('Going to California', 5, 482, 0, 3, 2) ;
INSERT INTO Track (title, rating, len, count, album_id, genre_id) 
    VALUES ('Hells Bells', 4, 313, 0, 4, 2) ;
INSERT INTO Track (title, rating, len, count, album_id, genre_id) 
    VALUES ('Low Rolling Hills', 5, 207, 0, 2, 3) ;
INSERT INTO Track (title, rating, len, count, album_id, genre_id) 
    VALUES ('Cyborg Parking', 5, 208, 0, 2, 3) ;
INSERT INTO Track (title, rating, len, count, album_id, genre_id) 
    VALUES ('Momma', 5, 209, 0, 1, 1) ;
INSERT INTO Track (title, rating, len, count, album_id, genre_id) 
    VALUES ('Institutionalized', 5, 210, 0, 1, 1) ;
   
   
SELECT * FROM Track; 

UPDATE Artist
SET name = 'Led Zeppelin'
WHERE name = 'Led Zepplin'

SELECT Album.title, Artist.name FROM Album JOIN Artist 
    ON Album.artist_id = Artist.id
    

SELECT Album.title, Album.artist_id, Artist.id, Artist.name 
    FROM Album JOIN Artist ON Album.artist_id = Artist.id
    
    

SELECT Track.title, Genre.name FROM Track JOIN Genre 
    ON Track.genre_id = Genre.id
    
    
SELECT Track.title, Artist.name, Album.title, Genre.name 
FROM Track JOIN Genre JOIN Album JOIN Artist 
    ON Track.genre_id = Genre.id AND Track.album_id = Album.id 
    AND Album.artist_id = Artist.id
