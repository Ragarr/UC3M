-- Rechazar compra de tickets por parte de clientes menores de 18 años
--TODO: VECTOR DE DATOS
DROP TABLE TMP_MENORES CASCADE CONSTRAINTS;

-- Crearmos tabla temporal para ir actualizando los menores
CREATE GLOBAL TEMPORARY TABLE TMP_MENORES(  
    new_E_MAIL VARCHAR(100) NOT NULL
); 

CREATE OR REPLACE TRIGGER TR_TICKETS_NO_MENORES BEFORE
    INSERT ON ATTENDANCES FOR EACH ROW
DECLARE
    hay_menor NUMBER(1);
BEGIN
    INSERT INTO TMP_MENORES (SELECT :NEW.CLIENT AS new_E_MAIL FROM DUAL WHERE (SYSDATE-(SELECT BIRTHDATE FROM CLIENTS WHERE CLIENTS.E_MAIL=:NEW.CLIENT)) /365.2422 < 18);
    SELECT COUNT(*) INTO hay_menor FROM TMP_MENORES WHERE new_E_MAIL = :NEW.client;
    IF hay_menor > 0 THEN
        RAISE_APPLICATION_ERROR (-20001, 'No se pueden vender tickets a menores de 18 anos');
    END IF;
END;
/
-- CASOS DE PRUEBA:
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
-- Cantidad media canciones conciertos, duracion media conciertos, periodicidad media conciertos
INSERT INTO CONCERTS VALUES('Performer Falso', TO_DATE('01/01/2020', 'DD/MM/YY'), NULL, 'Colmenarejo', NULL, NULL, 10, 2000, 999999999);
INSERT INTO CONCERTS VALUES('Performer Falso', TO_DATE('03/01/2020', 'DD/MM/YY'), NULL, 'Colmenarejo', NULL, NULL, 10, 3000, 999999999);

-- Menor de edad
SELECT *  FROM CONCERTS WHERE (PERFORMER='Performer Falso' AND WHEN=TO_DATE('01/01/2020', 'DD/MM/YY'));
INSERT INTO CLIENTS VALUES ( 'menordeedad@menor.menor', 'Pancracio', 'Perez', NULL, TO_DATE('01/01/2020', 'DD/MM/YY'), NULL, NULL, '09991223');

-- Mayor de edad
INSERT INTO CLIENTS VALUES ('mayordeedad@mayor.mayor', 'Evaristo', 'Perez', NULL, TO_DATE('01/01/1960', 'DD/MM/YY'),NULL, NULL, '09991224');

-- Intentamos añadir el menor de edad
INSERT INTO ATTENDANCES VALUES ('menordeedad@menor.menor', 'Performer Falso', TO_DATE('01/01/2020', 'DD/MM/YY'), 'rfidinventado2', NULL);

-- Intentamos añadir el mayor de edad
INSERT INTO ATTENDANCES VALUES ( 'mayordeedad@mayor.mayor', 'Performer Falso', TO_DATE('01/01/2020', 'DD/MM/YY'), 'rfidinventado1', NULL);

-- Comprobamos que no se ha metido el menor de edad y sí el mayor:
SELECT * FROM ATTENDANCES WHERE CLIENT ='menordeedad@menor.menor' OR CLIENT ='mayordeedad@mayor.mayor';

-- Restauramos la base de datos
DELETE FROM ATTENDANCES WHERE(CLIENT = 'menordeedad@menor.menor' AND PERFORMER = 'Performer Falso' AND WHEN=TO_DATE('01/01/2020', 'DD/MM/YY') );
DELETE FROM ATTENDANCES WHERE (CLIENT = 'mayordeedad@mayor.mayor' AND PERFORMER = 'Performer Falso' AND WHEN=TO_DATE('01/01/2020', 'DD/MM/YY') );
DELETE FROM CLIENTS WHERE(E_MAIL = 'menordeedad@menor.menor');
DELETE FROM CLIENTS WHERE(E_MAIL = 'mayordeedad@mayor.mayor');
DELETE FROM TRACKS WHERE (PAIR = '111111111111111' AND sequ=001);
DELETE FROM TRACKS WHERE (PAIR = '111111111111111' AND sequ=002);
DELETE FROM TRACKS WHERE (PAIR = '111111111111111' AND sequ=003);
DELETE FROM ALBUMS WHERE (PAIR='111111111111111');
DELETE FROM TRACKS WHERE (PAIR = '111111111111112' AND sequ=001);
--DELETE FROM TRACKS WHERE (PAIR = '111111111111112' AND sequ=002);
DELETE FROM TRACKS WHERE (PAIR = '111111111111112' AND sequ=003);
DELETE FROM TRACKS WHERE (PAIR = '111111111111112' AND sequ=004);
DELETE FROM ALBUMS WHERE (PAIR='111111111111112');
DELETE FROM ALBUMS WHERE (PAIR='111111111111113');
DELETE FROM CONCERTS WHERE (performer='Performer Falso' AND when = TO_DATE('01/01/2020', 'DD/MM/YY'));
DELETE FROM CONCERTS WHERE (performer='Performer Falso'AND when = TO_DATE('03/01/2020', 'DD/MM/YY'));
DELETE FROM MANAGERS WHERE (mobile=999999999);
DELETE FROM PUBLISHERS WHERE (name='Editorial Falsa');
DELETE FROM PERFORMERS WHERE (name='Performer Falso');