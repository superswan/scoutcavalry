"""
Code is based on slyd0g's pwnVNC
https://github.com/slyd0g/pwnVNC

More info here:
https://grumpy-sec.blogspot.com/2017/02/scanning-entire-internet.html
"""
import socket
import os

from bcolors import bcolors

# takes a screen screenshot of VNC connection. Will only connect when authentication is disabled on VNC
def getVncScreen(ip_addr, port):
    vnc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vnc_socket.settimeout(0.5)
    try:
        # attmept to create TCP handshake and do authentication check using RFB protocol
        vnc_socket.connect((ip_addr, port))
        RFB_VERSION = vnc_socket.recv(12)
        rfb_version_string = RFB_VERSION.decode('UTF-8')
        if "RFB" not in rfb_version_string:
            print("Unable to capture screenshot")
            return
        
        vnc_socket.send(RFB_VERSION)
        auth_required = vnc_socket.recv(1)
        
        if not auth_required:
            print("Unable to capture screenshot")
            return

        # 0x01 received from server signifies that no authentication is required  
        if auth_required == b'\x01':
            filename = ip_addr.replace('.', '_') + '_scrot' + '.jpg'
            print(f"Saving VNC snapshot as {filename}")
            vnc_snapshot = f"timeout 10 vncsnapshot -allowblank -port {str(port)} {ip_addr}:0 {filename}" 
            print(vnc_snapshot) 

            # close authentication check socket and then run command. command must be run after or vncsnapshot will end prematurely
            vnc_socket.shutdown(socket.SHUT_WR)
            vnc_socket.close()
            
            os.system(vnc_snapshot)
            return filename
        

    except socket.error:
        vnc_socket.close()
        pass
    except socket.timeout:
        vnc_socket.close()
        pass
