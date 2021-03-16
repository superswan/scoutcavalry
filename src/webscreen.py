# Takes screen shot of webpage and saves to file
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import ipaddress
import time

from bcolors import bcolors

# Web driver configuraton, headless mode to prevent window popup, disable-gpu
# for performance
chrome_options=Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--ignore-certificate-errors")

# driver must be created in function or it will give an error due to
# the way selenium handles sessions

def getWebScreen(url):
    url_parsed = urlparse(url)
    net_loc = url_parsed.netloc
    filename = None
    print(url_parsed)
    print(net_loc)
    try:
        if ipaddress.ip_address(net_loc.split(":")[0]):
            net_loc = str(url_parsed.netloc.split(":")[0])
            port_num = str(url_parsed.netloc.split(":")[1])
            ip_stripped = net_loc.replace('.','-')
            filename = f"{ip_stripped}_{port_num}_scrot.png"
    
    except:
        print(f"{bcolors.WARNING}[!] Using hostname instead of IP{bcolors.ENDC}")
        pass

    if filename is None:
        filename = url_parsed.netloc.replace('.', '_')+'_scrot.png' # change to timestamp in future 
   
    print(url)
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(800,600)
    try:
        driver.get(url)
        print(f"{bcolors.OKGREEN}[*] Saving screenshot as: {filename}{bcolors.ENDC}")
        screenshot = driver.save_screenshot(filename)
    except:
        print(f"{bcolors.WARNING}[!] Screenshot Unavailable{bcolors.ENDC}")
        pass

    driver.quit()
    return filename

