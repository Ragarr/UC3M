--Vista my_albums (read only): lista los álbumes (con duración total) del intérprete actual. 
DROP VIEW my_albums CASCADE CONSTRAINTS;

CREATE OR REPLACE VIEW my_albums AS
    (SELECT
        TRACKS.PAIR,
        SUM(duration) AS total_duration
    FROM
        TRACKS JOIN ALBUMS ON TRACKS.pair = ALBUMS.pair
    WHERE
        ALBUMS.performer = melopack.get_interprete_actual()
    GROUP BY
        TRACKS.PAIR)
    WITH READ ONLY;
        
-- CASOS DE PRUEBA:
-- Creamos nuevo performer
INSERT INTO PERFORMERS VALUES ('Performer Falso', 'Spanish', 'Spanish');
INSERT INTO MANAGERS VALUES('Manolo','Perez', NULL, 999999999);
INSERT INTO PUBLISHERS VALUES('Editorial Falsa', '111111111');
INSERT INTO ALBUMS VALUES('111111111111111', 'Performer Falso', 'T', 'Album Falso',TO_DATE('01/01/2020', 'DD/MM/YY'), 'Editorial Falsa', 999999999);
INSERT INTO TRACKS VALUES('111111111111111', 001, 'Shoo', 'MX>>0166063677', 200, TO_DATE('01/02/2020', 'DD/MM/YY'), 'Cervantes Recordings', 'Raul Aguilar Arroyo');
INSERT INTO TRACKS VALUES('111111111111111', 002, 'Shoo', 'MX>>0166063677', 300, TO_DATE('01/02/2020', 'DD/MM/YY'), 'Cervantes Recordings', 'Raul Aguilar Arroyo');
INSERT INTO TRACKS VALUES('111111111111111', 003, 'Shoo', 'MX>>0166063677', 400, TO_DATE('01/02/2020', 'DD/MM/YY'), 'Cervantes Recordings', 'Raul Aguilar Arroyo');
INSERT INTO ALBUMS VALUES('111111111111112', 'Performer Falso', 'T', 'Album Falso',TO_DATE('03/01/2020', 'DD/MM/YY'), 'Editorial Falsa', 999999999);
INSERT INTO TRACKS VALUES('111111111111112', 001, 'Shoo', 'MX>>0166063677', 200, TO_DATE('03/02/2020', 'DD/MM/YY'), 'Cervantes Recordings', 'Raul Aguilar Arroyo');
INSERT INTO TRACKS VALUES('111111111111112', 002, 'Shoo', 'MX>>0166063677', 300, TO_DATE('03/02/2020', 'DD/MM/YY'), 'Cervantes Recordings', 'Raul Aguilar Arroyo');
INSERT INTO TRACKS VALUES('111111111111112', 003, 'Shoo', 'MX>>0166063677', 400, TO_DATE('03/02/2020', 'DD/MM/YY'), 'Cervantes Recordings', 'Raul Aguilar Arroyo');
INSERT INTO TRACKS VALUES('111111111111112', 004, 'Shoo', 'MX>>0166063677', 100, TO_DATE('03/02/2020', 'DD/MM/YY'), 'Cervantes Recordings', 'Raul Aguilar Arroyo');
INSERT INTO CONCERTS VALUES('Performer Falso', TO_DATE('01/01/2020', 'DD/MM/YY'), NULL, 'Colmenarejo', NULL, NULL, 10, 2000, 999999999);
INSERT INTO CONCERTS VALUES('Performer Falso', TO_DATE('03/01/2020', 'DD/MM/YY'), NULL, 'Colmenarejo', NULL, NULL, 10, 3000, 999999999);
-- Lo establecemos como interprete actual
EXECUTE melopack.asignar_interprete_actual('Performer Falso');
-- mostrar vista
SELECT * FROM my_albums;

-- Restauramos la base de datos
DELETE FROM TRACKS WHERE (PAIR = '111111111111111' AND sequ=001);
DELETE FROM TRACKS WHERE (PAIR = '111111111111111' AND sequ=002);
DELETE FROM TRACKS WHERE (PAIR = '111111111111111' AND sequ=003);
DELETE FROM ALBUMS WHERE (PAIR='111111111111111');
DELETE FROM TRACKS WHERE (PAIR = '111111111111112' AND sequ=001);
--DELETE FROM TRACKS WHERE (PAIR = '111111111111112' AND sequ=002);
DELETE FROM TRACKS WHERE (PAIR = '111111111111112' AND sequ=003);
DELETE FROM TRACKS WHERE (PAIR = '111111111111112' AND sequ=004);
DELETE FROM ALBUMS WHERE (PAIR='111111111111112');
DELETE FROM CONCERTS WHERE (performer='Performer Falso' AND when = TO_DATE('01/01/2020', 'DD/MM/YY'));
DELETE FROM CONCERTS WHERE (performer='Performer Falso'AND when = TO_DATE('03/01/2020', 'DD/MM/YY'));
DELETE FROM MANAGERS WHERE (mobile=999999999);
DELETE FROM PUBLISHERS WHERE (name='Editorial Falsa');
DELETE FROM PERFORMERS WHERE (name='Performer Falso');

--Intentamos insertar a través de la vista. No dejará porque es de solo lectura
--INSERT INTO my_albums VALUES('111111111111114', 1000);

--RESULTADO OBTENIDO: ORA-42399: no se puede realizar una operacion DML en una vista de solo lectura