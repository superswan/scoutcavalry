import os

import xml.etree.ElementTree as ET
import socket
import sqlite3
import shutil

#Local imports
# program-specific imports, see each file for more info
# Print ANSI colors | see bcolors.py
from bcolors import bcolors

# see geolocation.py
import geolocation

#see webscreen.py
import webscreen

# get absolute path of running script
current_abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.abspath(os.getcwd()))
data_dir = os.path.join(current_abs_path, "data")
db_dir = os.path.join(data_dir, "db")
import_dir = os.path.join(current_abs_path, "import")
image_dir = os.path.join(current_abs_path, "images")

# create connection to db

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    
    #c = conn.cursor()
   
    return conn

def create_host(conn, host):
    sql = ''' INSERT INTO
    hosts(hostname,ip,port,service,continent,country,city,lat,long,img_file)
    VALUES(?,?,?,?,?,?,?,?,?,?)'''

    c = conn.cursor()
    c.execute(sql, host)
    conn.commit()
    return c.lastrowid

def xmlImport(filename, db_name):
    database = f"{db_dir}/{db_name}"

    # Readin in XML Doc for parsing
    tree = ET.parse(filename)
    root = tree.getroot()
    conn = create_connection(database)
    hosts = root.findall('host')
    host_count = len(hosts)
    
    print(f"{bcolors.OKBLUE}Importing {host_count}{bcolors.ENDC}")
    for host in hosts:
    # Get hosts and add to host_data 
        ip_addr = host.find('address').attrib.get('addr')
        port_id = host.find('ports').find('port').attrib.get('portid')
        service_id = None
        hostname = None
        img_file = None

             
        try:
            service_id = socket.getservbyport(int(port_id))
        except:
            pass

        if service_id is None:
           service_id = "Unknown"

       # get hostname, set to None if unavailable
        try:
            print(f"{bcolors.OKBLUE}[+] Resolving hostname for {ip_addr}...{bcolors.ENDC}")
            hostname = socket.gethostbyaddr(ip_addr)
        except:
            print(f"{bcolors.FAIL}[!] Could not resolve hostname{bcolors.ENDC}")
            pass
        
        if hostname is None:
            hostname = None
        else: hostname = hostname[0]
        
        # get screenshot of http or https service
        if service_id == 'http' or service_id == 'https':
            if hostname is None:
                hostname = "N/A"
                url = f"{service_id}://{ip_addr}:{port_id}"
            else:
                url = f"{service_id}://{hostname}"
            
            try:
               img_file = webscreen.getWebScreen(url)
               # move image file to data/images directory 
            except:
               pass
        
        elif img_file is None:       
            img_file = "unavailable"
            print(f"{bcolors.WARNING}[*] Unable to capture screenshot{bcolors.ENDC}")
        

        # get geolocation data
        continent,country,city,latitude,longitude = geolocation.getGeoLoc(ip_addr)
        print(f"{bcolors.OKBLUE}[+] submitting:\t{hostname}({ip_addr}:{port_id}, {service_id}) to database{bcolors.ENDC}")
        host_data = (hostname,ip_addr,int(port_id),service_id,continent,country,city,latitude,longitude,img_file)
        with conn:
            try:
                host_id = create_host(conn, host_data)
                print(f"{bcolors.OKGREEN}[*] Successfully created host with ID:\t{host_id}{bcolors.ENDC}\n\n")
            except Exception as e:
                print(f"{bcolors.FAIL}[!] Skipping duplicate entry...{bcolors.ENDC}\n\n")
                print(e)
                pass
        
    print(f"{bcolors.OKBLUE}[*] Finished {bcolors.ENDC}")






