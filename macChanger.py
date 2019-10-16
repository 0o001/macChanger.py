import argparse
import os
import random
import re

__author__ = 'mustafauzun0'

'''
MACCHANGER
'''

def getMacAddress(interface):
        command = os.popen('ifconfig ' + interface + ' | grep -o -E "([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}"')
        macaddress = command.read().strip()

        if macaddress:
                return macaddress

def setMacAddress(interface, macadress):
        os.popen('ifconfig ' + interface + ' down')
        os.popen('ifconfig ' + interface + ' hw ether ' + macadress)
        os.popen('ifconfig ' + interface + ' up')

def resetMacAddress(interface):
        command = os.popen('ethtool -P ' + interface + ' | grep -o -E "([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}"')
        macaddress = command.read().strip()
        setMacAddress(interface, macaddress)

def checkMacAddress(interface, macaddress):
        return getMacAddress(interface) == macaddress

def randomMacAddress():
        return ':'.join(('%02x' % random.randint(0x00, 0x7f)) for _ in range(6))

def validateMacAddress(macaddress):
        return re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macaddress.lower())

def main():
        parser = argparse.ArgumentParser(description='Mac Changer')

        parser.add_argument('-i', '--interface', dest='interface', help='Target Interface', required=True)
        parser.add_argument('-m', '--macaddress', dest='macaddress', help='Mac Address')
        parser.add_argument('-rm', '--random', dest='random', action='store_true', help='Random Mac Address')
        parser.add_argument('-r', '--reset', dest='reset', action='store_true', help='Reset Mac Address')

        args = parser.parse_args()

        if args.random:
                args.macaddress = randomMacAddress()

        if args.macaddress:
                if validateMacAddress(args.macaddress):
                        setMacAddress(args.interface, args.macaddress)
                        
                        if checkMacAddress(args.interface, args.macaddress):
                                print('[+] Changed', args.interface, 'Mac Address to', args.macaddress)
                        else:
                                print('[-] Not Changed', args.interface, 'Mac Address')
                else:
                        print('[-] Mac Address not Validate')
                

        if args.reset:
                resetMacAddress(args.interface)
                print('[+] Reset', args.interface, 'Mac Address')
if __name__ == '__main__':
        main()
