DROP TABLE Console;
DROP TABLE Game;
DROP TABLE Developer;
DROP TABLE DeveloperGames;
DROP TABLE Publisher;
DROP TABLE PublisherGames;
DROP TABLE Region;
DROP TABLE RegionGames;
DROP TABLE Accessory;
DROP TABLE ConsoleAccessories;
DROP TABLE GameAccessories;
DROP TABLE Languages;
DROP TABLE GameLanguages;
DROP TABLE Franchise;
DROP TABLE FranchiseGames;

CREATE TABLE Console (
    name VARCHAR(255) NOT NULL,
    manufacturer VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    handheld BOOLEAN NOT NULL,
    bit_length DECIMAL(3,0) NOT NULL,
    sales DECIMAL(12,0),
	PRIMARY KEY (name)
);

CREATE TABLE Game (
    name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    genre VARCHAR(255) NOT NULL,
    sales DECIMAL(12,0),
    sequel_name VARCHAR(255),
    sequel_console VARCHAR(255),
	PRIMARY KEY (name, console_name)
);

CREATE TABLE Developer (
    name VARCHAR(255) NOT NULL,
    date_founded DATE,
	PRIMARY KEY (name)
);

CREATE TABLE DeveloperGames (
    developer_name VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (developer_name, game_name, console_name)
);

CREATE TABLE Publisher (
    name VARCHAR(255) NOT NULL,
    date_founded DATE,
	PRIMARY KEY (name)
);

CREATE TABLE PublisherGames (
    publisher_name VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (publisher_name, game_name, console_name)
);

CREATE TABLE Region (
    name VARCHAR(255) NOT NULL,
    encoding_standard VARCHAR(255) NOT NULL,
	PRIMARY KEY (name)
);

CREATE TABLE RegionGames (
    region_name VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (region_name, game_name, console_name)
);

CREATE TABLE Accessory (
    name VARCHAR(255) NOT NULL,
    manufacturer VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    sales DECIMAL(12,0),
	PRIMARY KEY (name, manufacturer)
);

CREATE TABLE ConsoleAccessories (
    name VARCHAR(255) NOT NULL,
    manufacturer VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (name, manufacturer, console_name)
);

CREATE TABLE GameAccessories (
    name VARCHAR(255) NOT NULL,
    manufacturer VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (name, manufacturer, game_name, console_name)
);

CREATE TABLE Languages (
    name VARCHAR(255) NOT NULL,
	PRIMARY KEY (name)
);

CREATE TABLE GameLanguages (
    language_name VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (language_name, game_name, console_name)
);

CREATE TABLE Franchise (
    name VARCHAR(255) NOT NULL,
    original_developer VARCHAR(255) NOT NULL,
	PRIMARY KEY (name)
);

CREATE TABLE FranchiseGames (
    name VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (name, game_name, console_name)
);

.separator |
.import console.tbl Console
.import game.tbl Game
.import developer.tbl Developer
.import developergames.tbl DeveloperGames
.import publisher.tbl Publisher
.import publishergames.tbl PublisherGames
.import region.tbl Region
.import regiongames.tbl RegionGames
.import accessory.tbl Accessory
.import consoleaccessories.tbl ConsoleAccessories
.import gameaccessories.tbl GameAccessories
.import languages.tbl Languages
.import gamelanguages.tbl GameLanguages
.import franchise.tbl Franchise
.import franchisegames.tbl FranchiseGames

-- Console with the highest sales for each manufacturer with more than one console
SELECT c.manufacturer, c.name, MAX(c.sales)
FROM Console c
GROUP BY c.manufacturer HAVING COUNT(DISTINCT c.name) > 1;

-- Console and handheld with the lowest sales for each manufacturer
SELECT c.manufacturer, c.name, MIN(c.sales)
FROM Console c
GROUP BY c.manufacturer, c.handheld;

-- Most recently released game for each console
SELECT c.name, g.name, MAX(g.release_date)
FROM Console c, Game g
WHERE c.name = g.console_name
GROUP BY c.name;

-- All languages for Super Mario 64
SELECT l.name
FROM Languages l, GameLanguages gl
WHERE l.name = gl.language_name AND gl.game_name LIKE 'Super Mario 64' AND gl.console_name LIKE 'Nintendo 64';

-- All games and their sequel (if it exists) in the Mario Franchise
SELECT g.name, g.sequel_name, g.sequel_console
FROM Game g, FranchiseGames fg, Franchise f
WHERE g.name = fg.game_name AND g.console_name = fg.console_name AND fg.name = f.name 
AND f.name LIKE 'Mario' AND g.sequel_name IS NOT NULL
ORDER BY g.release_date ASC;