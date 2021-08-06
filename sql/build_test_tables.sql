USE brewbot_test;

CREATE OR REPLACE TABLE measurements (
 id INT NOT NULL AUTO_INCREMENT,
 profile_id INT NOT NULL,
 measurement_date DATETIME NOT NULL,
 fermenter_temp DOUBLE NOT NULL,
 within_temp_range BOOLEAN NOT NULL,
 ambient_temp DOUBLE DEFAULT 0.0,
 heating_on BOOLEAN,
 cooling_on BOOLEAN,
 PRIMARY KEY(id)
);

CREATE OR REPLACE TABLE specific_gravity (
 id INT NOT NULL AUTO_INCREMENT,
 profile_id INT NOT NULL,
 measurement_date DATETIME NOT NULL,
 measurement DOUBLE NOT NULL,
 PRIMARY KEY(id)
);

CREATE OR REPLACE TABLE brew_profile (
 profile_id INT NOT NULL AUTO_INCREMENT,
 profile_name VARCHAR(255) NOT NULL,
 stage_id INT NOT NULL,
 stage_name VARCHAR(255) NOT NULL,
 start_time DATETIME NOT NULL,
 finish_time DATETIME NOT NULL,
 min_temp DOUBLE NOT NULL,
 max_temp DOUBLE NOT NULL,
 volume_litres DOUBLE NOT NULL,
 original_gravity DOUBLE NOT NULL,
 final_gravity DOUBLE NOT NULL,
 alert_on_finish BOOLEAN NOT NULL,
 PRIMARY KEY(profile_id, stage_id)
);

INSERT INTO brew_profile (profile_name, stage_id, stage_name, start_time, finish_time, min_temp, max_temp, volume_litres, original_gravity, final_gravity, alert_on_finish)
VALUES
(
  'Mangrove Jack\'s - Crossman\'s Gold Lager', 
  1, 
  'FERMENTATION', 
  '2012-07-02 12:30:00', 
  '2012-07-06 12:30:00', 
  20.0, 
  25.0, 
  24.5, 
  1030.0, 
  1005.0, 
  TRUE
);

INSERT INTO specific_gravity (profile_id, measurement_date, measurement) VALUES 
(1, NOW() - INTERVAL 7 DAY, 1030.0),
(1, NOW(), 1005.0);

INSERT INTO measurements (profile_id, measurement_date, fermenter_temp, within_temp_range, ambient_temp, heating_on, cooling_on) VALUES
 (1, NOW() - INTERVAL 10 DAY, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 9 DAY, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 8 DAY, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 7 DAY, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 6 DAY, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 5 DAY, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 4 DAY, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 3 DAY, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 2 DAY, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 1 DAY, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 1 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 2 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 3 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 4 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 5 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 6 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 7 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 8 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 9 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 10 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 11 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 12 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 13 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 14 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 15 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 16 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 17 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 18 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 19 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 20 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 21 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 22 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 23 HOUR, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 10 MINUTE, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 20 MINUTE, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 30 MINUTE, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 40 MINUTE, 22.0, TRUE, 24.0, FALSE, FALSE), 
 (1, NOW() - INTERVAL 50 MINUTE, 22.0, TRUE, 24.0, FALSE, FALSE)
;
