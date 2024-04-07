CREATE DEFINER=`MCUser`@`localhost` PROCEDURE `get_session_history`(startdate datetime, enddate datetime, person_id int)
BEGIN
select s.id as session_id,s.startdate,s.enddate,s.playmode,g.name as game,w.name as weapon,s.turnsplayed,p.credits,
(SELECT GROUP_CONCAT(
          concat(firstname,' ',lastname) SEPARATOR ', '
        ) 
	FROM models_sessionparticipants
	JOIN models_person on models_sessionparticipants.person_id=models_person.id
	WHERE session_id = s.id
GROUP BY s.id) as players,
(SELECT GROUP_CONCAT(
          fullname SEPARATOR ', '
        ) 
	FROM models_nontrmnparticipants
	WHERE session_id = s.id
GROUP BY s.id) as nontrmnplayers
from models_session s
join models_game g on (s.game_id = g.id) and g.active = 1 
join models_weapon w on g.weapon_id = w.id
join models_sessionparticipants p on (p.session_id = s.id) and p.active=1
where s.dupsessid is null and g.verified=1
and s.startdate between startdate and enddate
and p.person_id=person_Id and p.active=1;
END