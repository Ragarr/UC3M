-- 1.2.- Operatividad (paquete ‘melopack’ con procedimientos/funciones) 
-- Variable “intérprete actual (ES UN PERFORMER)” y procedimiento que permita asignarle un valor dado (parám.). 
-- Dos procedimientos para insertar y borrar álbumes y sus canciones. Es decir: 
--       > insertar nuevo álbum del intérprete actual, con una canción (track); todas las filas 
--       referenciadas deberán existir previamente, y sólo se insertan el álbum y la pista 
--       (track); 
--       > los datos necesarios (menos el intérprete, que es el actual) se proporcionan 
--       por parámetros; si el álbum (pair) ya existiera, se inserta sólo el track dado. 
--       > borrar track de un álbum; si se elimina el último track del álbum, se borrará también 
--       el registro del álbum. 
-- Informe intérprete: listar estadísticas propias (del intérprete actual) y de sus colaboradores. 
--  Este informe se sacará por pantalla mediante los procedimientos I/O adecuados (del paquete 
--  DBMS_OUTPUT) y se deberá estructurar como un informe legible. Las estadísticas propias 
--  son: núm. álbumes de cada tipo (formato), cantidad media de canciones por cada tipo, 
--  duración media del álbum por cada tipo, y periodicidad media (lapso medio entre dos 
--  publicaciones consecutivas) por cada tipo. Se añadirá la misma información para los 
--  conciertos (cantidad media de canciones, duración media de los conciertos, y periodicidad de 
--  estos). Las estadísticas de los colaboradores consisten en listar el nombre de cada uno de ellos 
--  y especificar su tipo (discográfica, estudio, ingeniero, manager), número de colaboraciones 
--  en álbumes/conciertos (en el caso de managers, listar por separado álbumes y conciertos), y 
--  qué porcentaje hace ese número con respecto al total del grupo. 
DROP PACKAGE melopack;
CREATE OR REPLACE PACKAGE melopack AS
    interprete_actual VARCHAR(50);
    PROCEDURE asignar_interprete_actual (interprete IN VARCHAR2);
    PROCEDURE insertar_nuevo_album (PAIR_param IN CHAR, format_param IN CHAR, title_param IN VARCHAR2, rel_date_param IN DATE, publisher_param IN VARCHAR2, manager_param IN NUMBER);
    PROCEDURE borrar_track_de_album (PAIR_param IN CHAR, sequ_param IN NUMBER);
    PROCEDURE informe_interprete;
    FUNCTION get_interprete_actual RETURN VARCHAR2;
END melopack;
/
CREATE OR REPLACE PACKAGE BODY melopack AS
    -- Necesario para realizar vistas externas que deban usar el interprete_actual
    FUNCTION get_interprete_actual RETURN VARCHAR2 IS
        BEGIN
            RETURN interprete_actual;
    END get_interprete_actual;
    
    PROCEDURE asignar_interprete_actual (interprete IN VARCHAR2) IS 
    existe_interprete NUMBER;    
    BEGIN
        SELECT COUNT(*) INTO existe_interprete FROM PERFORMERS WHERE name = interprete;
        IF existe_interprete > 0 THEN
            interprete_actual := interprete;
        ELSE
            DBMS_OUTPUT.PUT_LINE('El interprete no existe');
        END IF;
    END asignar_interprete_actual;
    
    PROCEDURE insertar_nuevo_album (PAIR_param IN CHAR, format_param IN CHAR, title_param  IN VARCHAR2, rel_date_param IN DATE, publisher_param IN VARCHAR2, manager_param IN NUMBER) IS
        existe_publisher NUMBER;
        existe_manager NUMBER;
        existe_claves_unicas NUMBER; 
        existe_album NUMBER;
        BEGIN
            -- Combprobamos que las filas referenciadas existen
            SELECT COUNT(*) INTO existe_publisher FROM PUBLISHERS WHERE name = publisher_param;
            SELECT COUNT(*) INTO existe_manager FROM MANAGERS WHERE mobile = manager_param;
            SELECT COUNT(*) INTO existe_claves_unicas FROM ALBUMS WHERE ALBUMS.performer = interprete_actual AND ALBUMS.format = format_param AND ALBUMS.title = title_param AND ALBUMS.rel_date = rel_date_param;
            SELECT COUNT(*) INTO existe_album FROM ALBUMS WHERE ALBUMS.pair = PAIR_param;
            IF existe_publisher > 0  THEN
                IF existe_manager > 0 THEN
                    -- Comprobamos que son unicas las claves que deben serlo
                    IF existe_claves_unicas = 0 THEN
                        -- Comprobamos que el album no existe previamente
                        IF existe_album = 0 THEN
                            INSERT INTO ALBUMS VALUES (PAIR_param, interprete_actual, format_param, title_param, rel_date_param, publisher_param, manager_param);
                            DBMS_OUTPUT.PUT_LINE('Album insertado correctamente');
                        ELSE
                            DBMS_OUTPUT.PUT_LINE('El album ya existe');
                        END IF;
                    ELSE
                        DBMS_OUTPUT.PUT_LINE('El album ya existe');
                    END IF;
                ELSE
                    DBMS_OUTPUT.PUT_LINE('El manager no existe');
                END IF;
            ELSE
                DBMS_OUTPUT.PUT_LINE('La editorial no existe');
            END IF;
        END insertar_nuevo_album;

    PROCEDURE borrar_track_de_album (PAIR_param IN CHAR, sequ_param IN NUMBER) IS
        existe_track NUMBER;
        n_tracks_album NUMBER;
        BEGIN
            SELECT COUNT(*) INTO existe_track FROM TRACKS WHERE TRACKS.PAIR = PAIR_param AND TRACKS.sequ = sequ_param;
            SELECT COUNT(*) INTO n_tracks_album FROM TRACKS WHERE TRACKS.PAIR = PAIR_param;
            -- Comprobamos que existe la track y si es la última eliminamos también el album
            IF existe_track > 0 AND n_tracks_album > 1 THEN
                DELETE FROM TRACKS WHERE TRACKS.PAIR = PAIR_param AND TRACKS.sequ = sequ_param;
            ELSIF existe_track > 0 AND n_tracks_album = 1 THEN
                DELETE FROM TRACKS WHERE TRACKS.PAIR = PAIR_param AND TRACKS.sequ = sequ_param;
                DELETE FROM ALBUMS WHERE ALBUMS.PAIR = PAIR_param;  
            ELSE
                DBMS_OUTPUT.PUT_LINE('El track no existe');
            END IF;
        END borrar_track_de_album;
    
    PROCEDURE informe_interprete IS
        num_albums_T NUMBER;
        num_albums_C NUMBER;
        num_albums_M NUMBER;
        num_albums_V NUMBER;
        num_albums_S NUMBER;
        cnt_media_canciones_albums_T NUMBER;
        cnt_media_canciones_albums_C NUMBER;
        cnt_media_canciones_albums_M NUMBER;
        cnt_media_canciones_albums_V NUMBER;
        cnt_media_canciones_albums_S NUMBER;
        dur_media_albums_T NUMBER;
        dur_media_albums_C NUMBER;
        dur_media_albums_M NUMBER;
        dur_media_albums_V NUMBER;
        dur_media_albums_S NUMBER;
        periodicidad_media_albums_T NUMBER;
        periodicidad_media_albums_C NUMBER;
        periodicidad_media_albums_M NUMBER;
        periodicidad_media_albums_V NUMBER;
        periodicidad_media_albums_S NUMBER;
        fecha_prev DATE;
        diferencia NUMBER;
        sum_diferencias NUMBER;
        num_conciertos NUMBER;
        cnt_media_canciones_conciertos NUMBER;
        dur_media_conciertos NUMBER;
        periodicidad_media_conciertos NUMBER;
        nombre_discografica VARCHAR2(25);
        nombre_estudio VARCHAR2(50);
        nombre_ingeniero VARCHAR2(50);
        nombre_manager_concierto VARCHAR2(35);
        nombre_manager_album VARCHAR2(35);
        num_colaboraciones_discografica NUMBER;
        num_colaboraciones_estudio NUMBER;
        num_colaboraciones_ingeniero NUMBER;
        num_colaboraciones_manager_albumes NUMBER;
        num_colaboraciones_manager_conciertos NUMBER;
        total_colaboraciones_discograficas NUMBER;
        total_colaboraciones_estudios NUMBER;
        total_colaboraciones_ingenieros NUMBER;
        total_colaboraciones_managers_album NUMBER;
        total_colaboraciones_managers_conciertos NUMBER;
        porcentaje_discografica NUMBER;
        porcentaje_estudio NUMBER;
        porcentaje_ingeniero NUMBER;
        porcentaje_manager_album NUMBER;
        porcentaje_manager_concierto NUMBER;
        BEGIN
            SELECT COUNT(*) INTO num_albums_T FROM ALBUMS WHERE ALBUMS.performer = interprete_actual AND ALBUMS.format = 'T';
            SELECT COUNT(*) INTO num_albums_C FROM ALBUMS WHERE ALBUMS.performer = interprete_actual AND ALBUMS.format = 'C';
            SELECT COUNT(*) INTO num_albums_M FROM ALBUMS WHERE ALBUMS.performer = interprete_actual AND ALBUMS.format = 'M';
            SELECT COUNT(*) INTO num_albums_V FROM ALBUMS WHERE ALBUMS.performer = interprete_actual AND ALBUMS.format = 'V';
            SELECT COUNT(*) INTO num_albums_S FROM ALBUMS WHERE ALBUMS.performer = interprete_actual AND ALBUMS.format = 'S';
            SELECT AVG(COUNT(*)) INTO cnt_media_canciones_albums_T FROM ALBUMS, TRACKS WHERE ALBUMS.performer = interprete_actual AND ALBUMS.format = 'T' AND ALBUMS.PAIR = TRACKS.PAIR GROUP BY ALBUMS.PAIR;
            SELECT AVG(COUNT(*)) INTO cnt_media_canciones_albums_C FROM ALBUMS, TRACKS WHERE ALBUMS.performer = interprete_actual AND ALBUMS.format = 'C' AND ALBUMS.PAIR = TRACKS.PAIR GROUP BY ALBUMS.PAIR;
            SELECT AVG(COUNT(*)) INTO cnt_media_canciones_albums_M FROM ALBUMS, TRACKS WHERE ALBUMS.performer = interprete_actual AND ALBUMS.format = 'M' AND ALBUMS.PAIR = TRACKS.PAIR GROUP BY ALBUMS.PAIR;
            SELECT AVG(COUNT(*)) INTO cnt_media_canciones_albums_V FROM ALBUMS, TRACKS WHERE ALBUMS.performer = interprete_actual AND ALBUMS.format = 'V' AND ALBUMS.PAIR = TRACKS.PAIR GROUP BY ALBUMS.PAIR;
            SELECT AVG(COUNT(*)) INTO cnt_media_canciones_albums_S FROM ALBUMS, TRACKS WHERE ALBUMS.performer = interprete_actual AND ALBUMS.format = 'S' AND ALBUMS.PAIR = TRACKS.PAIR GROUP BY ALBUMS.PAIR;
            
            SELECT SUM(duration) / COUNT(DISTINCT albums.PAIR) INTO dur_media_albums_T FROM TRACKS JOIN albums ON TRACKS.PAIR = albums.PAIR WHERE albums.format = 'T' AND albums.performer = interprete_actual;
            SELECT SUM(duration) / COUNT(DISTINCT albums.PAIR) INTO dur_media_albums_C FROM TRACKS JOIN albums ON TRACKS.PAIR = albums.PAIR WHERE albums.format = 'C' AND albums.performer = interprete_actual;
            SELECT SUM(duration) / COUNT(DISTINCT albums.PAIR) INTO dur_media_albums_M FROM TRACKS JOIN albums ON TRACKS.PAIR = albums.PAIR WHERE albums.format = 'M' AND albums.performer = interprete_actual;
            SELECT SUM(duration) / COUNT(DISTINCT albums.PAIR) INTO dur_media_albums_V FROM TRACKS JOIN albums ON TRACKS.PAIR = albums.PAIR WHERE albums.format = 'V' AND albums.performer = interprete_actual;
            SELECT SUM(duration) / COUNT(DISTINCT albums.PAIR) INTO dur_media_albums_S FROM TRACKS JOIN albums ON TRACKS.PAIR = albums.PAIR WHERE albums.format = 'S' AND albums.performer = interprete_actual;

            sum_diferencias := 0;
            fecha_prev := NULL;
            FOR row IN (SELECT rec_date FROM TRACKS JOIN ALBUMS on TRACKS.pair = ALBUMS.pair WHERE ALBUMS.format = 'T' AND ALBUMS.performer=interprete_actual ORDER BY rec_date ASC) LOOP
                IF fecha_prev IS NOT NULL THEN
                    diferencia := row.rec_date - fecha_prev;
                    sum_diferencias := sum_diferencias + diferencia;
                END IF;
                fecha_prev := row.rec_date;
            END LOOP;
            IF num_albums_T > 1 THEN
                periodicidad_media_albums_T := sum_diferencias / (num_albums_T-1);
            END IF;
            sum_diferencias := 0;
            fecha_prev := NULL;
            FOR row IN (SELECT rec_date FROM TRACKS JOIN ALBUMS on TRACKS.pair = ALBUMS.pair WHERE ALBUMS.format = 'C' AND ALBUMS.performer=interprete_actual ORDER BY rec_date ASC) LOOP
                IF fecha_prev IS NOT NULL THEN
                    diferencia := row.rec_date - fecha_prev;
                    sum_diferencias := sum_diferencias + diferencia;
                END IF;
                fecha_prev := row.rec_date;
            END LOOP;
            IF num_albums_C > 1 THEN
                periodicidad_media_albums_C := sum_diferencias / (num_albums_C-1);
            END IF;
            sum_diferencias := 0;
            fecha_prev := NULL;
            FOR row IN (SELECT rec_date FROM TRACKS JOIN ALBUMS on TRACKS.pair = ALBUMS.pair WHERE ALBUMS.format = 'M' AND ALBUMS.performer=interprete_actual ORDER BY rec_date ASC) LOOP
                IF fecha_prev IS NOT NULL THEN
                    diferencia := row.rec_date - fecha_prev;
                    sum_diferencias := sum_diferencias + diferencia;
                END IF;
                fecha_prev := row.rec_date;
            END LOOP;
            IF num_albums_M > 1 THEN
                periodicidad_media_albums_M := sum_diferencias / (num_albums_M-1);
            END IF;
            sum_diferencias := 0;
            fecha_prev := NULL;
            FOR row IN (SELECT rec_date FROM TRACKS JOIN ALBUMS on TRACKS.pair = ALBUMS.pair WHERE ALBUMS.format = 'V' AND ALBUMS.performer=interprete_actual ORDER BY rec_date ASC) LOOP
                IF fecha_prev IS NOT NULL THEN
                    diferencia := row.rec_date - fecha_prev;
                    sum_diferencias := sum_diferencias + diferencia;
                END IF;
                fecha_prev := row.rec_date;
            END LOOP;
            IF num_albums_V > 1 THEN
                periodicidad_media_albums_V := sum_diferencias / (num_albums_V-1);
            END IF;
            sum_diferencias := 0;
            fecha_prev := NULL;
            FOR row IN (SELECT rec_date FROM TRACKS JOIN ALBUMS on TRACKS.pair = ALBUMS.pair WHERE ALBUMS.format = 'S' AND ALBUMS.performer=interprete_actual ORDER BY rec_date ASC) LOOP
                IF fecha_prev IS NOT NULL THEN
                    diferencia := row.rec_date - fecha_prev;
                    sum_diferencias := sum_diferencias + diferencia;
                END IF; 
                fecha_prev := row.rec_date;
            END LOOP;
            IF num_albums_S > 1 THEN
                periodicidad_media_albums_S := sum_diferencias / (num_albums_S-1);
            END IF;
            sum_diferencias := 0;
            fecha_prev := NULL;
            
            SELECT COUNT(*) INTO num_conciertos FROM CONCERTS WHERE CONCERTS.performer = interprete_actual;
            SELECT AVG(COUNT(*)) INTO cnt_media_canciones_conciertos FROM CONCERTS, PERFORMANCES WHERE CONCERTS.performer = interprete_actual AND CONCERTS.performer = PERFORMANCES.performer AND CONCERTS.when = PERFORMANCES.when GROUP BY CONCERTS.when;
           
            SELECT AVG(CONCERTS.duration) INTO dur_media_conciertos FROM CONCERTS WHERE CONCERTS.performer = interprete_actual;
            FOR row IN (SELECT CONCERTS.when as cuando FROM CONCERTS WHERE CONCERTS.performer=interprete_actual ORDER BY cuando ASC) LOOP
                IF fecha_prev IS NOT NULL THEN
                    diferencia := row.cuando - fecha_prev;
                    sum_diferencias := sum_diferencias + diferencia;
                END IF;
                fecha_prev := row.cuando;
            END LOOP;
            IF num_conciertos > 1 THEN
                periodicidad_media_conciertos := sum_diferencias / (num_conciertos-1);
            END IF;
            -- Informe de las estadísticas propias
            DBMS_OUTPUT.PUT_LINE('ESTADISTICAS PROPIAS DEL INTERPRETE ' || interprete_actual);
            DBMS_OUTPUT.PUT_LINE('Numero de albumes de tipo streamig: ' || num_albums_T);
            DBMS_OUTPUT.PUT_LINE('Numero de albumes de tipo CD: ' || num_albums_C);
            DBMS_OUTPUT.PUT_LINE('Numero de albumes de tipo audio file: ' || num_albums_M);
            DBMS_OUTPUT.PUT_LINE('Numero de albumes de tipo vinyl: ' || num_albums_V);
            DBMS_OUTPUT.PUT_LINE('Numero de albumes de tipo single: ' || num_albums_S);
            DBMS_OUTPUT.PUT_LINE('Numero medio de canciones por album de tipo streaming: ' || ROUND(cnt_media_canciones_albums_T,2));
            DBMS_OUTPUT.PUT_LINE('Numero medio de canciones por album de tipo cd: ' || ROUND(cnt_media_canciones_albums_C,2));
            DBMS_OUTPUT.PUT_LINE('Numero medio de canciones por album de tipo audio file: ' || ROUND(cnt_media_canciones_albums_M,2));
            DBMS_OUTPUT.PUT_LINE('Numero medio de canciones por album de tipo vinyl: ' || ROUND(cnt_media_canciones_albums_V,2));
            DBMS_OUTPUT.PUT_LINE('Numero medio de canciones por album de tipo single: ' || ROUND(cnt_media_canciones_albums_S,2));
            DBMS_OUTPUT.PUT_LINE('Duracion media de los albums de tipo streaming (segundos): ' || ROUND(dur_media_albums_T,2));
            DBMS_OUTPUT.PUT_LINE('Duracion media de los albums de tipo cd (segundos): ' || ROUND(dur_media_albums_C,2));
            DBMS_OUTPUT.PUT_LINE('Duracion media de los albums de tipo audio file (segundos): ' || ROUND(dur_media_albums_M,2));
            DBMS_OUTPUT.PUT_LINE('Duracion media de los albums de tipo vinyl (segundos): ' || ROUND(dur_media_albums_V,2));
            DBMS_OUTPUT.PUT_LINE('Duracion media de los albums de tipo single (segundos): ' || ROUND(dur_media_albums_S,2));
            DBMS_OUTPUT.PUT_LINE('Periodicidad media de lanzamiento de albumes de tipo streaming (dias): ' || ROUND(periodicidad_media_albums_T,2));
            DBMS_OUTPUT.PUT_LINE('Periodicidad media de lanzamiento de albumes de tipo cd (dias): ' || ROUND(periodicidad_media_albums_C,2));
            DBMS_OUTPUT.PUT_LINE('Periodicidad media de lanzamiento de albumes de tipo audio file (dias): ' || ROUND(periodicidad_media_albums_M,2));
            DBMS_OUTPUT.PUT_LINE('Periodicidad media de lanzamiento de albumes de tipo vinyl (dias): ' || ROUND(periodicidad_media_albums_V,2));
            DBMS_OUTPUT.PUT_LINE('Periodicidad media de lanzamiento de albumes de tipo single (dias): ' || ROUND(periodicidad_media_albums_S,2));
            DBMS_OUTPUT.PUT_LINE('Numero de conciertos: ' || num_conciertos);
            DBMS_OUTPUT.PUT_LINE('Numero medio de canciones por concierto: ' || ROUND(cnt_media_canciones_conciertos,2));
            DBMS_OUTPUT.PUT_LINE('Duracion media de conciertos: (segundos) ' || ROUND(dur_media_conciertos,2));
            DBMS_OUTPUT.PUT_LINE('Periodicidad media de lanzamiento de conciertos (dias): ' || ROUND(periodicidad_media_conciertos,2));
            
            -- Calculo de las estadísticas de los colaboradores 
            -- Discográficas
            DBMS_OUTPUT.PUT_LINE('- ');
            DBMS_OUTPUT.PUT_LINE('ESTADISTICAS DE LAS DISCOGRAFICAS');
            SELECT COUNT('X') INTO total_colaboraciones_discograficas FROM ALBUMS WHERE ALBUMS.performer = interprete_actual;
            FOR row IN (SELECT DISTINCT ALBUMS.publisher INTO nombre_discografica FROM ALBUMS WHERE ALBUMS.performer = interprete_actual) LOOP
                nombre_discografica := row.publisher;
                SELECT COUNT('X') INTO num_colaboraciones_discografica FROM ALBUMS WHERE ALBUMS.publisher = nombre_discografica AND ALBUMS.performer = interprete_actual;
                porcentaje_discografica := 0;
                IF num_colaboraciones_discografica > 0 THEN
                    porcentaje_discografica := (num_colaboraciones_discografica / total_colaboraciones_discograficas) * 100;
                ELSE
                    porcentaje_discografica := 0;
                END IF;
                DBMS_OUTPUT.PUT_LINE('Nombre: ' || nombre_discografica); 
                DBMS_OUTPUT.PUT_LINE('Numero de colaboraciones en albumes: ' || num_colaboraciones_discografica);
                DBMS_OUTPUT.PUT_LINE('Porcentaje de colaboraciones respecto al total de discograficas: ' || ROUND(porcentaje_discografica, 2));
                DBMS_OUTPUT.PUT_LINE('- ');
            END LOOP;
            -- Estudios
            DBMS_OUTPUT.PUT_LINE('- ');
            DBMS_OUTPUT.PUT_LINE('ESTADISTICAS DE LOS ESTUDIOS');
            SELECT COUNT('X') INTO total_colaboraciones_estudios FROM TRACKS INNER JOIN ALBUMS ON TRACKS.PAIR = ALBUMS.PAIR WHERE ALBUMS.performer = interprete_actual;
            FOR row IN (SELECT DISTINCT TRACKS.studio INTO nombre_estudio FROM TRACKS INNER JOIN ALBUMS ON TRACKS.PAIR = ALBUMS.PAIR WHERE ALBUMS.performer = interprete_actual) LOOP
                nombre_estudio := row.studio;
                SELECT COUNT('X') INTO num_colaboraciones_estudio FROM TRACKS INNER JOIN ALBUMS ON ALBUMS.PAIR = TRACKS.PAIR WHERE TRACKS.studio = row.studio AND ALBUMS.performer = interprete_actual;
                IF num_colaboraciones_estudio > 0 THEN
                    porcentaje_estudio := (num_colaboraciones_estudio / total_colaboraciones_estudios) * 100;
                ELSE
                    porcentaje_estudio := 0;
                END IF;
                DBMS_OUTPUT.PUT_LINE('Nombre: ' || nombre_estudio);
                DBMS_OUTPUT.PUT_LINE('Numero de colaboraciones en albumes: ' || num_colaboraciones_estudio);
                DBMS_OUTPUT.PUT_LINE('Porcentaje de colaboraciones respecto al total de estudios: ' || ROUND(porcentaje_estudio, 2));
                DBMS_OUTPUT.PUT_LINE('- ');
            END LOOP;
            -- Ingenieros
            DBMS_OUTPUT.PUT_LINE('- ');
            DBMS_OUTPUT.PUT_LINE('ESTADISTICAS DE LOS INGENIEROS');
            SELECT COUNT('X') INTO total_colaboraciones_ingenieros FROM TRACKS INNER JOIN ALBUMS ON TRACKS.PAIR = ALBUMS.PAIR WHERE ALBUMS.performer = interprete_actual;
            FOR row IN (SELECT DISTINCT TRACKS.engineer INTO nombre_ingeniero FROM TRACKS INNER JOIN ALBUMS ON TRACKS.PAIR = ALBUMS.PAIR WHERE ALBUMS.performer = interprete_actual) LOOP
                nombre_ingeniero := row.engineer;
                SELECT COUNT('X') INTO num_colaboraciones_ingeniero FROM TRACKS INNER JOIN ALBUMS ON ALBUMS.PAIR = TRACKS.PAIR WHERE TRACKS.engineer = row.engineer AND ALBUMS.performer = interprete_actual;
                IF num_colaboraciones_ingeniero > 0 THEN
                    porcentaje_ingeniero := (num_colaboraciones_ingeniero / total_colaboraciones_ingenieros) * 100;
                ELSE
                    porcentaje_ingeniero := 0;
                END IF;
                DBMS_OUTPUT.PUT_LINE('Nombre: ' || nombre_ingeniero);
                DBMS_OUTPUT.PUT_LINE('Numero de colaboraciones en albumes: ' || num_colaboraciones_ingeniero);
                DBMS_OUTPUT.PUT_LINE('Porcentaje de colaboraciones respecto al total de ingenieros: ' || ROUND(porcentaje_ingeniero, 2));
                DBMS_OUTPUT.PUT_LINE('- ');
            END LOOP;
            -- Managers en conciertos
            DBMS_OUTPUT.PUT_LINE('- ');
            DBMS_OUTPUT.PUT_LINE('ESTADISTICAS DE LOS MANAGERS EN CONCIERTOS');
            SELECT COUNT('X') INTO total_colaboraciones_managers_conciertos FROM CONCERTS WHERE CONCERTS.performer = interprete_actual;
            FOR row IN (SELECT DISTINCT MANAGERS.name, MANAGERS.mobile FROM CONCERTS INNER JOIN MANAGERS ON CONCERTS.manager=MANAGERS.mobile  WHERE CONCERTS.performer = interprete_actual) LOOP
                SELECT COUNT('X') INTO num_colaboraciones_manager_conciertos FROM CONCERTS WHERE CONCERTS.manager = row.mobile AND CONCERTS.performer = interprete_actual;
                IF num_colaboraciones_manager_conciertos > 0 THEN
                    porcentaje_manager_concierto := (num_colaboraciones_manager_conciertos / total_colaboraciones_managers_conciertos) * 100;
                ELSE 
                    porcentaje_manager_concierto := 0;
                END IF; 
                DBMS_OUTPUT.PUT_LINE('Nombre: ' || row.name);
                DBMS_OUTPUT.PUT_LINE('Numero de colaboraciones en conciertos: ' || num_colaboraciones_manager_conciertos);
                DBMS_OUTPUT.PUT_LINE('Porcentaje de colaboraciones respecto al total de managers: ' || ROUND(porcentaje_manager_concierto, 2));
                DBMS_OUTPUT.PUT_LINE('- ');
            END LOOP;
            -- Managers en albumes
            DBMS_OUTPUT.PUT_LINE('- ');
            DBMS_OUTPUT.PUT_LINE('ESTADISTICAS DE LOS MANAGERES EN ALBUMES');
            SELECT COUNT('X') INTO total_colaboraciones_managers_album FROM ALBUMS WHERE ALBUMS.performer = interprete_actual;
            FOR row IN (SELECT DISTINCT MANAGERS.name, MANAGERS.mobile  FROM ALBUMS INNER JOIN MANAGERS ON ALBUMS.manager = MANAGERS.mobile WHERE ALBUMS.performer = interprete_actual) LOOP
                SELECT COUNT('X') INTO num_colaboraciones_manager_albumes FROM ALBUMS WHERE ALBUMS.manager = row.mobile AND ALBUMS.performer = interprete_actual;
                IF num_colaboraciones_manager_albumes > 0 THEN
                    porcentaje_manager_album := (num_colaboraciones_manager_albumes / total_colaboraciones_managers_album) * 100;
                ELSE 
                    porcentaje_manager_album := 0;
                END IF;
                DBMS_OUTPUT.PUT_LINE('Nombre: ' || row.name);
                DBMS_OUTPUT.PUT_LINE('Numero de colaboraciones en albumes: ' || num_colaboraciones_manager_albumes);
                DBMS_OUTPUT.PUT_LINE('Porcentaje de colaboraciones respecto al total de managers de albumes: ' || ROUND(porcentaje_manager_album,2));
                DBMS_OUTPUT.PUT_LINE('- ');
            END LOOP;
    END informe_interprete;
END melopack;
/
-- CASOS DE PRUEBA:
-- EJECCUCION DE LAS FUNCIONES
-- ASIGNAR INTERPRETE
EXECUTE melopack.asignar_interprete_actual('Manuel');
-- INFORME INTERPRETE
EXECUTE melopack.informe_interprete;
-- Creamos nuevo performer para comprobar la validez de los resultados de forma sencilla

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
EXECUTE melopack.asignar_interprete_actual('Performer Falso');
EXECUTE melopack.informe_interprete;
-- Borramos una track de un album para probar el procedimiento: 
EXECUTE melopack.borrar_track_de_album('111111111111111', 002);
-- La sequ 002 no debe salir
SELECT * FROM TRACKS WHERE TRACKS.pair = '111111111111111';
--Añadimos un album para probar el procedimiento
EXECUTE melopack.insertar_nuevo_album('111111111111113', 'T', 'Album Falso', TO_DATE('04/01/2020', 'DD/MM/YY'), 'Editorial Falsa', 999999999);
-- Debería aparacere
SELECT * FROM ALBUMS WHERE ALBUMS.PAIR = '111111111111113';
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
DELETE FROM ALBUMS WHERE (PAIR='111111111111113');
DELETE FROM CONCERTS WHERE (performer='Performer Falso' AND when = TO_DATE('01/01/2020', 'DD/MM/YY'));
DELETE FROM CONCERTS WHERE (performer='Performer Falso'AND when = TO_DATE('03/01/2020', 'DD/MM/YY'));
DELETE FROM MANAGERS WHERE (mobile=999999999);
DELETE FROM PUBLISHERS WHERE (name='Editorial Falsa');
DELETE FROM PERFORMERS WHERE (name='Performer Falso');
