CREATE TABLE ACCOUNT_INFO(
	A_USERNAME VARCHAR(80), #stores username
    A_EMAIL VARCHAR(80) NOT NULL UNIQUE, #stores email address
    A_PASSWORD VARCHAR(255) NOT NULL, #stores password
    A_CREATION_DATE TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, #stores timestamp of account creation automatically when new account added to this table
    PRIMARY KEY(A_USERNAME)
);

CREATE TABLE CUSTOM_MEMES(
	M_ID INT NOT NULL AUTO_INCREMENT, #assigns a unique ID (surrogate key) to each custom meme. starting value can be modified below
	M_NAME VARCHAR(80) NOT NULL, #stores name of the meme
	M_UPLOAD_DATE TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, #stores timestamp of upload date automatically when the meme was added to the table (aka upload date/time)
	PRIMARY KEY(M_ID)
);

ALTER TABLE CUSTOM_MEMES AUTO_INCREMENT=10000000; #starting ID value for custom memes

CREATE TABLE ACCOUNT_STREAMS(
	A_USERNAME VARCHAR(80), #username of user
	S_STREAMNAME VARCHAR(80), #stream that they are subscribed to or own (not sure how it will work implementation wise but could add another value for stream owner)
	PRIMARY KEY(A_USERNAME, S_STREAMNAME), #each row must be unique (user can't be subscribed to same stream twice) 
	FOREIGN KEY(A_USERNAME) REFERENCES ACCOUNT_INFO(A_USERNAME) #username is a foreign key (must be in ACCOUNT_INFO table)
);

CREATE TABLE SCRAPED_MEMES(
    ID int NOT NULL AUTO_INCREMENT,
    UPLOAD_DATE TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    LINK VARCHAR(200) NOT NULL,
    PRIMARY KEY(ID)
); 
    
