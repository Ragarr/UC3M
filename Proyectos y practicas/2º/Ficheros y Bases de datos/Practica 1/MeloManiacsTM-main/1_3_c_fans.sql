/* Vista fans (operatividad completa): asistentes a más de un concierto del intérprete
actual (si el intérprete tiene menos de dos conciertos, no tendrá fans). Se aportará el
email, nombre completo y edad de los fans. Si se borra un fan de esta vista, no se deben
eliminar sus datos (ni de la tabla clientes ni de la tabla asistentes) pero ese cliente será
“vetado” (dejará de aparecer en esta vista, aunque siga almacenado como cliente en la
tabla global; para este fin, se puede crear una tabla adicional que recoja qué clientes
están vetados para qué intérpretes). Si se inserta un fan, se insertará como cliente (si no
existía ya); si tiene menos de dos asistencias a conciertos del intérprete actual, se
insertará su asistencia al último o los dos últimos conciertos. Si era un fan “vetado”,
dejará de estar vetado (volverá a aparecer en la vista). Las modificaciones (update)
sobre esta vista no deberán tener efecto.  */

DROP VIEW fans CASCADE CONSTRAINTS;
DROP TABLE fans_vetados CASCADE CONSTRAINTS;

CREATE TABLE fans_vetados(
    EMAIL VARCHAR2(50) NOT NULL,
    PERFORMER VARCHAR2(50) NOT NULL,    
    CONSTRAINT PK_FANS_VETADOS PRIMARY KEY(EMAIL, PERFORMER),
    CONSTRAINT FK_EMAIL_FANS_VETADOS FOREIGN KEY(EMAIL) REFERENCES CLIENTS(e_mail),
    CONSTRAINT FK_PERFORMER_FANS_VETADOS FOREIGN KEY(PERFORMER) REFERENCES PERFORMERS(name)
);

CREATE OR REPLACE VIEW fans AS(
    SELECT CLIENTS.e_mail as e_mail, CLIENTS.NAME as name, ROUND(((SYSDATE-CLIENTS.birthdate)/365.24)) AS EDAD
    FROM (
        SELECT ATTENDANCES.CLIENT AS CLIENT, COUNT(*) AS n_asistencias, ATTENDANCES.PERFORMER AS PERFORMER
        FROM ATTENDANCES
        WHERE ATTENDANCES.PERFORMER=melopack.get_interprete_actual()
        GROUP BY ATTENDANCES.CLIENT, ATTENDANCES.PERFORMER
        HAVING COUNT(*)>1   
    ) ASISTENCIAS JOIN CLIENTS ON ASISTENCIAS.CLIENT=CLIENTS.e_mail
    WHERE ASISTENCIAS.CLIENT=CLIENTS.e_mail AND NOT EXISTS(
        SELECT * FROM fans_vetados WHERE fans_vetados.email=CLIENTS.e_mail AND fans_vetados.PERFORMER=ASISTENCIAS.PERFORMER 
    )
    AND ASISTENCIAS.PERFORMER=melopack.get_interprete_actual() 
    GROUP BY CLIENTS.e_mail, CLIENTS.NAME, ((SYSDATE-ClIENTS.birthdate)/365.24)
);
-- Si se borra un fan no se deben borrar sus datastore
CREATE OR REPLACE TRIGGER TRG_FANS_DELETE
    INSTEAD OF DELETE ON fans FOR EACH ROW
    BEGIN
        INSERT INTO fans_vetados VALUES(:OLD.e_mail, melopack.get_interprete_actual());
    END;
/
-- Si se inserta un fan se insertará como cliente (si no existe ya)
-- Si tinene menos de dos asistencias a conciertos se insertará su asistencia al último o los dos últimos conciertos
CREATE OR REPLACE TRIGGER TRG_FANS_INSERT
    INSTEAD OF INSERT ON fans FOR EACH ROW
    DECLARE
        existe_en_clientes NUMBER(1);
        existe_en_fans_vetados NUMBER(1);
        existe_en_fans NUMBER(1);
        ha_ido_al_ultimo_concierto NUMBER(1);
    BEGIN
        SELECT COUNT(*) INTO existe_en_clientes FROM CLIENTS WHERE CLIENTS.e_mail=:NEW.e_mail;
        SELECT COUNT(*) INTO existe_en_fans_vetados FROM fans_vetados WHERE fans_vetados.email=:NEW.e_mail AND fans_vetados.PERFORMER=melopack.get_interprete_actual();
        SELECT COUNT(*) INTO existe_en_fans FROM fans WHERE fans.e_mail=:NEW.e_mail;
        SELECT COUNT(*) INTO ha_ido_al_ultimo_concierto FROM ATTENDANCES WHERE ATTENDANCES.CLIENT=:NEW.e_mail AND ATTENDANCES.PERFORMER=melopack.get_interprete_actual() AND ATTENDANCES.when=(SELECT MAX(CONCERTS.when) FROM CONCERTS WHERE CONCERTS.performer=melopack.get_interprete_actual());
        IF existe_en_clientes = 0 THEN 
            -- Si no existía en clientes se mete en clientes
            INSERT INTO CLIENTS VALUES(:NEW.e_mail, :NEW.NAME, NULL, NULL, SYSDATE-:NEW.EDAD*365.24, NULL, NULL, NULL);
        ELSIF existe_en_fans_vetados > 0 THEN 
            -- Si existe en clientes y está vetado
            DELETE FROM fans_vetados WHERE fans_vetados.email=:NEW.e_mail AND fans_vetados.PERFORMER=melopack.get_interprete_actual();
        ELSIF existe_en_fans = 0 THEN
            -- Si existe en clientes, no está vetado y no es fan, entonces le añadimos asistencias
            -- El RFID debe ser único, en base a la base de datos sabemos que ningún RFID se crea con caracteres especiales
            -- Por esa razón, generaremos uno único a partir del email (que ya contiene caracteres especiales) del cliente y la fecha del sistema
            IF ha_ido_al_ultimo_concierto >0 THEN
                INSERT INTO ATTENDANCES VALUES(:NEW.e_mail, melopack.get_interprete_actual(), 
                                            (SELECT MAX(CONCERTS.when) FROM CONCERTS WHERE CONCERTS.performer=melopack.get_interprete_actual() AND 
                                            CONCERTS.when<(SELECT MAX(CONCERTS.when) FROM CONCERTS WHERE CONCERTS.performer=melopack.get_interprete_actual())), 
                                            CONCAT(:NEW.e_mail, TO_CHAR(SYSDATE, 'DD/MM/YY HH24:MI:SS')), TO_DATE(SYSDATE, 'DD/MM/YYYY'));
            ELSE
                INSERT INTO ATTENDANCES VALUES(:NEW.e_mail, melopack.get_interprete_actual(), 
                                            (SELECT MAX(CONCERTS.when) FROM CONCERTS WHERE CONCERTS.performer=melopack.get_interprete_actual()), 
                                            CONCAT(:NEW.e_mail, TO_CHAR(SYSDATE, 'DD/MM/YY HH24:MI:SS')), TO_DATE(SYSDATE, 'DD/MM/YYYY'));
                -- Llamada recursiva para que si ya está en un concierto no le añada dos asistencias, sino solo una      
                INSERT INTO fans VALUES(:NEW.e_mail, :NEW.NAME, :NEW.EDAD);    
            END IF;    
        END IF;
        -- Si existe, no está vetado y es fan, no hacemos nada
    END;
/
-- Las modificaciones update no deberán tener efecto
CREATE OR REPLACE TRIGGER TRG_FANS_UPDATE
    INSTEAD OF UPDATE ON fans FOR EACH ROW
    BEGIN
        NULL;
    END;
/
--CASOS DE PRUEBA:
-- Creamos nuevo performer
INSERT INTO PERFORMERS VALUES ('Performer Falso', 'Spanish', 'Spanish');
INSERT INTO MANAGERS VALUES('Manolo','Perez', NULL, 999999999);
INSERT INTO PUBLISHERS VALUES('Editorial Falsa', '111111111');
INSERT INTO CONCERTS VALUES('Performer Falso', TO_DATE('01/01/2020', 'DD/MM/YY'), NULL, 'Colmenarejo', NULL, NULL, 10, 2000, 999999999);
INSERT INTO CONCERTS VALUES('Performer Falso', TO_DATE('03/01/2020', 'DD/MM/YY'), NULL, 'Colmenarejo', NULL, NULL, 10, 3000, 999999999);
-- Añadimos interpretaciones
INSERT INTO PERFORMANCES VALUES('Performer Falso', TO_DATE('01/01/2020', 'DD/MM/YY'), 001, 'Shoo', 'MX>>0166063677', 1000);
INSERT INTO PERFORMANCES VALUES('Performer Falso', TO_DATE('01/01/2020', 'DD/MM/YY'), 002, 'Shoo', 'MX>>0166063677', 1000);
INSERT INTO PERFORMANCES VALUES('Performer Falso', TO_DATE('03/01/2020', 'DD/MM/YY'), 001, 'Shoo', 'MX>>0166063677', 3000);
-- Lo establecemos como interprete actual
EXECUTE melopack.asignar_interprete_actual('Performer Falso');
--Añadimos clientes
INSERT INTO CLIENTS VALUES('cliente1@mailinventado.com', 'Cliente 1', NULL, NULL, SYSDATE-20*365.24, NULL, NULL, NULL);
INSERT INTO CLIENTS VALUES('cliente2@mailinventado.com', 'Cliente 2', NULL, NULL, SYSDATE-21*365.24, NULL, NULL, NULL);
INSERT INTO CLIENTS VALUES('cliente3@mailinventado.com', 'Cliente 3', NULL, NULL, SYSDATE-22*365.24, NULL, NULL, NULL);
-- Añadimos asistencias
INSERT INTO ATTENDANCES VALUES('cliente1@mailinventado.com', 'Performer Falso', TO_DATE('01/01/2020', 'DD/MM/YY'), '1&', TO_DATE('01/01/2020', 'DD/MM/YY'));
INSERT INTO ATTENDANCES VALUES('cliente1@mailinventado.com', 'Performer Falso', TO_DATE('03/01/2020', 'DD/MM/YY'), '1&', TO_DATE('03/01/2020', 'DD/MM/YY'));
INSERT INTO ATTENDANCES VALUES('cliente2@mailinventado.com', 'Performer Falso', TO_DATE('01/01/2020', 'DD/MM/YY'), '2&', TO_DATE('01/01/2020', 'DD/MM/YY'));
-- Observamos si cliente 1 se mete en fans
SELECT * FROM fans;
-- Añadimos fans
INSERT INTO fans VALUES('cliente2@mailinventado.com', 'Cliente 2', 21);
INSERT INTO fans VALUES('cliente3@mailinventado.com', 'Cliente 3', 22);
INSERT INTO fans VALUES('cliente4@mailinventado.com', 'Cliente 4', 24);
-- Confirmamos la veracidad de los resultados
SELECT * FROM fans;
SELECT * FROM CLIENTS WHERE (CLIENTS.e_mail = 'cliente4@mailinventado.com');

-- Vetar un fan
DELETE FROM fans WHERE (e_mail='cliente1@mailinventado.com');
-- Confirmamos la veracidad de los datos
SELECT * from fans;
select * from fans_vetados;

-- Desvetar un fan
INSERT INTO fans VALUES('cliente1@mailinventado.com', 'Cliente 2', 20);

-- Restauramos la base de datos
DELETE FROM PERFORMANCES WHERE (performer='Performer Falso' AND when = TO_DATE('01/01/2020', 'DD/MM/YY') AND sequ =001);
DELETE FROM PERFORMANCES WHERE (performer='Performer Falso' AND when = TO_DATE('01/01/2020', 'DD/MM/YY') AND sequ = 002);
DELETE FROM PERFORMANCES WHERE (performer='Performer Falso' AND when = TO_DATE('03/01/2020', 'DD/MM/YY') AND sequ =001);

DELETE FROM CONCERTS WHERE (performer='Performer Falso' AND when = TO_DATE('01/01/2020', 'DD/MM/YY'));
DELETE FROM CONCERTS WHERE (performer='Performer Falso'AND when = TO_DATE('03/01/2020', 'DD/MM/YY'));
DELETE FROM MANAGERS WHERE (mobile=999999999);
DELETE FROM PUBLISHERS WHERE (name='Editorial Falsa');
DELETE FROM PERFORMERS WHERE (name='Performer Falso');

DELETE FROM ATTENDANCES WHERE (client = 'cliente1@mailinventado.com' AND performer = 'Performer Falso' AND when = TO_DATE('01/01/2020', 'DD/MM/YY'));
DELETE FROM ATTENDANCES WHERE (client = 'cliente2@mailinventado.com' AND performer = 'Performer Falso' AND when = TO_DATE('03/01/2020', 'DD/MM/YY'));
DELETE FROM ATTENDANCES WHERE (client = 'cliente3@mailinventado.com' AND performer = 'Performer Falso' AND when = TO_DATE('01/01/2020', 'DD/MM/YY'));
DELETE FROM CLIENTS WHERE (e_mail = 'cliente1@mailinventado.com');
DELETE FROM CLIENTS WHERE (e_mail = 'cliente2@mailinventado.com');
DELETE FROM CLIENTS WHERE (e_mail = 'cliente3@mailinventado.com');
DELETE FROM CLIENTS WHERE (e_mail = 'cliente4@mailinventado.com');
