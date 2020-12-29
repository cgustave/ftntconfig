# -*- coding: utf-8 -*-
'''
Created on December 23, 2020
@author: cgustave
Fortinet device configuration library for SSH based configuration.
Main object to instanciate
'''
import logging as log
from Ftntconfig.Ftnt_ssh import Ftnt_ssh
from Ftntconfig.Ftntconfig_firewall import Firewall


class Ftntconfig(object):
    '''
	FortiGate configuration through SSH connection
    '''

    # create logger
    log.basicConfig(
        format='%(asctime)s,%(msecs)3.3d %(levelname)-8s[%(module)-7.7s.%(funcName)-30.30s:%(lineno)5d] %(message)s',
        datefmt='%Y%m%d:%H:%M:%S',
        filename='ftntconfig.log',
        level=log.NOTSET)
    log.debug('----------START-------------')

    def __init__(self,ip='', port=22, user='admin', password='', private_key='', private_key_file='', debug=False) :
        '''
        Constructor
        '''

        # Set debug level first
        if debug:
            self.debug = True
            log.basicConfig(level='DEBUG')

        log.info('Constructor with ip={} port={} user={} password={} private_key_file={} debug={}'.format(
            ip, port, user, password, private_key_file, debug))

        # attributs
        self.ssh              = Ftnt_ssh(ip=ip, port=port, user=user, password=password, private_key=private_key, private_key_file=private_key_file, debug=debug)
        self.firewall         = Firewall(self.ssh, debug=debug)

if __name__ == '__main__' :
    pass
