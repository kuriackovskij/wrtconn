from netmiko import ConnectHandler
import os
import sys
import getpass
from mac_vendor_lookup import MacLookup

os.system('cls' if os.name == 'nt' else 'clear')

GREEN = "\033[1;32m"
sys.stdout.write(GREEN)

def data_analys(output):
    vendor=''
    print('--- %d clients detected' % (len(output.splitlines())))
    for line in output.splitlines():
        mac = line.split(' ')[1]
        try:
            vendor = MacLookup().lookup(mac)
        except:
            print('Could not parse MAC %s' % (mac))
        hostname = line.split(' ')[3]
        print('CLIENT: %s [%s]' % (vendor, hostname))

def connect(username, password, type, ipaddress, port):
    params = {
        'username': username,
        'password': password,
        'device_type': type,
        'ip': ipaddress,
        'port': port}

    login = ConnectHandler(**params)
    login.enable()
    output = login.send_command_expect('cat /tmp/dhcp.leases')
    login.disconnect()

    data_analys(output)


wrt_pass = getpass.getpass('Enter password: ')

connect('root', wrt_pass, 'linux', '172.17.17.1', '2222')
