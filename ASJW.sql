CREATE TABLE SAMOCHODY
	(ID_samochodu INTEGER,
	ladownosc INTEGER NOT NULL,
	miejsce_przebywania TEXT,
	PRIMARY KEY(ID_samochodu));
CREATE TABLE ZLECENIA
	(ID_zlecenia INTEGER,
	skad TEXT NOT NULL,
	dokad TEXT NOT NULL,
	masa INTEGER NOT NULL,
	data_przyjscia DATE NOT NULL,
	PRIMARY KEY(ID_zlecenia));
CREATE TABLE WYKONANIA
	(ID_wykonania INTEGER,
	ID_zlecenia INTEGER,
	ID_samochodu INTEGER,
	data_wykonania DATE,
	PRIMARY KEY(ID_wykonania),
	FOREIGN KEY(ID_zlecenia) REFERENCES ZLECENIA(ID_zlecenia),
	FOREIGN KEY(ID_samochodu) REFERENCES SAMOCHODY(ID_samochodu));
CREATE TABLE ZAKONCZENIA
	(ID_zakonczenia INTEGER,
	data_zakonczenia DATE NOT NULL,
	ID_wykonania INTEGER NOT NULL,
	status TEXT NOT NULL,
	PRIMARY KEY(ID_zakonczenia),
	FOREIGN KEY(ID_wykonania) REFERENCES WYKONANIA(ID_wykonania));
CREATE TABLE PUNKTY_MAPY
	(nr_trasy INTEGER,
	miejscowosc_A TEXT NOT NULL,
	miejscowosc_B TEXT NOT NULL,
	czas INTEGER NOT NULL);

/*Mapa:*/
INSERT INTO PUNKTY_MAPY VALUES (1, 'Szczecin', 'Koszalin', 140);
INSERT INTO PUNKTY_MAPY VALUES (2, 'Szczecin', 'Piła', 140);
INSERT INTO PUNKTY_MAPY VALUES (3, 'Szczecin', 'Gorzów Wielk.', 70);
INSERT INTO PUNKTY_MAPY VALUES (4, 'Gorzów Wielk.', 'A', 40);
INSERT INTO PUNKTY_MAPY VALUES (5, 'A', 'Zielona Góra', 40);
INSERT INTO PUNKTY_MAPY VALUES (6, 'A', 'Poznań', 90);
INSERT INTO PUNKTY_MAPY VALUES (7, 'Zielona Góra', 'Legnica', 80);
INSERT INTO PUNKTY_MAPY VALUES (8, 'Legnica', 'Wrocław', 80);
INSERT INTO PUNKTY_MAPY VALUES (9, 'Koszalin', 'Piła', 120);
INSERT INTO PUNKTY_MAPY VALUES (10, 'Piła', 'Poznań', 100);
INSERT INTO PUNKTY_MAPY VALUES (11, 'Poznań', 'Leszno', 90);
INSERT INTO PUNKTY_MAPY VALUES (12, 'Leszno', 'Wrocław', 60);
INSERT INTO PUNKTY_MAPY VALUES (13, 'Wrocław', 'Sieradz', 110);
INSERT INTO PUNKTY_MAPY VALUES (14, 'Wrocław', 'Opole', 90);
INSERT INTO PUNKTY_MAPY VALUES (15, 'Koszalin', 'Gdańsk', 170);
INSERT INTO PUNKTY_MAPY VALUES (16, 'Piła', 'Bydgoszcz', 90);
INSERT INTO PUNKTY_MAPY VALUES (17, 'Poznań', 'Konin', 80);
INSERT INTO PUNKTY_MAPY VALUES (18, 'Konin', 'Łódź', 90);
INSERT INTO PUNKTY_MAPY VALUES (19, 'Sieradz', 'Łódź', 50);
INSERT INTO PUNKTY_MAPY VALUES (20, 'Opole', 'Katowice', 90);
INSERT INTO PUNKTY_MAPY VALUES (21, 'Gdańsk', 'Elbląg', 40);
INSERT INTO PUNKTY_MAPY VALUES (22, 'Gdańsk', 'B', 90);
INSERT INTO PUNKTY_MAPY VALUES (23, 'B', 'Bydgoszcz', 70);
INSERT INTO PUNKTY_MAPY VALUES (24, 'Bydgoszcz', 'Toruń', 50);
INSERT INTO PUNKTY_MAPY VALUES (25, 'B', 'Toruń', 50);
INSERT INTO PUNKTY_MAPY VALUES (26, 'Toruń', 'D', 150);
INSERT INTO PUNKTY_MAPY VALUES (27, 'Toruń', 'Łódź', 120);
INSERT INTO PUNKTY_MAPY VALUES (28, 'Piotrków Tryb.', 'Częstochowa', 70);
INSERT INTO PUNKTY_MAPY VALUES (29, 'Częstochowa', 'Katowice', 80);
INSERT INTO PUNKTY_MAPY VALUES (30, 'Katowice', 'Kraków', 80);
INSERT INTO PUNKTY_MAPY VALUES (31, 'Elbląg', 'C', 50);
INSERT INTO PUNKTY_MAPY VALUES (32, 'C', 'Olsztyn', 40);
INSERT INTO PUNKTY_MAPY VALUES (33, 'C', 'D', 120);
INSERT INTO PUNKTY_MAPY VALUES (34, 'D', 'Warszawa', 50);
INSERT INTO PUNKTY_MAPY VALUES (35, 'Łódź', 'Warszawa', 110);
INSERT INTO PUNKTY_MAPY VALUES (36, 'Łódź', 'Piotrków Tryb.', 50);
INSERT INTO PUNKTY_MAPY VALUES (37, 'Piotrków Tryb.', 'Radom', 100);
INSERT INTO PUNKTY_MAPY VALUES (38, 'Piotrków Tryb.', 'Kielce', 100);
INSERT INTO PUNKTY_MAPY VALUES (39, 'Kielce', 'Kraków', 100);
INSERT INTO PUNKTY_MAPY VALUES (40, 'Kraków', 'Tarnów', 70);
INSERT INTO PUNKTY_MAPY VALUES (41, 'Olsztyn', 'Ełk', 140);
INSERT INTO PUNKTY_MAPY VALUES (42, 'Ełk', 'Łomża', 80);
INSERT INTO PUNKTY_MAPY VALUES (43, 'Łomża', 'E', 40);
INSERT INTO PUNKTY_MAPY VALUES (44, 'Warszawa', 'E', 110);
INSERT INTO PUNKTY_MAPY VALUES (45, 'Warszawa', 'Radom', 110);
INSERT INTO PUNKTY_MAPY VALUES (46, 'Radom', 'Kielce', 70);
INSERT INTO PUNKTY_MAPY VALUES (47, 'Ełk', 'Białystok', 90);
INSERT INTO PUNKTY_MAPY VALUES (48, 'E', 'Białystok', 30);
INSERT INTO PUNKTY_MAPY VALUES (49, 'Białystok', 'Lublin', 210);
INSERT INTO PUNKTY_MAPY VALUES (50, 'Warszawa', 'Lublin', 150);
INSERT INTO PUNKTY_MAPY VALUES (51, 'Radom', 'Lublin', 90);
INSERT INTO PUNKTY_MAPY VALUES (52, 'Kielce', 'Tarnobrzeg', 100);
INSERT INTO PUNKTY_MAPY VALUES (53, 'Lublin', 'F', 100);
INSERT INTO PUNKTY_MAPY VALUES (54, 'Tarnobrzeg', 'F', 40);
INSERT INTO PUNKTY_MAPY VALUES (55, 'F', 'Rzeszów', 50);
INSERT INTO PUNKTY_MAPY VALUES (56, 'Tarnów', 'Rzeszów', 60);

/*Kierowcy:*/
INSERT INTO SAMOCHODY VALUES (1, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (2, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (3, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (4, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (5, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (6, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (7, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (8, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (9, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (10, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (11, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (12, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (13, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (14, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (15, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (16, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (17, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (18, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (19, 1000, 'Łódź');
INSERT INTO SAMOCHODY VALUES (20, 1000, 'Łódź');