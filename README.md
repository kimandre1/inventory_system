# inventory_system
Inventory system for pre-made mysql database due for a school project.
Made by Kim André, Even and Simen.


## How to use
To use this software you need to create a config.yml file and put it in the project root directory.

config.yml should have the following syntax (update using your credentials): 
```yaml
# config.yaml


# Database information, input your credentials here before running in production!
database:
  user: your_db_user
  password: your_db_password
  host: your_db_host
  port: your_db_port
  name: your_db_name

  ```

# Stored Procedures

This script uses a lot of stored procedures. MySQL required. Add these before use

```mysql

//Henter info om alle Varer
DELIMITER //

CREATE PROCEDURE GetVareinfo()
BEGIN
	SELECT VNr AS Varenummer, Betegnelse, Pris, Antall FROM varehusdb.vare;
END //

DELIMITER ;

//Henter info om alle Ordre
DELIMITER //

CREATE PROCEDURE GetOrdreinfo()
BEGIN
	SELECT OrdreNr as 'Ordrenummer', OrdreDato AS 'Bestillingsdato', SendtDato AS 'Sendt', BetaltDato AS 'Betalt', KNr AS 'Kundenummer' FROM varehusdb.ordre;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE InspectOrder(IN order_id INT)
BEGIN
	SELECT 
    ordrelinje.OrdreNr AS Ordrenummer, 
    vare.Betegnelse, 
    vare.VNr AS Varenummer, 
    ordrelinje.Antall AS 'Antall Solgt', 
    vare.Pris, 
    SUM(ordrelinje.Antall * vare.Pris) AS 'Pris Total' 
	FROM 
		ordrelinje
	INNER JOIN 
		vare ON ordrelinje.VNr = vare.VNr 
	WHERE 
		OrdreNr = order_id
	GROUP BY 
		ordrelinje.OrdreNr, vare.Betegnelse, vare.VNr, ordrelinje.Antall, vare.Pris;
END //

DELIMITER ;


//Henter info om kunde for inspier ordre

DELIMITER //

CREATE PROCEDURE GetClientinfo(IN order_id INT)
BEGIN
	SELECT
		kunde.Fornavn,
		kunde.Etternavn,
		kunde.Adresse,
		kunde.PostNr AS Postnummer
	FROM
		kunde
	INNER JOIN
		ordre ON kunde.KNr = ordre.KNr
	WHERE 
		OrdreNr = order_id
	GROUP BY
		kunde.Fornavn, kunde.Etternavn, kunde.Adresse, kunde.PostNr;
END //

DELIMITER ;

//Henter generell kunde-informasjon

CREATE PROCEDURE GetKundeInfo()
BEGIN
	SELECT kunde.KNr AS 'Kundenummer', kunde.Fornavn, kunde.Etternavn, kunde.Adresse, kunde.PostNr AS 'Postnummer' FROM varehusdb.kunde;
END //
DELIMITER ;

CALL GetKundeInfo();