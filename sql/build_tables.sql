CREATE OR REPLACE TABLE measurements (
 id INT NOT NULL AUTO_INCREMENT,
 profile VARCHAR(255) NOT NULL,
 date DATETIME NOT NULL,
 fermenter_temp DOUBLE NOT NULL,
 within_temp_range BOOLEAN NOT NULL,
 ambient_temp DOUBLE DEFAULT 0.0,
 heating_on BOOLEAN NOT NULL,
 cooling_on BOOLEAN NOT NULL,
 PRIMARY KEY(id)
);

CREATE OR REPLACE TABLE brew_profile (
 profile_id INT NOT NULL AUTO_INCREMENT,
 profile_name VARCHAR(255) NOT NULL,
 stage_id INT NOT NULL,
 stage_name VARCHAR(255) NOT NULL,
 start_time TIME NOT NULL,
 finish_time TIME NOT NULL,
 min_temp DOUBLE NOT NULL,
 max_temp DOUBLE NOT NULL,
 alert_on_finish BOOLEAN NOT NULL,
 PRIMARY KEY(profile_id, stage_id)
);

INSERT INTO brew_profile (profile_name, stage_id, stage_name, start_time, finish_time, min_temp, max_temp, alert_on_finish)
VALUES
('Mangrove Jack\'s - Crossman\'s Gold Lager', 1, 'FERMENTATION', '0 00:00:00', '4 00:00:00', 20.0, 25.0, TRUE);
