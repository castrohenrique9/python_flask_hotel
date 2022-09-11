"""Create database and data"""

import sqlite3

connection = sqlite3.connect('banco.sqlite')
cursor = connection.cursor()

CRIA_TABELA = ("CREATE TABLE IF NOT EXISTS hoteis"
               +" (hotel_id text PRIMARY KEY, nome text, estrelas real, diaria real, cidade text)")

CRIA_HOTEL = "INSERT INTO hoteis VALUES ('castro', 'Castro Hotel', 4.3, 345.30, 'Rio de Janeiro')"

cursor.execute(CRIA_TABELA)
cursor.execute(CRIA_HOTEL)

connection.commit()
connection.close()
