set wrap off;
set linesize 2000;
-- número total de canciones que cada intérprete
-- ha escrito y también ha interpretado
WITH n_canciones_interpretadas_propias AS(
    SELECT DISTINCT
        PERFORMANCES.performer AS banda,
        count('x') AS total
        FROM performances JOIN INVOLVEMENT ON 
        INVOLVEMENT.band = PERFORMANCES.performer
        WHERE INVOLVEMENT.musician = PERFORMANCES.songwriter
        GROUP BY PERFORMANCES.performer
),
-- número total de canciones que cada intérprete
-- ha interpretado
n_canciones_interpretadas AS(
    SELECT DISTINCT
        PERFORMANCES.performer AS banda,
        count('x') AS total
        FROM performances
        GROUP BY PERFORMANCES.performer
),
-- porcentaje de canciones que cada intérprete
-- ha escrito y también ha interpretado
porcentaje_canciones_interpretadas_propias AS(
    SELECT DISTINCT
        n_canciones_interpretadas_propias.banda,
        (n_canciones_interpretadas_propias.total / n_canciones_interpretadas.total)*100 AS porcentaje_canciones_interpretadas_propias
        FROM n_canciones_interpretadas_propias JOIN n_canciones_interpretadas ON
        n_canciones_interpretadas_propias.banda = n_canciones_interpretadas.banda
),
-- numero canciones grabadas
canciones_grabadas AS(
    SELECT
        ALBUMS.performer AS banda,
        TRACKS.writer AS compositor
        FROM ALBUMS JOIN TRACKS ON 
        ALBUMS.pair = TRACKS.pair
),
n_canciones_grabadas AS(
    SELECT DISTINCT
        canciones_grabadas.banda AS banda,
        COUNT('x') AS total
        FROM canciones_grabadas JOIN INVOLVEMENT ON
        INVOLVEMENT.band = canciones_grabadas.banda 
        WHERE INVOLVEMENT.musician = canciones_grabadas.compositor
        GROUP BY canciones_grabadas.banda
),
-- numero canciones grabadas propias
n_canciones_grabadas_propias AS(
    SELECT DISTINCT
        n_canciones_grabadas.banda AS banda,
        COUNT('x') AS total
        FROM n_canciones_grabadas
        GROUP BY n_canciones_grabadas.banda
),
-- porcentaje de canciones grabadas propias
porcentaje_canciones_grabadas_propias AS(
    SELECT DISTINCT
        n_canciones_grabadas_propias.banda,
        (n_canciones_grabadas_propias.total / n_canciones_grabadas.total)*100 AS porcentaje_canciones_grabadas_propias
        FROM n_canciones_grabadas_propias JOIN n_canciones_grabadas ON
        n_canciones_grabadas_propias.banda = n_canciones_grabadas.banda
)
SELECT DISTINCT
    porcentaje_canciones_interpretadas_propias.banda,
    porcentaje_canciones_interpretadas_propias.porcentaje_canciones_interpretadas_propias,
    porcentaje_canciones_grabadas_propias.porcentaje_canciones_grabadas_propias
    FROM porcentaje_canciones_interpretadas_propias JOIN porcentaje_canciones_grabadas_propias ON
    porcentaje_canciones_interpretadas_propias.banda = porcentaje_canciones_grabadas_propias.banda
    ORDER BY porcentaje_canciones_grabadas_propias.porcentaje_canciones_grabadas_propias DESC;