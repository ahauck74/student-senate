drop database if exists senate;

create database senate;

use senate;


create table organizations(
    ORG_ID int NOT NULL AUTO_INCREMENT,
    ORG_NAME varchar(225) NOT NULL,
    ORG_ACR varchar(225) DEFAULT NULL,
    ORG_EMAIL varchar(225),
    CURRENT_TIER varchar(225),
    TIER_REQUEST varchar(225) DEFAULT NULL,
    ORG_DESCRIPTION text(2000),
    CONSTITUTION blob,
    ORG_MEMBERS varchar(225),
    ORG_ATTENDING_MEMBERS varchar(225),
    BUDGET int,
    APPROVAL_STATUS varchar(10) DEFAULT NULL,
    CHANGE_DATE datetime,
    PRIMARY KEY (ORG_ID)
    );

INSERT INTO organizations(ORG_NAME, ORG_ACR, ORG_EMAIL, CURRENT_TIER, TIER_REQUEST, ORG_DESCRIPTION, ORG_MEMBERS, ORG_ATTENDING_MEMBERS, BUDGET, APPROVAL_STATUS, CHANGE_DATE)
VALUES ("Alliance", NULL, "weregoingupton@gmail.com", "Tier 1", NULL, "Valpos lgbt+ community", 45, 20, 2000, TRUE, NOW()), 
		("Social Action Leaders hip Team", "SALT", "weregoingupton@gmail.com", "Tier 2", NULL, "Social justice ministry.", 80, 46, 500, TRUE, NOW()), 			("Test Org", "Test", "weregoingupton@gmail.com", "Tier 2", "Tier 1", "Testing.", 80, 46, 500, NULL, NOW());

create table deadlines(
  deadline datetime NOT NULL
);

INSERT INTO deadlines SET deadline=NOW();


create table officers(
    OFFICER_ID int NOT NULL AUTO_INCREMENT,
    OFFICER_NAME varchar(225),
    OFFICER_PHONE varchar(225),
    OFFICER_EMAIL varchar(225),
    TITLE varchar(225),
    YEAR year,
    ORG_ID int NOT NULL,
    PRIMARY KEY (OFFICER_ID),
    FOREIGN KEY (ORG_ID) REFERENCES organizations(ORG_ID)
);

insert into officers(OFFICER_NAME, OFFICER_PHONE, OFFICER_EMAIL, TITLE, YEAR, ORG_ID) VALUES
("Keith Shmeith", "773-708-4561", "weregoingupton@gmail.com", "President", YEAR(CURDATE()), 1), ("Saddie Sadburg", "666-666-6666", "weregoingupton@gmail.com", "Treasurer", YEAR(CURDATE()), 2), ("Um from Umbridge", "708-224-9999", "weregoingupton@gmail.com", "Historian", YEAR(CURDATE()), 1);


create table advisors(
    ADVISOR_ID int NOT NULL AUTO_INCREMENT,
    ADVISOR_NAME varchar(225),
    ADVISOR_PHONE varchar(225),
    ADVISOR_EMAIL varchar(225),
    TITLE varchar(225),
    ORG_ID int NOT NULL,
    PRIMARY KEY (ADVISOR_ID),
    FOREIGN KEY (ORG_ID) REFERENCES organizations(ORG_ID)
);

insert into advisors(ADVISOR_NAME, ADVISOR_PHONE, ADVISOR_EMAIL, TITLE, ORG_ID)
VALUES ("Lana Mier", "798-675-9856", "weregoingupton@gmail.com", "Assistant Professor", 1), ("Mike Cath", "567-273-4561", "weregoingupton@gmail.com", "Doing his best", 2);


create table archives(
    ORG_ID int,
    ORG_NAME varchar(225),
    ORG_ACR varchar(225),
    ORG_EMAIL varchar(225),
    TIER varchar(225),
    ORG_DESCRIPTION text(2000),
    BUDGET int,
    CHANGE_DATE datetime
);

create table officer_archives(
  OFFICER_ID int,
  OFFICER_NAME varchar(225),
  OFFICER_PHONE varchar(225),
  OFFICER_EMAIL varchar(225),
  TITLE varchar(225),
  YEAR year,
  ORG_ID int,
  DELETED_ON datetime
);

create table advisor_archives(
  ADVISOR_ID int,
  ADVISOR_NAME varchar(225),
  ADVISOR_PHONE varchar(225),
  ADVISOR_EMAIL varchar(225),
  TITLE varchar(225),
  ORG_ID int,
  DELETED_ON datetime
);

DELIMITER ;;
CREATE TRIGGER after_org_update
AFTER UPDATE ON organizations
FOR EACH ROW
BEGIN
INSERT INTO archives SET ORG_ID=OLD.ORG_ID, ORG_NAME=OLD.ORG_NAME, ORG_ACR=OLD.ORG_ACR, ORG_EMAIL=OLD.ORG_EMAIL, TIER=OLD.CURRENT_TIER, ORG_DESCRIPTION=OLD.ORG_DESCRIPTION, BUDGET=OLD.BUDGET, CHANGE_DATE=NOW();
END;;

CREATE TRIGGER after_officer_delete
AFTER DELETE ON officers
FOR EACH ROW
BEGIN
INSERT INTO officer_archives SET OFFICER_ID=OLD.OFFICER_ID, OFFICER_NAME=OLD.OFFICER_NAME, OFFICER_PHONE=OLD.OFFICER_PHONE, OFFICER_EMAIL=OLD.OFFICER_EMAIL, TITLE=OLD.TITLE, YEAR=OLD.YEAR, ORG_ID=OLD.ORG_ID, DELETED_ON=NOW();
END;;

CREATE TRIGGER after_advisor_delete
AFTER DELETE ON advisors
FOR EACH ROW
BEGIN
INSERT INTO advisor_archives SET ADVISOR_ID=OLD.ADVISOR_ID, ADVISOR_NAME=OLD.ADVISOR_NAME, ADVISOR_PHONE=OLD.ADVISOR_PHONE, ADVISOR_EMAIL=OLD.ADVISOR_EMAIL, TITLE=OLD.TITLE, ORG_ID=OLD.ORG_ID, DELETED_ON=NOW();
END;;

DELIMITER ;
