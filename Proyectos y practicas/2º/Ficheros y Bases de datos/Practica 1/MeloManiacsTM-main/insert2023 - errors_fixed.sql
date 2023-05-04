-- -----------------------------------------
-- FSDB Assignments on Relational DB '2023
-- -----------------------------------------
-- -----------------------------------------
-- 1st assignment - --- LOAD SCRIPT --- ----
-- -----------------------------------------

--  GENERAL IMPLICIT assumptions: the format of dates within strings is 'dd-mm-yyyy'

-- -----------------------------------------
-- loading auxiliary tables
-- -----------------------------------------

INSERT INTO LANGUAGES(name) (SELECT DISTINCT band_language FROM fsdb.artists WHERE band_language is not null);
-- 3 rows created

INSERT INTO NATIONALITIES(name) (SELECT DISTINCT nationality FROM fsdb.artists WHERE nationality is not null);
-- 17 rows created

INSERT INTO MANAGERS(name,f_name,surname,mobile) 
   (SELECT DISTINCT manager_name,man_fam_name,man_surname,man_mobile FROM fsdb.recordings
       WHERE man_mobile is not null and manager_name is not null and man_fam_name is not null
    UNION   
    SELECT DISTINCT manager_name,man_fam_name,man_surname,man_mobile FROM fsdb.livesingings 
       WHERE man_mobile is not null and manager_name is not null and man_fam_name is not null);
-- 127 rows created

INSERT INTO PUBLISHERS(name,phone) 
   (SELECT DISTINCT publisher,pub_phone FROM fsdb.recordings WHERE publisher is not null and pub_phone is not null);
-- 30 rows created

INSERT INTO STUDIOS(name,address) 
   (SELECT DISTINCT studio,stud_address FROM fsdb.recordings WHERE studio is not null and stud_address is not null);
-- 40 rows created


-- -----------------------------------------
-- loading tables regarding musicians part
-- -----------------------------------------

-- assuming all performers and musicians are in fsdb.artists (as explicitly stated); can be checked
INSERT INTO PERFORMERS(name,nationality,language) 
   (SELECT DISTINCT band,band_nation,band_language FROM fsdb.artists 
       WHERE band is not null and band_nation is not null and band_language is not null);
-- 695 rows created

INSERT INTO MUSICIANS(name,passport,birthdate,nationality) 
   (SELECT DISTINCT musician,passport,to_date(birthdate,'dd-mm-yyyy'),nationality FROM fsdb.artists 
       WHERE musician is not null and passport is not null and birthdate is not null and nationality is not null);
-- 1649 rows created

-- INSERT INTO INVOLVEMENT(band,musician,role,start_d,end_d) 
--   (SELECT DISTINCT band,passport,role,to_date(start_date,'dd-mm-yyyy'),to_date(end_date,'dd-mm-yyyy') FROM fsdb.artists;
-- Error detected: band is null for many musicians
-- IMPLICIT SEMANTIC ASSUMPTION: if band is null, it is assumed that it is a songwriter (not part of a band nor solist)
-- Error detected: membership with startdate greater than enddate
-- IMPLICIT SEMANTIC ASSUMPTION: if startdate is greater than end_date, it is assumed they are reversed
-- that is, (star_d <- end_date) AND (end_d <- start_date)
INSERT INTO INVOLVEMENT(band,musician,role,start_d,end_d) 
   (SELECT DISTINCT band,passport,role,to_date(end_date,'dd-mm-yyyy'),to_date(start_date,'dd-mm-yyyy') FROM fsdb.artists  
       WHERE band is not null and end_date is not null and to_date(start_date,'dd-mm-yyyy')>to_date(end_date,'dd-mm-yyyy'));
-- 1 rows created

-- Error detected: membership with null startdate 
-- IMPLICIT SEMANTIC ASSUMPTION: if startdate is null, it will be substituted by that musician's birthdate
INSERT INTO INVOLVEMENT(band,musician,role,start_d,end_d) 
   (SELECT DISTINCT band,passport,role,to_date(birthdate,'dd-mm-yyyy'),to_date(end_date,'dd-mm-yyyy') 
       FROM fsdb.artists WHERE band is not null and start_date is null );
-- 1 rows created

-- The rest of the rows:
INSERT INTO INVOLVEMENT(band,musician,role,start_d,end_d) 
   (SELECT DISTINCT band,passport,role,to_date(start_date,'dd-mm-yyyy'),to_date(end_date,'dd-mm-yyyy') FROM fsdb.artists  
       WHERE band is not null and start_date is not null 
	         and (end_date is null or to_date(start_date,'dd-mm-yyyy')<=to_date(end_date,'dd-mm-yyyy')));
-- 1222 rows created

-- -----------------------------------------
-- loading tables regarding recordings part
-- -----------------------------------------

-- IMPLICIT semantic assumption: any format different (from the ones in the statement) is an audio file, typed 'M'
INSERT INTO ALBUMS(PAIR,performer,format,title,rel_date,publisher,manager) 
(SELECT DISTINCT album_pair,performer,decode(UPPER(format),'STREAMING','T','CD','C','VYNIL','V','SINGLE','S','M'),
        album_title,to_date(release_date,'dd-mm-yyyy'),publisher,man_mobile
    FROM fsdb.recordings 
    WHERE album_pair is not null and performer is not null and format is not null 
          and album_title is not null and release_date is not null and publisher is not null and man_mobile is not null);
-- 21561 rows created

-- INSERT INTO SONGS(title,writer,cowriter) 
--    (SELECT DISTINCT song,writer,cowriter FROM fsdb.recordings
--        WHERE song is not null and writer is not null
--     UNION
--     SELECT DISTINCT song,writer,cowriter FROM fsdb.livesingings 
--        WHERE song is not null and writer is not null);
-- Error detected: first author=second author
-- IMPLICIT SEMANTIC ASSUMPTION: if both authors are the same, second should be null

INSERT INTO SONGS(title,writer,cowriter) 
   (SELECT DISTINCT song,writer,cowriter FROM fsdb.recordings
       WHERE song is not null and writer is not null and (cowriter is null or writer!=cowriter)
    UNION 
	SELECT DISTINCT song,writer,null FROM fsdb.recordings
       WHERE song is not null and writer is not null and writer=cowriter
    UNION
    SELECT DISTINCT song,writer,cowriter FROM fsdb.livesingings 
       WHERE song is not null and writer is not null and (cowriter is null or writer!=cowriter)
    UNION
    SELECT DISTINCT song,writer,null FROM fsdb.livesingings 
       WHERE song is not null and writer is not null and writer=cowriter
);

-- 123699 rows created

-- Check any song is inserted twice, with authors reversed
-- SELECT title, writer from songs where (title,writer,cowriter) in (SELECT title,cowriter,writer from songs);
-- Error detected: one song has reversed authors
-- TITLE                                              WRITER         COWRITER
-- -------------------------------------------------- -------------- --------------
-- Something jazzes                                   GB>>0600283845 GB>>0785936179
-- Something jazzes                                   GB>>0785936179 GB>>0600283845
-- 
-- select count('s') from fsdb.recordings where song='Something jazzes' and writer='GB>>0600283845';
-- select count('s') from fsdb.livesingings where song='Something jazzes' and writer='GB>>0600283845';
-- select count('s') from fsdb.recordings where song='Something jazzes' and writer='GB>>0785936179';
-- select count('s') from fsdb.livesingings where song='Something jazzes' and writer='GB>>0785936179';
-- The authors order is different in 1 track recording and 15 live performances
-- IMPLICIT SEMANTIC ASSUMPTION: the writer='GB>>0600283845', and cowriter='GB>>0785936179';
-- We delete the other one, and it will be taken into account when inserting tracks
DELETE songs where title='Something jazzes' and writer='GB>>0785936179';
-- 1 row deleted

-- insert that track with cowriter as writer, and then skip it during general insert
INSERT INTO TRACKS(PAIR,sequ,title,writer,duration,rec_date,studio,engineer) 
(SELECT DISTINCT album_pair,tracknum,song,cowriter,duration,rec_date,studio,engineer 
    FROM fsdb.recordings 
    WHERE song='Something jazzes' and writer='GB>>0785936179');
-- 1 row created

-- INSERT INTO TRACKS(PAIR,sequ,title,writer,duration,rec_date,studio,engineer) 
-- (SELECT DISTINCT album_pair,tracknum,song,writer,duration,rec_date,studio,engineer 
--     FROM fsdb.recordings 
--     WHERE album_pair is not null and tracknum is not null and song is not null and writer is not null 
--           and duration is not null and rec_date is not null and engineer is not null
--		     and not (song='Something jazzes' and writer='GB>>0785936179')
-- );
-- Error detected: PK violation due to 2 trackss of same album with the same tracknum 
-- IMPLICIT SEMANTIC ASSUMPTION: skip (those tracks won't be inserted)

INSERT INTO TRACKS(PAIR,sequ,title,writer,duration,rec_date,studio,engineer) 
(SELECT DISTINCT album_pair,tracknum,min(song),min(writer),min(duration),
                 min(rec_date),min(studio),min(engineer) 
    FROM fsdb.recordings 
    WHERE album_pair is not null and tracknum is not null and song is not null and writer is not null 
          and duration is not null and rec_date is not null and engineer is not null
		  and not (song='Something jazzes' and writer='GB>>0785936179')
	GROUP BY album_pair,tracknum having count('s')=1
);
-- 146275 rows created

-- Though it is not required to insert the skipped tracks, you can do it with this sentence
-- (those tracks will be inserted with any order by the end of their album)
INSERT INTO TRACKS(PAIR,sequ,title,writer,duration,rec_date,studio,engineer) 
(SELECT DISTINCT album_pair,maxtrack+rownum,song,writer,duration,rec_date,studio,engineer 
	         FROM (SELECT album_pair, tracknum  
			          FROM fsdb.recordings 
                      WHERE album_pair is not null and tracknum is not null and song is not null 
					        and writer is not null and duration is not null and 
							rec_date is not null and engineer is not null
	                  GROUP BY album_pair,tracknum having count('s')>1 ) T1 
			      JOIN (SELECT pair album_pair, max(sequ) maxtrack FROM tracks GROUP BY pair) T2 
 				       USING(album_pair) 
		          JOIN fsdb.recordings USING(album_pair, tracknum)
);
-- 2 rows created

-- -----------------------------------------
-- loading tables regarding concerts part
-- -----------------------------------------

INSERT INTO TOURS(performer,name,manager) 
(SELECT DISTINCT performer,tour,man_mobile FROM fsdb.livesingings 
   WHERE performer is not null and tour is not null and man_mobile is not null);
-- 5332 rows created

INSERT INTO CONCERTS(performer,when,tour,municipality,address,country,attendance,duration,manager) 
(SELECT DISTINCT performer,to_date(when,'dd-mm-yyyy'),tour,municipality,address,country,
                 nvl(attendance,0),duration_min,man_mobile
    FROM fsdb.livesingings 
    WHERE performer is not null and when is not null and municipality is not null and address is not null 
          and country is not null and man_mobile is not null);
-- 76348 rows created

INSERT INTO PERFORMANCES(performer,when,sequ,songtitle,songwriter,duration) 
(SELECT DISTINCT performer,when,seqnumber,song,writer,duration_sec
    FROM fsdb.livesingings 
    WHERE performer is not null and when is not null and seqnumber is not null and 
          song is not null and writer is not null);
-- 856432 rows created

INSERT INTO CLIENTS(e_mail,name,surn1,surn2,birthdate,phone,address,DNI) 
(SELECT DISTINCT e_mail,name,surn1,surn2,birthdate,phone,address,dni 
   FROM fsdb.melomaniacs WHERE e_mail is not null);
-- 1500 rows created




-- INSERT INTO ATTENDANCES(client,performer,when,RFID,purchase) 
-- (SELECT DISTINCT e_mail,performer,when,rfid,purchase 
--   FROM fsdb.melomaniacs 
--   WHERE e_mail is not null and performer is not null and when is not null 
--        and rfid is not null and birthdate is not null and purchase is not null);
-- birthday is checked non null; may also check that (when-birthdate)/365.2422 >= 18;
-- Error detected: FK violation due to 3 non existent concerts 
-- IMPLICIT SEMANTIC ASSUMPTION: skip (those attendances won't be inserted)

INSERT INTO ATTENDANCES(client,performer,when,RFID,purchase) 
(SELECT DISTINCT e_mail,performer,when,rfid,purchase 
   FROM fsdb.melomaniacs 
   WHERE e_mail is not null and performer is not null and when is not null 
        and rfid is not null and birthdate is not null and purchase is not null
		and (performer,when) in (SELECT DISTINCT performer,when FROM fsdb.livesingings));
-- 35618 rows created

-- Check ill results:
-- SELECT DISTINCT e_mail,performer,when,rfid,purchase 
--   FROM fsdb.melomaniacs 
--   WHERE e_mail is not null and performer is not null and when is not null 
--        and rfid is not null and birthdate is not null and purchase is not null
--		and (performer,when) not in (SELECT DISTINCT performer,when FROM fsdb.livesingings);
--
-- The ill results are (client,performer,when)
-- ('screener@clients.vinylinc.com', 'Cunegunda ', '15-06-2019' )
-- ('felico@clients.vinylinc.com', 'Cunegunda Ibarra', '31-08-2019' )
-- ('brenda@clients.vinylinc.com', 'CUNEGUNDA', '06-07-2019' )
--
-- By inspecting the CONCERTS table
-- SELECT DISTINCT performer,when from concerts where upper(performer) like '%CUNEGUNDA%';
-- We can see the three concerts exist for performer 'Cunegunda'
-- They have not been linked because strings were not exatly the same, respectively: 
-- an extra blank space after 'Cunegunda '; surname after name; and uppercase (within string) 
--
-- Though it is not required, we can insert them setting a constant value for performer:
INSERT INTO ATTENDANCES(client,performer,when,RFID,purchase) 
(SELECT DISTINCT e_mail,'Cunegunda',when,rfid,purchase 
   FROM fsdb.melomaniacs 
   WHERE e_mail is not null and performer is not null and when is not null 
        and rfid is not null and birthdate is not null and purchase is not null
		and (performer,when) not in (SELECT DISTINCT performer,when FROM fsdb.livesingings));
-- 3 rows created

COMMIT;
