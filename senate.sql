drop database if exists senate;

create database senate;

use senate;


create table organizations(
    ORG_ID int NOT NULL AUTO_INCREMENT,
    ORG_LINK_NAME varchar(225) NOT NULL,
    ORG_NAME varchar(225) NOT NULL,
    ORG_ACR varchar(225) DEFAULT NULL,
    ORG_EMAIL varchar(225),
    CURRENT_TIER varchar(225),
    TIER_REQUEST varchar(225) DEFAULT NULL,
    ORG_DESCRIPTION text(2000),
    CONSTITUTION varchar(225),
    ORG_MEMBERS varchar(225),
    ORG_ATTENDING_MEMBERS varchar(225),
    BUDGET int,
    APPROVAL_STATUS varchar(10) DEFAULT NULL,
    PRIMARY KEY (ORG_ID, ORG_LINK_NAME)
    );

INSERT INTO organizations(ORG_LINK_NAME, ORG_NAME, ORG_ACR, ORG_EMAIL, CURRENT_TIER, TIER_REQUEST, ORG_DESCRIPTION, CONSTITUTION, ORG_MEMBERS, ORG_ATTENDING_MEMBERS, BUDGET, APPROVAL_STATUS)
VALUES ("Alliance", "Alliance", NULL, "alliance@valpo.edu", "Tier 1", NULL, "Valpo's lgbt+ community", "link.imdyinginside.com", 45, 20, 2000, "yes"), ("Social-Action-Leadership-Team", "Social Action Leadership Team", "SALT", "salt@valpo.edu", "Tier 2", "Tier 1", "Social justice ministry.", "everythingismeaningless.com/uuuuugh", 80, 46, 500, "Y");


create table officers(
    OFFICER_ID int NOT NULL AUTO_INCREMENT,
    OFFICER_NAME varchar(225),
    OFFICER_PHONE varchar(225),
    OFFICER_EMAIL varchar(225),
    TITLE varchar(225),
    YEAR year,
    ORG_ID int NOT NULL,
    ORG_LINK_NAME varchar(225) NOT NULL,
    PRIMARY KEY (OFFICER_ID),
    FOREIGN KEY (ORG_ID, ORG_LINK_NAME) REFERENCES organizations(ORG_ID, ORG_LINK_NAME)
);

insert into officers(OFFICER_NAME, OFFICER_PHONE, OFFICER_EMAIL, TITLE, YEAR, ORG_ID, ORG_LINK_NAME) VALUES
("Keith Shmeith", "773-708-4561", "keith.shmeith@valpo.edu", "President", YEAR(CURDATE()), 1, "Alliance"), ("Saddie Sadburg", "666-666-6666", "saddie.sadburg@valpo.edu", "Treasurer", YEAR(CURDATE()), 2, "Social-Action-Leadership-Team"), ("Um from Umbridge", "708-224-9999", "um.umbridge@valpo.edu", "Historian", YEAR(CURDATE()), 1, "Alliance");


create table advisors(
    ADVISOR_ID int NOT NULL AUTO_INCREMENT,
    ADVISOR_NAME varchar(225),
    ADVISOR_PHONE varchar(225),
    ADVISOR_EMAIL varchar(225),
    TITLE varchar(225),
    ORG_ID int NOT NULL,
    ORG_LINK_NAME varchar(225) NOT NULL,
    PRIMARY KEY (ADVISOR_ID),
    FOREIGN KEY (ORG_ID, ORG_LINK_NAME) REFERENCES organizations(ORG_ID, ORG_LINK_NAME)
);

insert into advisors(ADVISOR_NAME, ADVISOR_PHONE, ADVISOR_EMAIL, TITLE, ORG_ID, ORG_LINK_NAME)
VALUES ("Lana Mier", "798-675-9856", "lana.mier@valpo.edu", "Assistant Professor", 1, "Alliance"), ("Mike Cath", "567-273-4561", "mike.cath@valpo.edu", "Doing his best", 2, "Social-Action-Leadership-Team");


create table archives(
    ORG_ID int,
    ORG_LINK_NAME varchar(225),
    ORG_NAME varchar(225),
    ORG_ACR varchar(225),
    ORG_EMAIL varchar(225),
    TIER varchar(225),
    ORG_DESCRIPTION text(2000),
    BUDGET int,
    CHANGE_DATE datetime
);

DELIMITER ;;
CREATE TRIGGER before_org_update
BEFORE UPDATE ON organizations
FOR EACH ROW
BEGIN
INSERT INTO archives SET ORG_ID=OLD.ORG_ID, ORG_LINK_NAME=OLD.ORG_LINK_NAME, ORG_NAME=OLD.ORG_NAME, ORG_ACR=OLD.ORG_ACR, ORG_EMAIL=OLD.ORG_EMAIL, TIER=OLD.CURRENT_TIER, ORG_DESCRIPTION=OLD.ORG_DESCRIPTION, BUDGET=OLD.BUDGET, CHANGE_DATE=NOW();
END;;
DELIMITER ;
