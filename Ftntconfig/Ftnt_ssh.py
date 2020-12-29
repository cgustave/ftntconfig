# -*- coding: utf-8 -*-
'''
Created on December 23, 2020
@author: cgustave
Fortinet device configuration library : ssh connection to Fortinet device
'''
import logging as log
import socket
import time
import paramiko

# Workaround for paramiko deprecation warnings (will be fixed later in paramiko)
import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

class Ftnt_ssh(object):
    '''
    SSH class for communication with fortigate
    '''

    # create logger
    log.basicConfig(
        format='%(asctime)s,%(msecs)3.3d %(levelname)-8s[%(module)-7.7s.%(funcName)-30.30s:%(lineno)5d] %(message)s',
        datefmt='%Y%m%d:%H:%M:%S',
        filename='ftntconfig.log',
        level=log.NOTSET)

    def __init__(self, ip='', port=22, user='admin', password='', private_key='', private_key_file='', debug=False) :
        '''
        Constructor
        '''

        # Set debug level first
        if debug:
            self.debug = True
            log.basicConfig(level='DEBUG')

        log.info('Constructor with ip={} port={} user={} password={} private_key_file={} debug={}'.format(
            ip, port, user, password, private_key_file, debug))

		# Public Attributes
        self.ip               = ip
        self.port             = port
        self.user             = user
        self.password         = password
        self.private_key_file = private_key_file
        self.timeout          = 3

        # Private attributs
        self.client           = ''
        self.connected        = False
        self.shell            = None


    def connect(self):
        '''
        '''
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        log.debug("Connecting with ip=%s port=%s user=%s password=%s private_key=%s" % (self.ip,self.port,self.user,self.password,self.private_key_file) )

        try:
            # use private key if not null
            if (self.private_key_file != ''):
                private_key = paramiko.RSAKey.from_private_key_file(self.private_key_file)
                log.debug ("got private key")
                self.client.connect(hostname=self.ip,
                                    port=self.port,
                                    username=self.user,
                                    pkey=private_key,
                                    timeout=self.timeout,
                                    allow_agent=False,
                                    look_for_keys=False)

            else:
                self.client.connect(hostname=self.ip, port=self.port,
                                    username=self.user, password=self.password,
                                    timeout=self.timeout,
                                    allow_agent=False,look_for_keys=False)

        except paramiko.AuthenticationException:
            print ("Authentication failed, please verify your credentials")
            result_flag = False
        except paramiko.SSHException as sshException:
            print ("Could not establish SSH connection: %s" % sshException)
            result_flag = False
        except socket.timeout as e:
            print ("Connection timed out")
            result_flag = False
        except Exception as e:
            print ("Exception in connecting to the server")
            print ("PYTHON SAYS:"+str(e))
            result_flag = False
            self.client.close()
        else:
            result_flag = True

        # Shell
        self.shell = self.client.invoke_shell()


        # update connected attribut
        self.connected = True
        return result_flag


    def send(self,command):

        if not self.connected:
            self.connect()

        if (self.shell):
            self.shell.send(command+"\n")
            while not self.shell.recv_ready():
                time.sleep(0.1)

            output=self.shell.recv(5000)
            print(output)

if __name__ == '__main__' :
    pass
