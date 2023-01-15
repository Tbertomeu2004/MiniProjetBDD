DROP TABLE IF EXISTS activite;
DROP TABLE IF EXISTS localisation;

CREATE TABLE localisation (
    id_localisation INT AUTO_INCREMENT,
    nom_lieu VARCHAR(50),
    PRIMARY KEY (id_localisation)
);

CREATE TABLE activite (
    id_activite INT AUTO_INCREMENT,
    nom_activite VARCHAR(20),
    date_creation DATE,
    cout_inscription NUMERIC(5,2),
    type_activite VARCHAR(20),
    nb_participants INT,
    localisation_id INT,
    image VARCHAR(100),
    PRIMARY KEY (id_activite),
    FOREIGN KEY (localisation_id) REFERENCES localisation(id_localisation)
);

INSERT INTO localisation (id_localisation , nom_lieu) VALUES
 ( NULL, 'Gymnase IUT' ),
 ( NULL, 'Gymnase du phare' ),
 ( NULL, 'Stade d athlétisme' ),
 ( NULL, 'Site du Malsaucy' ),
 ( NULL, 'Piscine' ),
 ( NULL, 'Forge Musée Etueffont' );


INSERT INTO activite (id_activite, nom_activite, date_creation, cout_inscription, type_activite, nb_participants, localisation_id, image) VALUES
 ( NULL, 'pêche' , '2015-02-02' , 100.00 , 'loisirs', 65 , 2 , 'peche.jpg'),
 ( NULL, 'tir à l arc' , '2013-02-02', 135 , 'sport', 35 , 4 , 'tir-a-l-arc.jpg'),
 ( NULL, 'handball' , '2013-02-02', 100.00 , 'sport', 36 , 1 ,'handball.jpg'),
 ( NULL, 'Atelier musique' , '2000-02-02' , 200.00 , 'loisirs', 55 , 3 ,'musique.jpg'),
 ( NULL, 'cuisine' , '2015-02-02', 250.00 , 'loisirs' , 15 , 4 ,'cuisine.jpg'),
 ( NULL, 'Football' , '2015-02-02', 105.00 , 'sport', 105 , 3 ,'football.jpg'),
 ( NULL, 'Musculation' , '2015-02-02' , 100.00 , 'sport', 35 , 1 ,'musculation.jpg'),
 ( NULL, 'Natation' , '2014-10-25', 180 , 'sport' , 25 , 5 ,'natation.jpg'),
 ( NULL, 'Tennis' , '2015-02-01' , 200 , 'sport' , 15 , 1 , 'tennis.jpg'),
 ( NULL, 'Ping Pong' , '2000-10-20' , 130 , 'sport', 65 , 1 ,'ping-pong.jpg'),
 ( NULL, 'Escalade' , '2014-11-15' , 100, 'sport' , 35 , 2 ,'escalade.jpg'),
 ( NULL, 'zumba' , '2014-10-15', 140 , 'sport', 36 , 1,'zumba.jpg'),
 ( NULL, 'Basketball' , '2013-06-01', 120 , 'sport' , 25 , 1 ,'volleyball.jpg'),
 ( NULL, 'Volley' , '2013-05-08', 125 , 'sport' , 35 , 1 ,'volleyball.jpg'),
 ( NULL, 'Forge' , '2021-09-20', 40 , 'loisirs' , 5 , 6 ,'forge.jpg');

SELECT * FROM localisation;
SELECT * FROM activite;