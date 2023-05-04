--Para los diez intérpretes con mayor porcentaje de interpretaciones grabadas
--(canciones interpretadas en conciertos que ese mismo grupo ha grabado
--anteriormente), proporcionar la edad media de las canciones interpretadas (siendo la
--edad el tiempo transcurrido entre la grabación y la interpretación). La salida debe incluir
--el nombre del intérprete, el porcentaje de interpretaciones grabadas, y la edad media de
--las canciones (en años, meses, y días). 
WITH canciones_grabadas AS(
    SELECT DISTINCT
        ALBUMS.performer AS banda,
        TRACKS.writer AS compositor,
        TRACKS.rec_date AS fecha_grabacion
        FROM ALBUMS JOIN TRACKS ON 
        ALBUMS.pair = TRACKS.pair
),
canciones_interpretadas AS(
    SELECT DISTINCT
        PERFORMANCES.performer AS banda,
        TRACKS.writer AS compositor,
        PERFORMANCES.when AS fecha_interpretacion
        FROM PERFORMANCES JOIN TRACKS ON 
        PERFORMANCES.songtitle = TRACKS.title AND
        PERFORMANCES.songwriter = TRACKS.writer
),
canciones_grabadas_interpretadas AS(
    SELECT DISTINCT
        canciones_grabadas.banda AS banda,
        canciones_grabadas.compositor AS compositor,
        (canciones_interpretadas.fecha_interpretacion - canciones_grabadas.fecha_grabacion) AS edad
        FROM canciones_grabadas JOIN canciones_interpretadas ON
        canciones_grabadas.banda = canciones_interpretadas.banda AND
        canciones_grabadas.compositor = canciones_interpretadas.compositor
),
canciones_grabadas_interpretadas_porcentaje AS(
    SELECT DISTINCT
        canciones_grabadas_interpretadas.banda AS banda,
        COUNT(canciones_grabadas_interpretadas.compositor) AS num_canciones_grabadas_interpretadas,
        (COUNT(canciones_grabadas_interpretadas.compositor)/COUNT(canciones_grabadas.compositor))*100 AS porcentaje
        FROM canciones_grabadas_interpretadas JOIN canciones_grabadas ON
        canciones_grabadas_interpretadas.banda = canciones_grabadas.banda
        GROUP BY canciones_grabadas_interpretadas.banda
        ORDER BY porcentaje DESC
),
canciones_grabadas_interpretadas_porcentaje_edad AS(
    SELECT DISTINCT
        canciones_grabadas_interpretadas_porcentaje.banda AS banda,
        canciones_grabadas_interpretadas_porcentaje.num_canciones_grabadas_interpretadas AS n_canciones_grabadas_interpretadas,
        canciones_grabadas_interpretadas_porcentaje.porcentaje AS porcentaje,
        AVG(canciones_grabadas_interpretadas.edad) AS edad_media
        FROM canciones_grabadas_interpretadas_porcentaje JOIN canciones_grabadas_interpretadas ON
        canciones_grabadas_interpretadas_porcentaje.banda = canciones_grabadas_interpretadas.banda
        GROUP BY canciones_grabadas_interpretadas_porcentaje.banda,
        canciones_grabadas_interpretadas_porcentaje.num_canciones_grabadas_interpretadas,
        canciones_grabadas_interpretadas_porcentaje.porcentaje
)
SELECT DISTINCT
    canciones_grabadas_interpretadas_porcentaje_edad.banda,
    canciones_grabadas_interpretadas_porcentaje_edad.n_canciones_grabadas_interpretadas,
    canciones_grabadas_interpretadas_porcentaje_edad.porcentaje,
    canciones_grabadas_interpretadas_porcentaje_edad.edad_media
    FROM canciones_grabadas_interpretadas_porcentaje_edad
    ORDER BY canciones_grabadas_interpretadas_porcentaje_edad.porcentaje DESC;