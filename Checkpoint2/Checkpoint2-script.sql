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
    console_name VARCHAR(255) NOT NULL,
    console_manufacturer VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    handheld BOOLEAN NOT NULL,
    bit_length DECIMAL(3,0) NOT NULL,
    sales DECIMAL(12,0),
	PRIMARY KEY (console_name)
);

CREATE TABLE Game (
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    genre VARCHAR(255) NOT NULL,
    sales DECIMAL(12,0),
    sequel_name VARCHAR(255),
    sequel_console VARCHAR(255),
	PRIMARY KEY (game_name, console_name)
);

CREATE TABLE Developer (
    developer_name VARCHAR(255) NOT NULL,
    date_founded DATE,
	PRIMARY KEY (developer_name)
);

CREATE TABLE DeveloperGames (
    developer_name VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (developer_name, game_name, console_name)
);

CREATE TABLE Publisher (
    publisher_name VARCHAR(255) NOT NULL,
    date_founded DATE,
	PRIMARY KEY (publisher_name)
);

CREATE TABLE PublisherGames (
    publisher_name VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (publisher_name, game_name, console_name)
);

CREATE TABLE Region (
    region_name VARCHAR(255) NOT NULL,
    encoding_standard VARCHAR(255) NOT NULL,
	PRIMARY KEY (region_name)
);

CREATE TABLE RegionGames (
    region_name VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (region_name, game_name, console_name)
);

CREATE TABLE Accessory (
    accessory_name VARCHAR(255) NOT NULL,
    accessory_manufacturer VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    sales DECIMAL(12,0),
	PRIMARY KEY (accessory_name, accessory_manufacturer)
);

CREATE TABLE ConsoleAccessories (
    accessory_name VARCHAR(255) NOT NULL,
    accessory_manufacturer VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (accessory_name, accessory_manufacturer, console_name)
);

CREATE TABLE GameAccessories (
    accessory_name VARCHAR(255) NOT NULL,
    accessory_manufacturer VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (accessory_name, accessory_manufacturer, game_name, console_name)
);

CREATE TABLE Languages (
    language_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (language_name)
);

CREATE TABLE GameLanguages (
    language_name VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (language_name, game_name, console_name)
);

CREATE TABLE Franchise (
    franchise_name VARCHAR(255) NOT NULL,
    original_developer VARCHAR(255) NOT NULL,
	PRIMARY KEY (franchise_name)
);

CREATE TABLE FranchiseGames (
    franchise_name VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL,
    console_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (franchise_name, game_name, console_name)
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

-- 1 .Console with the highest sales for each manufacturer with more than one console
SELECT c.console_manufacturer, c.console_name, MAX(c.sales)
FROM Console c
GROUP BY c.console_manufacturer HAVING COUNT(DISTINCT c.console_name) > 1;

-- 2. Console and handheld with the lowest sales for each manufacturer
SELECT c.console_manufacturer, c.console_name, MIN(c.sales)
FROM Console c
WHERE c.sales IS NOT NULL
GROUP BY c.console_manufacturer, c.handheld;

-- 3. Most recently released game for each console
SELECT c.console_name, g.game_name, MAX(g.release_date)
FROM Console c, Game g
WHERE c.console_name = g.console_name
GROUP BY c.console_name;

-- 4. All languages for Super Mario 64
SELECT l.language_name
FROM Languages l, GameLanguages gl
WHERE l.language_name = gl.language_name AND gl.game_name LIKE 'Super Mario 64' AND gl.console_name LIKE 'Nintendo 64';

-- 5. All games with a Switch sequel
SELECT g.game_name, g.sequel_name, g.sequel_console
FROM Game g, FranchiseGames fg
WHERE g.game_name = fg.game_name AND g.console_name = fg.console_name AND g.sequel_console LIKE 'Switch';

-- 6. Game with the highest sales that uses an accessory
SELECT g.game_name, g.console_name, MAX(g.sales), a.accessory_name, a.accessory_manufacturer
FROM Game g, GameAccessories ga, Accessory a
WHERE g.game_name = ga.game_name AND g.console_name = ga.console_name AND
ga.accessory_name = a.accessory_name AND ga.accessory_manufacturer = a.accessory_manufacturer;

-- 7. All games in spanish
SELECT g.game_name, g.console_name
FROM Game g, GameLanguages gl, Languages l
WHERE g.game_name = gl.game_name AND g.console_name = gl.console_name AND gl.language_name = l.language_name AND l.language_name LIKE 'Spanish';

-- 8. Games that belong to two different franchises
SELECT game_name, console_name
FROM FranchiseGames
GROUP BY game_name, console_name HAVING COUNT(DISTINCT franchise_name) > 1;

-- 9. Games with a developer and publisher of the same name
SELECT dg.game_name, dg.console_name, dg.developer_name, pg.publisher_name
FROM DeveloperGames dg, PublisherGames pg
WHERE dg.game_name = pg.game_name AND dg.console_name = pg.console_name AND dg.developer_name = pg.publisher_name
LIMIT 10;

-- 10. English games released in Japan
SELECT rg.region_name, rg.game_name, rg.console_name
FROM RegionGames rg, GameLanguages gl
WHERE rg.game_name = gl.game_name AND rg.console_name = gl.console_name AND rg.region_name LIKE 'Japan' AND gl.language_name LIKE 'English';

-- 11. Accessories not designed for any game
SELECT ca.accessory_name, ca.console_name
FROM ConsoleAccessories ca
EXCEPT
SELECT ga.accessory_name, ga.console_name
FROM GameAccessories ga;

-- 12. Amount of days between the date a developer team was founded and their first game
SELECT d.developer_name, MIN(g.release_date), d.date_founded, JULIANDAY(MIN(g.release_date)) - JULIANDAY(d.date_founded) AS "Days passed"
FROM Game g, DeveloperGames dg, Developer d
WHERE g.game_name = dg.game_name AND g.console_name = dg.console_name AND dg.developer_name = d.developer_name
GROUP BY d.developer_name;

-- 13. Number of consoles in each bit length
SELECT c.bit_length, COUNT(c.console_name)
FROM Console c
GROUP BY c.bit_length;

-- 14. First game to release in every bit length
SELECT c.bit_length, g.game_name, g.console_name, MIN(g.release_date)
FROM Console c, Game g
WHERE c.console_name = g.console_name
GROUP BY c.bit_length;

-- 15. Add new games to Game table
INSERT INTO Game VALUES
('Yakuza: Like a Dragon', 'PlayStation 5', '2020-01-16', 'Role-Playing', null, 'Like a Dragon: Infinite Wealth', 'PlayStation 4'), 
('Like a Dragon: Infinite Wealth', 'PlayStation 5', '2024-01-26', 'Role-Playing', null, null, null), 
('Like a Dragon: Pirate Yakuza in Hawaii', 'PlayStation 5', '2025-02-21', 'Action-Adventure', null, null, null);

-- 16. Update game info when a sequel is released/announced
UPDATE Game SET sequel_name = 'Hollow Knight: Silksong', sequel_console = 'Switch' WHERE game_name LIKE 'Hollow Knight' AND console_name LIKE 'Switch';

-- 17. Delete a game if it gets cancelled
DELETE FROM Game WHERE game_name LIKE 'Castlevania: Resurrection' AND console_name LIKE 'Dreamcast';

-- 18. All Xbox Series X/PlayStation 5 games released after Yakuza: Like a Dragon
SELECT g.game_name, g.console_name, g.release_date
FROM Game g
WHERE g.console_name IN ('Xbox Series X', 'PlayStation 5') AND g.release_date >=
(SELECT g.release_date
FROM Game g
WHERE g.game_name LIKE 'Yakuza: Like a Dragon' AND g.console_name LIKE 'PlayStation 5');

-- 19. All SNES games released within 6 months of the console release date
SELECT g.game_name, g.release_date
FROM Game g, Console c
WHERE g.console_name = c.console_name AND g.console_name LIKE 'Super Nintendo Entertainment System' AND g.release_date <= DATE(c.release_date, '+6 months')
ORDER BY g.release_date;

-- 20. Franchise with the most sales
SELECT name, MAX(franchise_sales)
FROM (SELECT fg.franchise_name AS "name", SUM(g.sales) AS "franchise_sales"
FROM FranchiseGames fg, Game g
WHERE fg.game_name = g.game_name AND fg.console_name = g.console_name
GROUP BY fg.franchise_name);