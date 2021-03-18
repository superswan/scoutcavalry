
def run(filename, ip_addr, ports, packet_rate):
    command = f'masscan {ip_addr} -p {ports} --rate {packet_rate} -oX {filename}'
    print(command)