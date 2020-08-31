from netmiko import ConnectHandler
import os
import sys
import getpass
from mac_vendor_lookup import MacLookup

os.system('cls' if os.name == 'nt' else 'clear')

GREEN = "\033[1;32m"
sys.stdout.write(GREEN)

def nameLookup(mac):
    names = {
    '42:bf:71:29:4d:a4': 'X-A41VALMER',
    'e8:d0:fc:c9:1c:31': 'X-LENOVALME',
    'c6:ed:0e:97:75:25': 'X-ALEXS9',
    '44:8a:5b:ca:73:33': 'X-MYDESKMM',
    'c0:ee:fb:f5:d8:20': 'X-ONEPLUS',
    'f8:87:f1:c2:d5:a6': 'X-A_IPHONE',
    '3c:f0:11:05:08:1b': 'X-A_LAPWRK',
    '24:77:03:26:61:38': 'X-PWR_KUHN',
    '5c:ea:1d:0b:9e:8f': 'X-SONY SIT',
    '50:ec:50:1b:fa:13': 'X-FELIX',
    '04:f0:21:64:02:00': 'X-HIK_ATT',
    '00:17:10:90:df:a8': 'X-VM_BLA1',
    'e8:b1:fc:3a:b8:b7': 'X-TPX_LAP',
    '30:45:96:2b:80:f1': 'X-HW_WATCH'
    }

    if mac in names:
        return names[mac]
    else:
        return "NO NAME"

def data_analys(output, arpout):
    arpdict = {}
    for arp in arpout.splitlines():
        arpdict[arp] = 'NO RECORDED HOSTNAME'
    dhcpdict = {}
    for dhcplease in output.splitlines():
        dhcpdict[dhcplease.split(' ')[1]] = dhcplease.split(' ')[3]

    fullist = {**arpdict, **dhcpdict}
    print('--- %d clients detected' % (len(fullist)))

    for key, line in fullist.items():
        mac = key
        vendor = 'VENDOR NOT FOUND'
        try:
            vendor = MacLookup().lookup(mac)
        except:
            pass
            #print('Could not parse MAC %s' % (mac))
        name = nameLookup(mac)
        if name != 'NO NAME':
            hostname = name
        else:
            hostname = '!!!-'+line
        print('CLIENT: %s [%s]' % (hostname, vendor))


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
    arpout = login.send_command_expect("arp -a | awk 'NR>1{print $4}'")
    login.disconnect()

    data_analys(output, arpout)


wrt_pass = getpass.getpass('Enter password: ')

connect('root', wrt_pass, 'linux', '172.17.17.1', '2222')
