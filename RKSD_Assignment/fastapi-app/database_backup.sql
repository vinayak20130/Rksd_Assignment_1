PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('initial_schema');
CREATE TABLE roles (
	role_id INTEGER NOT NULL, 
	role_name VARCHAR NOT NULL, 
	description VARCHAR, 
	is_active BOOLEAN DEFAULT 1 NOT NULL, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (role_id)
);
INSERT INTO roles VALUES(1,'Software Engineer','Full-stack software development position',1,'2025-03-09 03:47:48','2025-03-09 03:47:48');
INSERT INTO roles VALUES(2,'Data Scientist','Data analysis and machine learning position',1,'2025-03-09 03:47:48','2025-03-09 03:47:48');
INSERT INTO roles VALUES(3,'Product Manager','Product strategy and management position',1,'2025-03-09 03:47:48','2025-03-09 03:47:48');
CREATE TABLE candidates (
	candidate_id INTEGER NOT NULL, 
	photo VARCHAR, 
	candidate_name VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	phone_number VARCHAR NOT NULL, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (candidate_id), 
	UNIQUE (email), 
	UNIQUE (phone_number)
);
INSERT INTO candidates VALUES(1,NULL,'John Doe','john.doe@email.com','+1234567890','2025-03-09 03:48:08','2025-03-09 03:48:08');
INSERT INTO candidates VALUES(2,NULL,'Jane Smith','jane.smith@email.com','+1987654321','2025-03-09 03:48:08','2025-03-09 03:48:08');
INSERT INTO candidates VALUES(3,NULL,'Bob Wilson','bob.wilson@email.com','+1122334455','2025-03-09 03:48:08','2025-03-09 03:48:08');
INSERT INTO candidates VALUES(4,NULL,'Sarah Chen','sarah.chen@email.com','+1234567891','2025-03-09 03:56:52','2025-03-09 03:56:52');
INSERT INTO candidates VALUES(5,NULL,'Michael Brown','michael.brown@email.com','+1234567892','2025-03-09 03:56:52','2025-03-09 03:56:52');
CREATE TABLE stages (
	stage_id INTEGER NOT NULL, 
	stage_name VARCHAR NOT NULL, 
	role_id INTEGER NOT NULL, 
	stage_sequence INTEGER NOT NULL, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (stage_id), 
	FOREIGN KEY(role_id) REFERENCES roles (role_id)
);
INSERT INTO stages VALUES(1,'Resume Screening',1,1,'2025-03-09 03:47:55','2025-03-09 03:47:55');
INSERT INTO stages VALUES(2,'Technical Interview',1,2,'2025-03-09 03:47:55','2025-03-09 03:47:55');
INSERT INTO stages VALUES(3,'HR Interview',1,3,'2025-03-09 03:47:55','2025-03-09 03:47:55');
INSERT INTO stages VALUES(4,'Resume Screening',2,1,'2025-03-09 03:47:55','2025-03-09 03:47:55');
INSERT INTO stages VALUES(5,'Technical Assessment',2,2,'2025-03-09 03:47:55','2025-03-09 03:47:55');
INSERT INTO stages VALUES(6,'Final Interview',2,3,'2025-03-09 03:47:55','2025-03-09 03:47:55');
INSERT INTO stages VALUES(7,'Resume Screening',3,1,'2025-03-09 03:47:55','2025-03-09 03:47:55');
INSERT INTO stages VALUES(8,'Case Study',3,2,'2025-03-09 03:47:55','2025-03-09 03:47:55');
INSERT INTO stages VALUES(9,'Leadership Interview',3,3,'2025-03-09 03:47:55','2025-03-09 03:47:55');
CREATE TABLE openings (
	opening_id INTEGER NOT NULL, 
	title VARCHAR NOT NULL, 
	description VARCHAR NOT NULL, 
	requirements VARCHAR NOT NULL, 
	salary_range VARCHAR NOT NULL, 
	location VARCHAR NOT NULL, 
	is_remote BOOLEAN DEFAULT 0 NOT NULL, 
	is_active BOOLEAN DEFAULT 1 NOT NULL, 
	posted_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
	deadline DATETIME NOT NULL, 
	role_id INTEGER NOT NULL, 
	experience_required INTEGER DEFAULT 0 NOT NULL, 
	PRIMARY KEY (opening_id), 
	FOREIGN KEY(role_id) REFERENCES roles (role_id)
);
INSERT INTO openings VALUES(1,'Senior Software Engineer','Looking for an experienced software engineer','Python, FastAPI, React','-','Remote',0,1,'2025-03-09 03:48:02','2024-12-31',1,5);
INSERT INTO openings VALUES(2,'Data Scientist - ML','AI/ML position for recommendation systems','Python, TensorFlow, SQL','-','New York',0,1,'2025-03-09 03:48:02','2024-12-31',2,3);
INSERT INTO openings VALUES(3,'Product Manager - Growth','Lead our growth initiatives','Product management, Analytics','-','San Francisco',0,1,'2025-03-09 03:48:02','2024-12-31',3,4);
CREATE TABLE applications (
	application_id INTEGER NOT NULL, 
	candidate_id INTEGER NOT NULL, 
	opening_id INTEGER NOT NULL, 
	rating INTEGER, 
	role_id INTEGER NOT NULL, 
	application_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	attachments VARCHAR, 
	status VARCHAR DEFAULT 'PENDING' NOT NULL, 
	current_stage INTEGER DEFAULT 1 NOT NULL, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (application_id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (candidate_id), 
	FOREIGN KEY(current_stage) REFERENCES stages (stage_id), 
	FOREIGN KEY(opening_id) REFERENCES openings (opening_id), 
	FOREIGN KEY(role_id) REFERENCES roles (role_id)
);
INSERT INTO applications VALUES(1,1,1,5,1,'2024-03-09','1','PENDING',1,'2025-03-09 03:48:13','2025-03-09 03:48:13');
INSERT INTO applications VALUES(2,2,2,5,2,'2024-03-09','2','PENDING',1,'2025-03-09 03:48:13','2025-03-09 03:48:13');
INSERT INTO applications VALUES(3,3,3,4,3,'2024-03-09','3','PENDING',1,'2025-03-09 03:48:13','2025-03-09 03:48:13');
INSERT INTO applications VALUES(4,4,1,4,1,'2024-03-09','4','PENDING',1,'2025-03-09 03:56:58','2025-03-09 03:56:58');
INSERT INTO applications VALUES(5,5,2,5,2,'2024-03-09','5','PENDING',1,'2025-03-09 03:56:58','2025-03-09 03:56:58');
CREATE TABLE experiences (
	experience_id INTEGER NOT NULL, 
	application_id INTEGER NOT NULL, 
	company_name VARCHAR NOT NULL, 
	position VARCHAR NOT NULL, 
	description VARCHAR, 
	start_date DATETIME NOT NULL, 
	end_date DATETIME, 
	duration INTEGER, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (experience_id), 
	FOREIGN KEY(application_id) REFERENCES applications (application_id)
);
INSERT INTO experiences VALUES(1,1,'Tech Corp','Software Developer','Full-stack development','2020-01-01','2024-03-09',NULL,'2025-03-09 03:48:20','2025-03-09 03:48:20');
INSERT INTO experiences VALUES(2,2,'Data Inc','Data Analyst','Data analysis and ML','2019-01-01','2024-03-09',NULL,'2025-03-09 03:48:20','2025-03-09 03:48:20');
INSERT INTO experiences VALUES(3,3,'Product Co','Product Owner','Product management','2018-01-01','2024-03-09',NULL,'2025-03-09 03:48:20','2025-03-09 03:48:20');
INSERT INTO experiences VALUES(4,4,'Tech Solutions','Senior Developer','Backend development and team lead','2018-01-01','2024-03-09',NULL,'2025-03-09 03:57:03','2025-03-09 03:57:03');
INSERT INTO experiences VALUES(5,5,'AI Research Lab','Research Scientist','Machine learning research','2019-06-01','2024-03-09',NULL,'2025-03-09 03:57:03','2025-03-09 03:57:03');
CREATE INDEX ix_roles_role_id ON roles (role_id);
CREATE INDEX ix_candidates_candidate_id ON candidates (candidate_id);
CREATE INDEX ix_stages_stage_id ON stages (stage_id);
CREATE INDEX ix_openings_opening_id ON openings (opening_id);
CREATE INDEX ix_applications_application_id ON applications (application_id);
CREATE INDEX ix_experiences_experience_id ON experiences (experience_id);
COMMIT;
