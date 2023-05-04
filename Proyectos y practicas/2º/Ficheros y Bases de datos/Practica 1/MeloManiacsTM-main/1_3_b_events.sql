-- Vista events (read only): actividad en conciertos del intérprete actual, con una fila por
-- cada mes y año (con algún concierto de ese intérprete), incluyendo la cantidad de
-- conciertos (de ese mes), cantidad de espectadores, la duración media de los conciertos,
-- y cantidad media de interpretaciones.
DROP VIEW events CASCADE CONSTRAINTS;

CREATE OR REPLACE VIEW events AS
    (SELECT
        conciertos.mes_y_ano,
        n_conciertos,
        n_espectadores_totales,
        duracion_media_de_conciertos,
        ROUND(NVL(n_actuaciones / n_conciertos, 0),2) AS n_media_interpretaciones 
    FROM (
            SELECT
                TO_CHAR(PERFORMANCES.when, 'MM/YYYY') AS mes_y_ano,
                COUNT (*) AS n_actuaciones
            FROM
                PERFORMANCES 
            WHERE
                PERFORMANCES.performer = melopack.get_interprete_actual()
            GROUP BY
                TO_CHAR(PERFORMANCES.when, 'MM/YYYY')
        ) actuaciones
    RIGHT JOIN(
        SELECT 
            TO_CHAR(CONCERTS.when, 'MM/YYYY') AS mes_y_ano,
            COUNT (*) AS n_conciertos,
            SUM(attendance) AS n_espectadores_totales,
            ROUND(AVG(duration),2) AS duracion_media_de_conciertos
        FROM
            CONCERTS
        WHERE 
            CONCERTS.performer = melopack.get_interprete_actual()
        GROUP BY
            TO_CHAR(CONCERTS.when, 'MM/YYYY')
    ) conciertos
    ON conciertos.mes_y_ano = actuaciones.mes_y_ano)
    WITH READ ONLY;

--CASOS DE PRUEBA:
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
-- Añadimos interpretaciones
INSERT INTO PERFORMANCES VALUES('Performer Falso', TO_DATE('01/01/2020', 'DD/MM/YY'), 001, 'Shoo', 'MX>>0166063677', 1000);
INSERT INTO PERFORMANCES VALUES('Performer Falso', TO_DATE('01/01/2020', 'DD/MM/YY'), 002, 'Shoo', 'MX>>0166063677', 1000);
INSERT INTO PERFORMANCES VALUES('Performer Falso', TO_DATE('03/01/2020', 'DD/MM/YY'), 001, 'Shoo', 'MX>>0166063677', 3000);
-- Lo establecemos como interprete actual
EXECUTE melopack.asignar_interprete_actual('Performer Falso');

-- Mostramos la vista
SELECT * FROM events;

-- Restauramos la base de datos
DELETE FROM TRACKS WHERE (PAIR = '111111111111111' AND sequ=001);
DELETE FROM TRACKS WHERE (PAIR = '111111111111111' AND sequ=002);
DELETE FROM TRACKS WHERE (PAIR = '111111111111111' AND sequ=003);
DELETE FROM ALBUMS WHERE (PAIR='111111111111111');
DELETE FROM TRACKS WHERE (PAIR = '111111111111112' AND sequ=001);
DELETE FROM TRACKS WHERE (PAIR = '111111111111112' AND sequ=003);
DELETE FROM TRACKS WHERE (PAIR = '111111111111112' AND sequ=004);
DELETE FROM ALBUMS WHERE (PAIR='111111111111112');
DELETE FROM PERFORMANCES WHERE (performer='Performer Falso' AND when = TO_DATE('01/01/2020', 'DD/MM/YY') AND sequ =001);
DELETE FROM PERFORMANCES WHERE (performer='Performer Falso' AND when = TO_DATE('01/01/2020', 'DD/MM/YY') AND sequ = 002);
DELETE FROM PERFORMANCES WHERE (performer='Performer Falso' AND when = TO_DATE('03/01/2020', 'DD/MM/YY') AND sequ =001);

DELETE FROM CONCERTS WHERE (performer='Performer Falso' AND when = TO_DATE('01/01/2020', 'DD/MM/YY'));
DELETE FROM CONCERTS WHERE (performer='Performer Falso'AND when = TO_DATE('03/01/2020', 'DD/MM/YY'));
DELETE FROM MANAGERS WHERE (mobile=999999999);
DELETE FROM PUBLISHERS WHERE (name='Editorial Falsa');
DELETE FROM PERFORMERS WHERE (name='Performer Falso');
