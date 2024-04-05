CREATE DEFINER=`MCUser`@`localhost` PROCEDURE `get_earned_awards_bydate`(IN startdate datetime, IN enddate datetime)
BEGIN

select p.id AS person_id,p.branch_id,p.lastname,p.firstname,c.name as chapter,c.id as chapter_id, f.name as fleet,f.id as fleet_id, w.name AS weapon,
Case When tc.marksman between startdate and enddate Then tc.marksman Else null End as marksman,
Case When tc.sharpshooter between startdate and enddate Then tc.sharpshooter Else null End as sharpshooter, 
Case When tc.expert between startdate and enddate Then tc.expert Else null End as expert,
Case When tc.high_expert between startdate and enddate Then tc.high_expert Else null End as high_expert
from models_person p 
join models_totalcredits tc on tc.person_id = p.id
join models_weapon w on tc.weapon_id = w.id
join models_chapter c on p.chapter_id=c.id
join models_fleet f on c.fleet_id = f.id
where p.active =1 and tc.active = 1 and  ((tc.marksman between startdate and enddate) or
(tc.sharpshooter between startdate and enddate) or
(tc.expert between startdate and enddate) or
(tc.high_expert between startdate and enddate))
order by f.name, c.name, p.lastname, p.firstname, w.name;

END