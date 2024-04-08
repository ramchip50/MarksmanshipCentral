CREATE DEFINER=`root`@`localhost` PROCEDURE `get_all_sessioncredits_bydate`(IN startdate datetime, IN enddate datetime)
BEGIN

SET @nextenddate = DATE_ADD(enddate,INTERVAL 1 Day);

select p.person_id as person_id, b.id as branch_id, g.weapon_id as weapon_id, sum(p.credits) as weaponcredits, m.firstname, m.lastname,c.name as chapter, c.id as chapter_id,
 f.name as fleet, f.id as fleet_id, w.name as weapon from models_sessionparticipants p
join models_person m on ((p.person_id = m.id) and m.active=1)
join models_branch b on ((m.branch_id = b.id) and b.active=1)
join models_chapter c on ((m.chapter_id = c.id) and c.active=1)
join models_fleet f on ((c.fleet_id = f.id) and f.active=1)
join models_session s on ((p.session_id = s.Id) and (s.active=1 and s.dupsessid is null))
join models_game g on ((s.game_id = g.id) and (g.active=1 and g.verified=1))
join models_weapon w on g.weapon_id = w.Id
where p.active=1
and s.enddate between startdate and @nextenddate
group by p.person_id, g.weapon_id
order by f.name, c.name, m.lastname, m.firstname, w.name;

END