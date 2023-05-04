-- Impedir que se inserte en ‘songs’ la misma canción con sus autores al revés. 

CREATE GLOBAL TEMPORARY TABLE TMP_SONGS(
    oldref_w VARCHAR(14),
    newref_w VARCHAR(14),
    oldref_c VARCHAR(14),
    newref_c VARCHAR(14),
    oldref_title VARCHAR(50),
    newref_title VARCHAR(50)
);
CREATE OR REPLACE TRIGGER TR_SAME_WRITERS_1 BEFORE
    INSERT ON songs FOR EACH ROW
BEGIN
    INSERT INTO TMP_SONGS VALUES (:OLD.writer, :NEW.writer, :OLD.cowriter, :NEW.cowriter, :OLD.title, :NEW.title);
END;
/
CREATE OR REPLACE TRIGGER TR_SAME_WRITERS_2 BEFORE
    INSERT ON songs FOR EACH ROW
BEGIN
    FOR row IN (SELECT * FROM TMP_SONGS) LOOP 
        IF :NEW.writer = row.newref_c AND :NEW.cowriter = row.newref_w AND :NEW.title = row.newref_title THEN
            RAISE_APPLICATION_ERROR(-20001, 'No se puede insertar la misma cancion con sus autores al reves');
        END IF;
    END LOOP;
END;
/
-- CASOS DE PRUEBA:
INSERT INTO SONGS VALUES('CancionFalsa', 'GR>>0857117612', 'IT>>0000272692');
-- Intentamos añadir la misma canción con sus autores al revés
INSERT INTO SONGS VALUES('CancionFalsa', 'IT>>0000272692' , 'GR>>0857117612');
-- Mostramos el resultado obtenido
SELECT * FROM SONGS WHERE title = 'CancionFalsa';
-- Dejamos la base de datos igual
DELETE FROM SONGS WHERE (title = 'CancionFalsa' AND writer = 'GR>>0857117612');
DELETE FROM SONGS WHERE (title = 'CancionFalsa' AND writer = 'IT>>0000272692');