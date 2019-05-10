
--/***************************************************************************************/
-- TABLE USER
--/***************************************************************************************/
CREATE TABLE IF NOT EXISTS `USERS`(
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(75) NOT NULL,
    `username` VARCHAR(75) NOT NULL,
    `email` VARCHAR(75) NOT NULL,
    `password` VARCHAR(100) NOT NULL,
    `register_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT UC_email UNIQUE(`email`)
)ENGINE=InnoDB CHARSET=utf8mb4;
