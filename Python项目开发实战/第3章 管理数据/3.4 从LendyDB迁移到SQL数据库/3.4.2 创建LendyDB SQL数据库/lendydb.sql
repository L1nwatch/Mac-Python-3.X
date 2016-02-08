PRAGMA Foreign_Keys=True;

drop table loan;
drop table item;
drop table member;

create table member (
ID INTEGER PRIMARY KEY,
Name TEXT NOT NULL,
Email TEXT);

create table item (
ID INTEGER PRIMARY KEY,
Name TEXT NOT NULL,
Description TEXT NOT NULL,
OwnerID INTEGER NOT NULL REFERENCES member(ID),
Price NUMERIC, 
Condition TEXT,
DateRegistered TEXT);

create table loan (
ID INTEGER PRIMARY KEY,
ItemID INTEGER NOT NULL REFERENCES item(ID),
BorrowerID INTEGER NOT NULL REFERENCES member(ID),
DateBorrowed TEXT NOT NULL,
DateReturned TEXT);

