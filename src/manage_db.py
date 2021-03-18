import sqlite3 as sql

# loads the selected database for host view 
def load_database(path, filename):
    conn = sql.connect(path+filename)
    conn.row_factory = sql.Row

    c = conn.cursor()
    # create the table if doesn't exist
    print("creating table")
    c.execute('''CREATE TABLE IF NOT EXISTS hosts(
                 host_id INTEGER PRIMARY KEY,
                 hostname TEXT,
                 ip TEXT,
                 port INTEGER,
                 service TEXT,
                 continent TEXT,
                 country TEXT,
                 city TEXT,
                 lat TEXT,
                 long TEXT,
                 img_file TEXT,
                 UNIQUE(ip, port))''')
    conn.commit()


    c.execute("SELECT * FROM hosts")

    rows = c.fetchall()

    return rows

# will create a database but not open it within the host view
def create_db(path, filename):
    conn = sql.connect(path+filename)

    c = conn.cursor()
    # create the table if doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS hosts(
                 host_id INTEGER PRIMARY KEY,
                 hostname TEXT,
                 ip TEXT,
                 port INTEGER,
                 service TEXT,
                 continent TEXT,
                 country TEXT,
                 city TEXT,
                 lat TEXT,
                 long TEXT,
                 img_file TEXT,
                 UNIQUE(ip, port))''')
    conn.commit()
