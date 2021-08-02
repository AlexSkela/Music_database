from pprint import pprint

import sqlalchemy


dns = 'postgresql://postgres:@localhost:5432/musiclist'
engine = sqlalchemy.create_engine(dns)

connection = engine.connect()

# pprint(sqlalchemy.inspect(engine).get_table_names())
#
# pprint(connection.execute("""SELECT yearofrelease, namealbum FROM album
# WHERE yearofrelease = 2018;""").fetchmany(10))
#
# pprint(connection.execute("""SELECT nameoftrack, duration FROM track
# ORDER BY duration DESC""").fetchmany(1))
#
# pprint(connection.execute("""SELECT nameoftrack, duration FROM track
# WHERE duration >= 3.50""").fetchmany(10))
#
# pprint(connection.execute("""SELECT name_collection FROM collection
# WHERE yearofrelease BETWEEN 2018 AND 2020""").fetchmany(10))
#
# # connection.execute("""SELECT name FROM singer
# # WHERE name""").fetchall()
#
# pprint(connection.execute("""SELECT nameoftrack FROM track
# WHERE nameoftrack LIKE '%%Моя%%'""").fetchmany(10))

pprint(connection.execute("""SELECT id_genre, COUNT(id_singer) FROM gendersinger
GROUP BY id_genre
ORDER BY COUNT(id_singer)""").fetchmany(10))

pprint(connection.execute("""SELECT namealbum, COUNT(t.nameoftrack) FROM album a
JOIN track t ON a.id = t.id_album
WHERE yearofrelease BETWEEN 2019 AND 2020
GROUP BY namealbum""").fetchmany(10))

pprint(connection.execute("""SELECT namealbum, AVG(t.duration) FROM album a
JOIN track t ON a.id = t.id_album
GROUP BY namealbum""").fetchmany(10))

pprint(connection.execute("""SELECT s.name FROM singer s
JOIN albumsinger asi ON s.id = asi.id_singer
JOIN album al ON asi.id_album = al.id
WHERE yearofrelease != 2020""").fetchmany(10))

pprint(connection.execute("""SELECT c.name_collection FROM collection c
JOIN collectiontrack ct ON c.id = ct.id_collection
JOIN track tr ON ct.id_track = tr.id
JOIN album ON tr.id_album = album.id
JOIN albumsinger als ON album.id = als.id_album
JOIN singer si ON als.id_singer = si.id
WHERE name = 'Баста'""").fetchmany(10))

pprint(connection.execute("""SELECT namealbum FROM album al
JOIN albumsinger alsi ON al.id = alsi.id_album
JOIN singer sin ON alsi.id_singer = sin.id
JOIN gendersinger gensi ON sin.id = gensi.id_singer
GROUP BY namealbum
HAVING COUNT(gensi.id_genre) > 1""").fetchmany(10))

pprint(connection.execute("""SELECT nameoftrack FROM track
LEFT JOIN collectiontrack ct ON track.id = ct.id_track
WHERE id_collection IS NULL""").fetchmany(10))

pprint(connection.execute("""SELECT name, tr.duration FROM singer
JOIN albumsinger albsin ON singer.id = albsin.id_singer
JOIN album alb ON albsin.id_album = alb.id
JOIN track tr ON alb.id = tr.id_album
GROUP BY singer.name, tr.duration
HAVING tr.duration = (
SELECT MIN(duration) FROM track)""").fetchmany(10))

pprint(connection.execute("""SELECT namealbum, COUNT(tra.id_album) FROM album
JOIN track tra ON album.id = tra.id_album
GROUP BY namealbum, tra.id_album
HAVING COUNT(tra.id_album) = (
SELECT MIN(id_album) FROM track)""").fetchmany(10))

