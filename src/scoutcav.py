import glob
import os
import platform  # Windows is not supported

from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from werkzeug.utils import secure_filename

# sqlite must be imorted after flask imports or it will generate an error, imports are handled by manage_db.py 

#local imports
import manage_db
import masscan_import
import scanner

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
# CONFIGURATION

# Define data/ directories for db, images, and imported xml
DB_DIR ='data/db/'
IMAGE_DIR = 'data/images/'
IMPORT_DIR ='data/import/'

ALLOWED_EXT_IMPORT = {'xml'}

app = Flask(__name__)

# Directory configuration
app.config['DB_DIR'] = DB_DIR
app.config['IMAGE_DIR'] = IMAGE_DIR
app.config['IMPORT_DIR'] = IMPORT_DIR

# Database selection
app.config['SELECTED_DB'] = 'scans.db'

def import_check_file_type(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT_IMPORT

# ROUTES

# Main view, displays hosts in a table
@app.route("/")
def view_main():
    active_page = 'hosts'

    rows = manage_db.load_database(app.config['DB_DIR'], app.config['SELECTED_DB'])

    return render_template("main.html", active_page = active_page, rows = rows)

# serve file from image directory
@app.route("/screen/<filename>")
def display_screenshot(filename):
    return send_from_directory(IMAGE_DIR, filename)

# RUN SCAN
@app.route("/scan")
def view_scan():
    active_page = 'scan'
    return render_template("scan.html", active_page=active_page)

@app.route("/run-scan", methods=['GET', 'POST'])
def run_scan():
    active_page = 'scan'
    if request.method == 'POST':
        filename = request.form.get('scan_filename', type=str)
        ip_addr = request.form.get('ip_addr')
        ports = request.form.get('ports').replace(" ", "")
        packet_rate = request.form.get('packet_rate')

    if filename.endswith(".xml"):
        filename = filename
    else:
        filename = filename+".xml"

    print("Starting scanner for IP/range: "+ip_addr)
    print("Scanning ports: "+ports)
    print("Saving as: "+filename)
    print("Packet Rate: "+packet_rate)
    
    scanner.run(filename, ip_addr, ports, packet_rate)
    return render_template("scan.html", active_page=active_page)


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
def config_db():
    active_page= 'manage_db'

    root_dir = os.getcwd() 
    # Get a list of available .db files in order to populate <select> element
    database_files = []
    os.chdir(DB_DIR)
    for db in glob.glob("*.db"):
        database_files.append(db)
    os.chdir(root_dir)

    return render_template("manage_db.html",database_files = database_files, active_page=active_page)

@app.route("/load_db", methods=['POST'])
def load_db(): 
    active_page= 'manage_db'
    return render_template("manage_db.html",active_page=active_page)

@app.route("/create_db", methods=['POST'])
def create_db():
    if request.method == 'POST':
        filename = request.form.get('filename', type=str)
        if not filename.endswith(".db"):
            filename = filename+".db"
    
        print("Creating database with filename:",filename)
        manage_db.create_db(app.config['DB_DIR'], filename)
        
    return  "Done."

@app.route("/save_db/<path:filename>") 
def save_db(filename):
    print("Downloading Database: " + filename)
    return send_from_directory(app.config['DB_DIR'], filename, mimetype='application/x-sqlite3')

@app.route("/import_db", methods=['GET', 'POST'])
def import_db():
    active_page= 'manage_db'
    return render_template("manage_db.html",active_page=active_page)

if __name__ == "__main__":
    if platform.system() == 'Windows':
        print("Must be run in a Linux environment, sorry. Try WSL")
    print(banner)
    app.run(debug=True, use_reloader=False, host="0.0.0.0")
