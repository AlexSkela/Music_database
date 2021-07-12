from pprint import pprint

import sqlalchemy


dns = 'postgresql://postgres:@localhost:5432/musiclist'
engine = sqlalchemy.create_engine(dns)

connection = engine.connect()

pprint(sqlalchemy.inspect(engine).get_table_names())

pprint(connection.execute("""SELECT yearofrelease, namealbum FROM album
WHERE yearofrelease = 2018;""").fetchmany(10))

pprint(connection.execute("""SELECT nameoftrack, duration FROM track
ORDER BY duration DESC""").fetchmany(1))

pprint(connection.execute("""SELECT nameoftrack, duration FROM track
WHERE duration >= 3.50""").fetchmany(10))

pprint(connection.execute("""SELECT name_collection FROM collection
WHERE yearofrelease BETWEEN 2018 AND 2020""").fetchmany(10))

# connection.execute("""SELECT name FROM singer
# WHERE name""").fetchall()

pprint(connection.execute("""SELECT nameoftrack FROM track
WHERE nameoftrack LIKE '%%Моя%%'""").fetchmany(10))
