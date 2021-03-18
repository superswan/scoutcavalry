import os


def run(filename, ip_addr, ports, packet_rate):
    command = f'sudo masscan {ip_addr} -p {ports} --rate {packet_rate} -oX {filename}'
    #setuid bit in order to run masscan as root
    print(f'Executing command: \n{command}')
    os.system(command)