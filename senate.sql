drop database if exists senate;

create database senate;

use senate;

create table organizations(
    ORG_NAME varchar(255) NOT NULL,
    ORG_ACR varchar(225) DEFAULT NULL,
    ORG_DESCRIPTION text(2000),
    ORG_EMAIL varchar(255),
    PRIMARY KEY (ORG_NAME));

INSERT INTO organizations VALUES ("Alliance", NULL, "Valpo's lgbt+ community", "alliance@valpo.edu"), ("Social Action Leadership Team", "SALT", "Social justice ministry", "salt@valpo.edu");

create table org_record(
    ORG_NAME varchar(255) NOT NULL,
    CURRENT_TIER varchar(255),
    TIER_REQUEST varchar(255) DEFAULT NULL,
    CONSTITUTION varchar(255),
    BUDGET int,
    APPROVAL_STATUS varchar(10) DEFAULT NULL,
    PRIMARY KEY (ORG_NAME),
    FOREIGN KEY (ORG_NAME) REFERENCES organizations(ORG_NAME));

INSERT INTO org_record VALUES ("Alliance", "Tier 1", NULL, "link.imdyinginside.com", 2000, "yes"), ("Social Action Leadership Team", "Tier 2", "Tier 1", "everythingismeaningless.com/uuuuugh", 500, "Y");


create table students(
    STUDENT_ID int NOT NULL AUTO_INCREMENT,
    STUDENT_NAME varchar(255),
    STUDENT_PHONE varchar(255),
    STUDENT_EMAIL varchar(255),
    PRIMARY KEY (STUDENT_ID));

INSERT INTO students(STUDENT_NAME, STUDENT_PHONE, STUDENT_EMAIL) VALUES ("Keith Shmeith", "773-708-4561", "keith.shmeith@valpo.edu"), ("Saddie Sadburg", "666-666-6666", "saddie.sadburg@valpo.edu"),
    ("Um from umbridge", "708-224-9999", "um.umbridge@valpo.edu");

create table officers(
    STUDENT_ID int NOT NULL,
    ORG_NAME varchar(255) NOT NULL,
    TITLE varchar(255),
    PRIMARY KEY (STUDENT_ID, ORG_NAME),
    FOREIGN KEY (STUDENT_ID) REFERENCES students(STUDENT_ID),
    FOREIGN KEY (ORG_NAME) REFERENCES organizations(ORG_NAME)
);

insert into officers VALUES(3, "Alliance", "President"), (2, "Social Action Leadership Team", "Treasurer"), (1, "Alliance", "Historian");


create table staff(
    STAFF_ID int NOT NULL AUTO_INCREMENT,
    STAFF_NAME varchar(255),
    STAFF_PHONE varchar(255),
    STAFF_EMAIL varchar(255),
    PRIMARY KEY (STAFF_ID)
);

insert into staff (STAFF_NAME, STAFF_PHONE, STAFF_EMAIL) VALUES ("Lana Mier", "798-675-9856", "lana.mier@valpo.edu"),("Mike Cath", "567-273-4829", "mike.cath@valpo.edu");

create table advisors(
    ORG_NAME varchar(255) NOT NULL,
    STAFF_ID int NOT NULL,
    TITLE varchar(255),
    PRIMARY KEY (ORG_NAME, STAFF_ID),
    FOREIGN KEY (ORG_NAME) REFERENCES organizations(ORG_NAME),
    FOREIGN KEY (STAFF_ID) REFERENCES staff(STAFF_ID)
);

insert into advisors VALUES ("Alliance", 1, "Assistant Professor"),("Social Action Leadership Team",2, "Doing his best");

DELIMITER ;;
CREATE TRIGGER before_org_record_update
BEFORE UPDATE ON org_record
FOR EACH ROW
BEGIN
INSERT INTO archives SET ORG_NAME=OLD.ORG_NAME, TIER=OLD.CURRENT_TIER, BUDGET=OLD.BUDGET, CHANGE_DATE=NOW();
END;;
DELIMITER ;
