CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `MCUser`@`localhost` 
    SQL SECURITY DEFINER
VIEW `modelview_categorycredits` AS
    SELECT 
        `m`.`id` AS `id`,
        `m`.`id` AS `person_id`,
        `m`.`lastname` AS `lastname`,
        `m`.`firstname` AS `firstname`,
        `w`.`name` AS `weapon`,
        `w`.`id` AS `weapon_id`,
        `b`.`name` AS `branch`,
        SUM(`p`.`credits`) AS `weaponcredits`
    FROM
        (((((`models_sessionparticipants` `p`
        JOIN `models_person` `m` ON (((`p`.`person_id` = `m`.`id`)
            AND (`m`.`active` = 1))))
        JOIN `models_branch` `b` ON (((`m`.`branch_id` = `b`.`id`)
            AND (`b`.`active` = 1))))
        JOIN `models_session` `s` ON (((`p`.`session_id` = `s`.`id`)
            AND (`s`.`active` = 1)
            AND (`s`.`dupsessid` IS NULL))))
        JOIN `models_game` `g` ON (((`s`.`game_id` = `g`.`id`)
            AND (`g`.`active` = 1)
            AND (`g`.`verified` = 1))))
        JOIN `models_weapon` `w` ON ((`g`.`weapon_id` = `w`.`id`)))
    WHERE
        (`p`.`active` = 1)
    GROUP BY `p`.`person_id` , `g`.`weapon_id`;
