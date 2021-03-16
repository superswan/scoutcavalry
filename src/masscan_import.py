import xml.etree.ElementTree as ET
import socket
import sqlite3
import shutil

# program-specific imports, see each file for more info
# Print ANSI colors | see bcolors.py
from bcolors import bcolors

# see geolocation.py
import geolocation

#see webscreen.py
import webscreen
 
# create connection to db

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    c = conn.cursor()
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
    
    return conn

def create_host(conn, host):
    sql = ''' INSERT INTO
    hosts(hostname,ip,port,service,continent,country,city,lat,long,img_file)
    VALUES(?,?,?,?,?,?,?,?,?,?)'''

    c = conn.cursor()
    c.execute(sql, host)
    conn.commit()
    return c.lastrowid

# Readin in XML Doc for parsing
def xmlImport(filename):
    database = '../data/db/scans.db'
    tree = ET.parse(filename)
    root = tree.getroot()
    conn = create_connection(database)
    hosts = root.findall('host')

    for host in hosts:
    # Get hosts and add to host_data 
        ip_addr = host.find('address').attrib.get('addr')
        port_id = host.find('ports').find('port').attrib.get('portid')
        service_id = None
        hostname = None
        img_file = None
        continent,country,city,latitude,longitude = geolocation.getGeoLoc(ip_addr)
      
        try:
            service_id = socket.getservbyport(int(port_id))
        except:
            pass

        if service_id is None:
           service_id = "Unknown"

       # get hostname, set to "N/A" if unavailable
        try:
            hostname = socket.gethostbyaddr(ip_addr)
        except:
            pass
        if hostname is None:
            hostname = "N/A"
        else: hostname = hostname[0]
        
        # get screenshot of http or https service
        if service_id == 'http' or service_id == 'https':
           if hostname is not None:
               url = f"{service_id}://{hostname}"
               img_file = webscreen.getWebScreen(url)
           else:
               url = f"{service_id}://{ip_addr}:{port_id}"
               img_file = webscreen.getWebScreen(url)

        if img_file is None:
            img_file = "unavailable"
        # move image file to data/ directory 
        try:
            shutil.move(img_file, '../data/images/')
        except:
            pass


        print(f"{bcolors.OKBLUE}[+] submitting:\t{hostname}({ip_addr}:{port_id}) to database{bcolors.ENDC}")
        host_data = (hostname,ip_addr,int(port_id),service_id,continent,country,city,latitude,longitude,img_file)
        with conn:
            try:
                host_id = create_host(conn, host_data)
                print(f"{bcolors.OKGREEN}[*] Successfully created host with HOST ID:\t{host_id}{bcolors.ENDC}")
            except:
                print(f"{bcolors.FAIL}[!] Skipping duplicate entry...{bcolors.ENDC}")
                pass






