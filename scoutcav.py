from flask import Flask
from flask import flash, render_template, request, redirect, send_from_directory, url_for
import sqlite3 as sql
import platform # Windows is not supported

from werkzeug.utils import secure_filename
#local imports
import masscan_import

# banner cause had to
banner = """
  ██████ ▄████▄  ▒█████   █    ██ ▄▄▄█████▓    ▄████▄   ▄▄▄    ██▒   █▓ ▄▄▄       ██▓     ██▀███ ▓██   ██▓
▒██    ▒▒██▀ ▀█ ▒██▒  ██▒ ██  ▓██▒▓  ██▒ ▓▒   ▒██▀ ▀█  ▒████▄ ▓██░   █▒▒████▄    ▓██▒    ▓██ ▒ ██▒▒██  ██▒
░ ▓██▄  ▒▓█    ▄▒██░  ██▒▓██  ▒██░▒ ▓██░ ▒░   ▒▓█    ▄ ▒██  ▀█▄▓██  █▒░▒██  ▀█▄  ▒██░    ▓██ ░▄█ ▒ ▒██ ██░
  ▒   ██▒▓▓▄ ▄██▒██   ██░▓▓█  ░██░░ ▓██▓ ░    ▒▓▓▄ ▄██▒░██▄▄▄▄██▒██ █░░░██▄▄▄▄██ ▒██░    ▒██▀▀█▄   ░ ▐██▓░
▒██████▒▒ ▓███▀ ░ ████▓▒░▒▒█████▓   ▒██▒ ░    ▒ ▓███▀ ░ ▓█   ▓██▒▒▀█░   ▓█   ▓██▒░██████▒░██▓ ▒██▒ ░ ██▒▓░
▒ ▒▓▒ ▒ ░ ░▒ ▒  ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒   ▒ ░░      ░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▐░   ▒▒   ▓▒█░░ ▒░▓  ░░ ▒▓ ░▒▓░  ██▒▒▒
░ ░▒  ░ ░ ░  ▒    ░ ▒ ▒░ ░░▒░ ░ ░     ░         ░  ▒     ▒   ▒▒ ░░ ░░    ▒   ▒▒ ░░ ░ ▒  ░  ░▒ ░ ▒░▓██ ░▒░
░  ░  ░ ░       ░ ░ ░ ▒   ░░░ ░ ░   ░         ░          ░   ▒     ░░    ░   ▒     ░ ░     ░░   ░ ▒ ▒ ░░
      ░ ░ ░         ░ ░     ░                 ░ ░            ░  ░   ░        ░  ░    ░  ░   ░     ░ ░
        ░                                     ░                    ░                              ░ ░
53 63 6F 75 74                                43 61 76 61 6C 72 79 


"""


# Define data/ directories for db, images, and imported xml
DB_DIR ='data/db/'
IMAGE_DIR = 'data/images/'
IMPORT_DIR ='data/import/'

ALLOWED_EXT_IMPORT = {'xml'}

app = Flask(__name__)
app.config['IMPORT_DIR'] = IMPORT_DIR

def import_check_file_type(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT_IMPORT

@app.route("/")
def view_main():
    active_page = 'hosts'

    conn = sql.connect("data/db/scans.db")
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

    rows = c.fetchall();
    return render_template("main.html", active_page = active_page, rows = rows)

@app.route("/screen/<filename>")
def display_screenshot(filename):
    if filename != "unavailable":
        return send_from_directory(IMAGE_DIR, filename)


# SCAN IMPORTING
@app.route("/import")
def view_import():
    active_page = 'import'
    return render_template("import.html", active_page=active_page)

@app.route("/upload-import", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['filename']
        f.save(secure_filename(f.filename))
        
        masscan_import.xmlImport(f.filename, 'scans.db')
    return render_template("import.html")

# DATABASE MANAGEMENT
@app.route("/database")
def manage_db():
    active_page= 'manage_db'
    return render_template("manage_db.html",active_page=active_page)

@app.route("/load_db")
def load_db():
    active_page= 'manage_db'
    return render_template("manage_db.html",active_page=active_page)

@app.route("/create_db")
def create_db():
    active_page= 'manage_db'
    return render_template("manage_db.html",active_page=active_page)

@app.route("/save_db")
def save_db():
    active_page= 'manage_db'
    return render_template("manage_db.html",active_page=active_page)

@app.route("/import_db")
def import_db():
    active_page= 'manage_db'
    return render_template("manage_db.html",active_page=active_page)

if __name__ == "__main__":
    if platform.system() == 'Windows':
        print("Must be run in a Linux environment, sorry. Try WSL")
    print(banner)
    app.run(debug=True, use_reloader=False, host="0.0.0.0")
