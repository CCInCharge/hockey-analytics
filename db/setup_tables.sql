CREATE DATABASE hockey_analytics IF NOT EXISTS;
USE hockey_analytics;

CREATE TABLE teams (
    id VARCHAR(16) NOT NULL,
    year INT NOT NULL,
    name VARCHAR(64),
    PRIMARY KEY (id),
    CONSTRAINT Team UNIQUE (year, name)
) ENGINE = InnoDB;

CREATE TABLE games (
	id INT NOT NULL AUTO_INCREMENT,
	game_date DATE NOT NULL,
	url VARCHAR(128),
	away_team_id VARCHAR(16) NOT NULL,
	home_team_id VARCHAR(16) NOT NULL,
	away_team_goals INT NOT NULL,
	home_team_goals INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (away_team_id) REFERENCES teams(id),
	FOREIGN KEY (home_team_id) REFERENCES teams(id)
) ENGINE = InnoDB;

CREATE TABLE goals (
	id INT NOT NULL AUTO_INCREMENT,
	gid INT NOT NULL,
	tid VARCHAR(16) NOT NULL,
	time_of_goal TIME NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (gid) REFERENCES games(id),
	FOREIGN KEY (tid) REFERENCES teams(id)
) ENGINE = InnoDB;