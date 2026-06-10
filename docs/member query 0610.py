create table Member(
	member_id INT,
	phone_number VARCHAR(11) Not Null,
	stamp INT DEFAULT 0,
	grade VARCHAR(20)
	);

ALTER TABLE member
ADD CONSTRAINT member_pk
PRIMARY KEY(member_id);
