# -*- coding: utf-8 -*-
'''
Created on December 23, 2020
@author: cgustave
Fortinet device configuration library : config firewall
'''
import logging as log
from Ftntconfig.Ftnt_ssh import Ftnt_ssh

class Firewall(object):
    '''
    Config firewall configuration
    '''
    def __init__(self, ssh, debug=False):
        log.basicConfig(
            format='%(asctime)s,%(msecs)3.3d %(levelname)-8s[%(module)-7.7s.%(funcName)-30.30s:%(lineno)5d] %(message)s',
            datefmt='%Y%m%d:%H:%M:%S',
            filename='ftntconfig.log',
            level=log.NOTSET)

        if debug:
            self.debug = True
            log.basicConfig(level='DEBUG')

        log.info('Constructor with debug={}'.format(debug))
        self.ssh = ssh

    def shaper(self, action='update', type='shared', name='', maximum_bandwidth='0', per_policy='disable'):
        '''
        Create, update or delete firewall shapers.
        Use action=update for both create and update
        Shapers could be either 'traffic-shaper' or 'per-ip-shaper'
        Supported configuration statements
            set maximum-bandwidth _maximum_bandwidth_
            set per-policy _enable|disable_
        '''
        log.info('* Enter with action={} type={} name={}'.format(action, type, name))

        # Sanity checks
        if name == '':
            log.error('shaper name is required')
            exit(0)

        if type == 'shared':
            self.ssh.send("config firewall shaper traffic-shaper")
        elif type == 'per-ip':
            self.ssh.send("config firewall shaper per-ip-shaper")
        else:
            log.error("unknown type")
            exit

        if action == 'delete':
            log.debug('delete shaper name={}'.format(name))
            self.ssh.send("delete "+name)
        elif action in ['create', 'update']:
            log.debug('create/update shaper name={}'.format(name))
            self.ssh.send("edit "+name)
            self.ssh.send("set maximum-bandwidth "+maximum_bandwidth)
            self.ssh.send("set per-policy "+per_policy)
            self.ssh.send("next")
        else:
            log.error("unknown action")
            exit

        self.ssh.send("end")

    def policy(self, action='update', id='0', traffic_shaper='', traffic_shaper_reverse='' ):
        '''
        Create, update or delete firewall policies
        Use 'unset' value to unset a config
        Supported configuration statements:
            set traffic-shaper _traffic_shaper'
            set traffic-shaper-reverse _traffic_shaper_reverse_
        '''
        log.info('* Enter with action={} traffic_shaper={} traffic-shaper-reverse={}'.format(action, traffic_shaper, traffic_shaper_reverse))

        if action == 'delete':
            log.debug('delete policy id={}'.format(id))
        elif action not in ['create', 'update', 'delete']:
            log.error('unknow action={}'.format(action))
            exit(0)

        log.debug('create/update policy id={}'.format(id))
        self.ssh.send("config firewall policy")
        self.ssh.send("edit "+id)

        if traffic_shaper == 'unset':
            log.debug('unset traffic_shaper')
            self.ssh.send('unset traffic-shaper')
        elif traffic_shaper != '':
            log.debug('set traffic-shaper {}'.format(traffic_shaper))
            self.ssh.send('set traffic-shaper '+traffic_shaper)

        if traffic_shaper_reverse == 'unset':
            log.debug('unset traffic_shaper_reverse')
            self.ssh.send('unset traffic-shaper-reverse')
        elif traffic_shaper_reverse != '':
            log.debug('set traffic-shaper-reverse {}'.format(traffic_shaper_reverse))
            self.ssh.send('set traffic-shaper-reverse '+traffic_shaper_reverse)

        self.ssh.send("next")
        self.ssh.send("end")
