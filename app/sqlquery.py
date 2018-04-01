import sqlite3 as sql

conn = sql.connect('database.db')
print "Opened database successfully";

conn.execute('drop table if exists users')
conn.execute('CREATE TABLE users (username text not null, password text not null, topic text, CONSTRAINT PK_users PRIMARY KEY (username))')
conn.commit()
print "Table created successfully";

conn.execute('insert into users (username, password, topic) values ("mahim", "mahim", "owntracks/nwgmhdaf/oneplus3t")')
conn.commit()
conn.execute('insert into users (username, password, topic) values ("saket", "saket", "owntracks/nwgmhdaf/h1")')
conn.commit()
conn.execute('insert into users (username, password, topic) values ("admin", "admin", "all")')
conn.commit()
print "data inserted successfully";
conn.close()

def check_credentials(username,password):
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute('Select COUNT(*) from users where username = ? and password = ?', (username, password))
    count = cur.fetchall()
    conn.close()
    return count

def get_topic(username,password):
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute('Select topic from users where username = ? and password = ?', (username, password))
    topic = cur.fetchall()
    conn.close()
    return topic	