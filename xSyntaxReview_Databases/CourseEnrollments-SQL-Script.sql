CREATE TABLE User (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT UNIQUE,
	email TEXT
);

CREATE TABLE Course (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	title TEXT UNIQUE
);


--- CONNECTOR TABLE BETWEEN User & Course ---
CREATE TABLE Member (
	user_id INTEGER,
	course_id INTEGER,
	role INTEGER, -- 0 for student, 1 for professor
	PRIMARY KEY (user_id, course_id)
);


INSERT INTO User (name, email) VALUES 
	('Priscilla', 'priscilla@walmartuniversity.edu'),
	('Squidward', 'squidward@walmartuniversity.edu'),
	('Refrigerator', 'refrigerator@walmartuniversity.edu'),
	('Queen Elizabeth', 'iambritish@walmartuniversity.edu'),
	('Bob', 'bob@walmartuniversity.edu'),
	('Queen Elizabeth', 'iambritish@walmartuniversity.edu');

	


INSERT INTO Course (title) VALUES
	('Tax Evasion 101'),
	('Advanced Philosophy, The Debated Existence of Florida'),
	('Intermediate Seminar on Watching Paint Dry'),
	('Pre-K Mathematics, Integral Calculus Edition'),
	('Introduction to the Morality of Toyotathon'),
	('Introduction to Building a Rogue, Sentient Robot (Fun)')
	
SELECT * FROM User;
SELECT * FROM Course;


INSERT INTO Member (user_id, course_id, role) VALUES
	--Tax Evasion 101
	(1, 1, 1),
	(2, 1, 0),
	(3, 1, 0),
	(4, 1, 0),
	(5, 1, 0),
	--Advanced Philosophy, The Debated Existence of Florida
	(2, 2, 0),
	(3, 2, 1),
	(5, 2, 0),
	--Intermediate Seminar on Watching Paint Dry
	(1, 3, 0),
	(2, 3, 1),
	--Pre-K Mathematics, Integral Calculus Edition
	(1, 4, 0),
	(5, 4, 1),
	--Introduction to the Morality of Toyotathon
	(2, 5, 1),
	(4, 5, 0),
	(5, 5, 0),
	--Introduction to Building a Rogue, Sentient Robot (Fun)
	(1, 6, 0),
	(2, 6, 0),
	(3, 6, 1),
	(4, 6, 0),
	(5, 6, 0);
	
SELECT * FROM Member;


SELECT User.id AS 'User ID', User.name, Member.role, 
			CASE WHEN Member.role = 0 THEN 'Student'
				 ELSE 'Professor'
			END AS RoleDescription,
		Course.id AS 'Course ID', Course.title 
FROM User
JOIN MEMBER JOIN Course
ON Member.user_id = User.id AND Member.course_id = Course.id
ORDER BY Course.title, Member.role DESC, User.name;
	