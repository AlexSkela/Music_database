from pprint import pprint

import sqlalchemy


dns = 'postgresql://postgres:@localhost:5432/musiclist'
engine = sqlalchemy.create_engine(dns)

connection = engine.connect()

pprint(sqlalchemy.inspect(engine).get_table_names())

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
INNER JOIN track t ON a.id = t.id_album
WHERE yearofrelease BETWEEN 2019 AND 2020
GROUP BY namealbum""").fetchmany(10))

pprint(connection.execute("""SELECT namealbum, AVG(t.duration) FROM album a
INNER JOIN track t ON a.id = t.id_album
GROUP BY namealbum""").fetchmany(10))

pprint(connection.execute("""SELECT s.name FROM singer s
INNER JOIN albumsinger asi ON s.id = asi.id_singer
INNER JOIN album al ON asi.id_album = al.id
WHERE yearofrelease != 2020""").fetchmany(10))

pprint(connection.execute("""SELECT c.name_collection FROM collection c
INNER JOIN collectiontrack ct ON c.id = ct.id_collection
INNER JOIN track tr ON ct.id_track = tr.id
INNER JOIN album ON tr.id_album = album.id
INNER JOIN albumsinger als ON album.id = als.id_album
INNER JOIN singer si ON als.id_singer = si.id
WHERE name = 'Баста'""").fetchmany(10))


pprint(connection.execute("""SELECT nameoftrack FROM track
LEFT JOIN collectiontrack ct ON track.id = ct.id_track
WHERE id_collection IS NULL""").fetchmany(10))

pprint(connection.execute("""SELECT name, tr.duration FROM singer
INNER JOIN albumsinger albsin ON singer.id = albsin.id_singer
INNER JOIN album alb ON albsin.id_album = alb.id
INNER JOIN track tr ON alb.id = tr.id
GROUP BY singer.name, tr.duration
ORDER BY tr.duration ASC""").fetchmany(1))

pprint(connection.execute("""SELECT namealbum, COUNT(tra.id_album) FROM album
INNER JOIN track tra ON album.id = tra.id_album
GROUP BY namealbum, tra.id_album
HAVING COUNT(tra.id_album) = 1""").fetchmany(3))