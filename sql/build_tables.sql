CREATE OR REPLACE TABLE MEASURESMENTS (
 ID INT NOT NULL AUTO_INCREMENT,
 PROFILE VARCHAR(255) NOT NULL,
 DATE DATETIME NOT NULL,
 TEMPERATURE DOUBLE NOT NULL, 
 PRIMARY KEY(ID)
);
