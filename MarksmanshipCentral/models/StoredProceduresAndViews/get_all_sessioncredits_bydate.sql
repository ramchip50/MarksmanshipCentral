CREATE DEFINER=`root`@`localhost` PROCEDURE `get_all_sessioncredits_bydate`(IN startdate datetime, IN enddate datetime)
BEGIN

select p.person_id as person_id, g.weapon_id as weapon_id, sum(p.credits) as weaponcredits, m.firstname, m.lastname,c.name as chapter, f.name as fleet, w.name as weapon from models_sessionparticipants p
join models_person m on ((p.person_id = m.id) and m.active=1)
join models_branch b on ((m.branch_id = b.id) and b.active=1)
join models_chapter c on ((m.chapter_id = c.id) and c.active=1)
join models_fleet f on ((c.fleet_id = f.id) and f.active=1)
join models_session s on ((p.session_id = s.Id) and (s.active=1 and s.flagged=0))
join models_game g on ((s.game_id = g.id) and (g.active=1 and g.verified=1))
join models_weapon w on g.weapon_id = w.Id
where p.active=1
and s.enddate >= startdate and s.enddate <= enddate
group by p.person_id, g.weapon_id
order by f.name, c.name, m.lastname, m.firstname, w.name;

END