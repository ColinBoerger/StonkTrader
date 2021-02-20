CREATE TABLE stocks(
	ticker varchar(5) PRIMARY KEY,
	companyName varchar2(256)
);

CREATE TABLE scans (
	scanId INTEGER PRIMARY KEY AUTOINCREMENT, 
	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	type varchar(64)
); 

CREATE TABLE mentions(
	ticker varchar(5),
	numMentions INTEGER,
	subReddit varchar(64),
	scan INTEGER,
	FOREIGN KEY(ticker) REFERENCES stocks(ticker),
	FOREIGN KEY(scan) REFERENCES scan(scanId)
);

