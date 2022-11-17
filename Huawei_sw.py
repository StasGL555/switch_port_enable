import telnetlib
import time
import getpass
import sys

#COMMAND = sys.argv[1].encode('utf-8')
#USER = input('Username: ').encode('utf-8')
#PASSWORD = getpass.getpass().encode('utf-8')
#ENABLE_PASS = getpass.getpass(prompt='Enter enable password: ').encode('utf-8')
USER = b'user'
PASSWORD = b'pass'
ENABLE_PASS = b'huawei'
#COMMAND = b'disp int brief'


IP = input('Device IP: ')
int_table = []
int_table_clear = []
d_interface = []
n_interface = []

print('Connection to device {}'.format(IP))
with telnetlib.Telnet(IP) as t:

    t.read_until(b'Username:')
    t.write(USER + b'\n')

    t.read_until(b'Password:')
    t.write(PASSWORD + b'\n')
    

    #t.read_until(b'Password:')
    #t.write(ENABLE_PASS + b'\n')
    t.write(b'screen-length 0 temporary \n')
    t.write(b'sys \n')
    t.write(b'disp int brief \n')

    time.sleep(5)

    output = t.read_until(b']')
    #output = t.read_very_eager().decode('utf-8')
    #print(output.decode('utf-8'))

    #output = t.read_until(b']')
    output = t.read_until(b'Interface')
    output = t.read_until(b']')
    #print('!!!!!!!!!!!!!!!!!')    
    #print(output.decode('utf-8'))

    int_table = (output.decode('utf-8')).split('\n')
    #print(int_table)

    avg_len = len(int_table[4].split())
    for i in int_table:
        if len(i.split()) == avg_len:
            if not 'lanif' in i:
                if not 'NULL' in i:
                    int_table_clear.append(i.split())
    print('!!!!!!!!!!!!!!!!!!!!!!!!')
    for i in int_table_clear:    
        print(i)
    print('\n')
    

    for i in int_table_clear:
        if '*down' in i:
            d_interface.append(i[0])
    print(d_interface, '\n')
    

    #d_interface = ['Ethernet0/0/2']
    if len(d_interface) != 0:
        print('Enable all disabled interfaces?')
        for i in d_interface:
            print(i)
        if input('y or n: ') == 'y':
            for i in d_interface:
                t.write(b'int ' + i.encode('utf-8') + b'\n')
                t.read_until(b']')
                t.write(b'undo sh \n')
                t.read_until(b']')
                t.write(b'quit \n')
                result = t.read_until(b']')
                

                print('int ' + i + ' enabled')
                #print(result.decode('utf-8'))
            
            time.sleep(5)

            for i in d_interface:
                t.write(b'disp int ' + i.encode('utf-8') + b'\n')
                result = t.read_until(b']')
                #if b'current state : DOWN' in result:
                if b'current state : UP' in result:
                    print(i, 'is now connected')
                else: n_interface.append(i)    

            if len(n_interface) !=0:
                print('Disable all notconnect interfaces?')
                for i in n_interface:
                    print(i)
                if input('y or n: ') == 'y':
                    for i in n_interface:
                        t.write(b'int ' + i.encode('utf-8') + b'\n')
                        t.read_until(b']')
                        t.write(b'sh \n')
                        result = t.read_until(b']')
                        print(i, 'is now disabled')
                else:
                    print('Interfaces not disabled')
                    for i in n_interface:
                        print(i) 


        else:
            print('\nint is still disabled')
            for i in d_interface:
                print(i) 
    else: print('\nno disabled interfaces found')