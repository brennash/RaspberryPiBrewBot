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
