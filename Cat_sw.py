import sys
import time

#from netmiko import NetMikoAuthenticationException, NetMikoTimeoutException
from netmiko import ConnectHandler

USER = user
PASSWORD = password
#PASSWORD = getpass.getpass()
ENABLE_PASS = en_password
while True:
    COMMANDS = []
    res = []    
    d_interface = []
    n_interface = []
    IP = input('Device IP: ')
    #IP = '192.168.100.253'
    print('Connection to device {}'.format(IP))
    DEVICE_PARAMS = {'device_type': 'cisco_ios_telnet',
                         'ip': IP,
                         'username':USER,
                         'password':PASSWORD,
                         'secret':ENABLE_PASS,
                         'verbose': False,
                         'global_delay_factor': 0.1}
    try:
        with ConnectHandler(**DEVICE_PARAMS) as telnet:
            print('Successful connection to device')
            telnet.enable()
            result = telnet.send_command('sh int status')
            print(result)
            #print(type(result))
            res_form = result.split('\n')
            #print(res_form)
            for i in res_form:
                res.append(i.split())
                #print(i)
            #print(res)
            for i in res:
                if len(i) != 0:
                    if 'disabled' in i:
                        d_interface.append(i[0])
            #for i in d_interface:
            #    print(i)

            if len(d_interface) != 0:
                print('Enable all disabled interfaces?')
                for i in d_interface:
                    print(i)
                if input('y or n: ') == 'y':
                    for i in d_interface:
                        COMMANDS.append('int ' + i)
                        COMMANDS.append('no sh')
                        #telnet.send_config_set(['int ' + i, 'no sh'])
                        print(i, 'is now enabled')
                    print('start')
                    start_time = time.time()
                    telnet.send_config_set(COMMANDS)        
                    print('stop')
                    print('Enabling of ' + str(len(d_interface)) + ' interfaces take', round(time.time() - start_time, 1), 'seconds')
                    print('Wait 5 sec, for interfaces will may connect')
                    time.sleep(5)

                    print('Searching for connected interfaces')
                    #COMMANDS.clear()
                    for i in d_interface:
                        result = telnet.send_command('sh int ' + i + ' status')
                        #print(result)
                        #if 'notconnect'.count('connected'):   
                        if result.count('connected'):
                            print(i, 'is now connected')
                        else: n_interface.append(i)    
                    if len(d_interface) == len(n_interface):
                        print('No connected interface found')
                    

                    COMMANDS.clear()
                    if len(n_interface) !=0:
                        print('Disable all notconnect interfaces?')
                        for i in n_interface:
                            print(i)
                        if input('y or n: ') == 'y':
                            for i in n_interface:
                                COMMANDS.append('int ' + i)
                                COMMANDS.append('sh')
                                #telnet.send_config_set(['int ' + i, 'sh'])
                                print(i, 'is now disabled')
                            print('start')
                            start_time = time.time()
                            telnet.send_config_set(COMMANDS)        
                            print('stop')
                            #print('Disabling of ' + str(len(n_interface)) + ' interfaces take', "--- %s seconds ---" % (round(time.time() - start_time), 1))
                            print('Disabling of ' + str(len(n_interface)) + ' interfaces take', round(time.time() - start_time, 1), 'seconds')
                        else:
                            print('Interfaces not disabled')
                            for i in n_interface:
                                print(i)


                else:
                    print('int is still disabled')
                    for i in d_interface:
                        print(i)
            else: print('no disabled interfaces found')
    except Exception as e:
        print('Error occur while connect to device')
        print(e) 
    if input('Another device? Yes(y) or No(n): ') == 'y':
        continue
    else:
        break