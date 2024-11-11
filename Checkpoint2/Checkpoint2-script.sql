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
DROP TABLE Language;
DROP TABLE GameLanguages;
DROP TABLE Franchise;
DROP TABLE FranchiseGames;

CREATE TABLE Console (
    name VARCHAR(255) UNIQUE NOT NULL,
    manufacturer VARCHAR(255) UNIQUE NOT NULL,
    release_date DATE NOT NULL,
    handheld BOOLEAN NOT NULL,
    bit_length DECIMAL(3,0) NOT NULL,
    sales DECIMAL(12,0)
);

CREATE TABLE Game (
    name VARCHAR(255) UNIQUE NOT NULL,
    console_name VARCHAR(255) UNIQUE NOT NULL,
    console_manufacturer VARCHAR(255) UNIQUE NOT NULL,
    release_date DATE NOT NULL,
    genre VARCHAR(255) NOT NULL,
    sales DECIMAL(12,0),
    prequel_name VARCHAR(255),
    prequel_console VARCHAR(255),
    prequel_manufacturer VARCHAR(255)
);

CREATE TABLE Developer (
    name VARCHAR(255) UNIQUE NOT NULL,
    date_founded DATE
);

CREATE TABLE DeveloperGames (
    developer_name VARCHAR(255) UNIQUE NOT NULL,
    game_name VARCHAR(255) UNIQUE NOT NULL,
    console_name VARCHAR(255) UNIQUE NOT NULL,
    console_manufacturer VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Publisher (
    name VARCHAR(255) UNIQUE NOT NULL,
    date_founded DATE
);

CREATE TABLE PublisherGames (
    publisher_name VARCHAR(255) UNIQUE NOT NULL,
    game_name VARCHAR(255) UNIQUE NOT NULL,
    console_name VARCHAR(255) UNIQUE NOT NULL,
    console_manufacturer VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Region (
    name VARCHAR(255) UNIQUE NOT NULL,
    encoding_standard VARCHAR(255) NOT NULL
);

CREATE TABLE RegionGames (
    region_name VARCHAR(255) UNIQUE NOT NULL,
    game_name VARCHAR(255) UNIQUE NOT NULL,
    console_name VARCHAR(255) UNIQUE NOT NULL,
    console_manufacturer VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Accessory (
    name VARCHAR(255) UNIQUE NOT NULL,
    manufacturer VARCHAR(255) UNIQUE NOT NULL,
    release_date DATE NOT NULL,
    sales DECIMAL(12,0)
);

CREATE TABLE ConsoleAccessories (
    name VARCHAR(255) UNIQUE NOT NULL,
    manufacturer VARCHAR(255) UNIQUE NOT NULL,
    console_name VARCHAR(255) UNIQUE NOT NULL,
    console_manufacturer VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE GameAccessories (
    name VARCHAR(255) UNIQUE NOT NULL,
    manufacturer VARCHAR(255) UNIQUE NOT NULL,
    game_name DATE UNIQUE NOT NULL,
    console_name VARCHAR(255) UNIQUE NOT NULL,
    game_manufacturer VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Language (
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE GameLanguages (
    language_name VARCHAR(255) UNIQUE NOT NULL,
    game_name VARCHAR(255) UNIQUE NOT NULL,
    console_name VARCHAR(255) UNIQUE NOT NULL,
    game_manufacturer VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Franchise (
    name VARCHAR(255) UNIQUE NOT NULL,
    original_developer VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE FranchiseGames (
    name VARCHAR(255) UNIQUE NOT NULL,
    original_developer VARCHAR(255) UNIQUE NOT NULL,
    game_name DATE UNIQUE NOT NULL,
    console_name VARCHAR(255) UNIQUE NOT NULL,
    game_manufacturer VARCHAR(255) UNIQUE NOT NULL
);