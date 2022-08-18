import sqlite3

db = sqlite3.connect('db.db')

c = db.cursor()

# создание таблицы

c.execute("""CREATE TABLE pass(
    nik TEXT PRIMARY KEY,
    FIO_guest TEXT,
    FIO_user TEXT,
    time_of_action_pass TEXT,
    validity period_pass INT,
    status_pass INT
)""")
db.commit()

c.execute("""CREATE TABLE users(
   userid INT PRIMARY KEY,
   username TEXT,
   nik TEXT,
   FIO_user TEXT,
   number_of_active_passes INT
)""")
db.commit()



c.execute("INSERT INTO pass VALUES('johniety','Elena','Sveta','20/08/22 22:00','1','1')")
c.execute("INSERT INTO pass VALUES('einterdi','Peter','Roman','22/08/22 09:20','6','1')")
c.execute("INSERT INTO pass VALUES('catrictw','Veronica','Slava','20/08/22 13:00','0.5','1')")
c.execute("INSERT INTO pass VALUES('merilynd','Danil','Pavel','31/08/22 14:00','6','1')")
c.execute("INSERT INTO pass VALUES('nappaleg','Ivan','Jon','28/08/22 15:30','5','1')")
db.commit()

user1 = ('0','null', 'johniety', 'Sveta', '0')
user2 = ('1','null', 'einterdi', 'Roman', '0')
user3 = ('2','null','merilynd', 'Pavel', '2')
user4 = ('3','null', 'nappaleg', 'Jon', '1')
user5 = ('4','null','maryetta', 'Inga', '1')

c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", user1)
c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", user2)
c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", user3)
c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", user4)
c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", user5)

db.commit()


c.execute("SELECT * FROM users")
db.commit()
print(c.fetchall())

c.execute("SELECT * FROM pass")
db.commit()
print(c.fetchall())


db.close()
