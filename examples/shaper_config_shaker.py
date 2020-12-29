# -*- coding: utf-8 -*-
'''
Created on December 23, 2020
@author: cgustave

Configuration loop for traffic shaping

config firewall shaper traffic-shaper
    edit "SHAPE-WAN-SUPPORT"
        set maximum-bandwidth 1024000
        set per-policy enable
    next
end

To be applied to policies 605, 606, 190, 370, 372, 529

'''
import logging as log
import time
from Ftntconfig import Ftntconfig

# Create Ftnt config object
fgt = Ftntconfig(ip='10.5.51.200', port='22', user='admin', password='', debug=True)

# Create / Delete shaper
# my test shaper
fgt.firewall.shaper(action='create', type='shared', name='CGU-TEST-SHAPER', maximum_bandwidth='1000000', per_policy='enable')


while True:

    # Create other unused Shapers
    for shp in ['CGU-UNUSED-1', 'CGU-UNUSED-2', 'CGU-UNUSED-3' ]:
        fgt.firewall.shaper(action='create', type='shared', name=shp, maximum_bandwidth='1000000', per_policy='enable')

    # Apply shaper to policies
    fgt.firewall.policy(action='update', id='605', traffic_shaper='CGU-UNUSED-1', traffic_shaper_reverse='CGU-TEST-SHAPER')
    fgt.firewall.policy(action='update', id='606', traffic_shaper='CGU-UNUSED-2', traffic_shaper_reverse='CGU-TEST-SHAPER')
    # my test traffic policy below
    #fgt.firewall.policy(action='update', id='529', traffic_shaper='CGU-TEST-SHAPER', traffic_shaper_reverse='CGU-TEST-SHAPER')

    #fgt.firewall.policy(action='update', id='190', traffic_shaper='CGU-TEST-SHAPER', traffic_shaper_reverse='CGU-TEST-SHAPER')
    fgt.firewall.policy(action='update', id='370', traffic_shaper='CGU-UNUSED-3', traffic_shaper_reverse='CGU-TEST-SHAPER')
    #fgt.firewall.policy(action='update', id='372', traffic_shaper='CGU-TEST-SHAPER', traffic_shaper_reverse='CGU-TEST-SHAPER')

    # my test traffic policy below
    #fgt.firewall.policy(action='update', id='190', traffic_shaper='unset', traffic_shaper_reverse='unset')
    #fgt.firewall.policy(action='update', id='372', traffic_shaper='unset', traffic_shaper_reverse='unset')

    # Update test shapers
    #fgt.firewall.shaper(action='update', type='shared', name='CGU-TEST-SHAPER', maximum_bandwidth='9999', per_policy='disable')
    #fgt.firewall.shaper(action='update', type='shared', name='CGU-TEST-SHAPER', maximum_bandwidth='9998', per_policy='enable')
    #fgt.firewall.shaper(action='update', type='shared', name='CGU-TEST-SHAPER', maximum_bandwidth='9997')
    #fgt.firewall.shaper(action='update', type='shared', name='CGU-TEST-SHAPER', maximum_bandwidth='9996', per_policy='disable')
    #fgt.firewall.shaper(action='update', type='shared', name='CGU-TEST-SHAPER', maximum_bandwidth='9995', per_policy='enable')

    # Delete unused Shapers
    fgt.firewall.policy(action='update', id='605', traffic_shaper='unset', traffic_shaper_reverse='unset')
    fgt.firewall.policy(action='update', id='606', traffic_shaper='unset', traffic_shaper_reverse='unset')
    fgt.firewall.policy(action='update', id='370', traffic_shaper='unset', traffic_shaper_reverse='unset')


    for shp in ['CGU-UNUSED-3', 'CGU-UNUSED-1', 'CGU-UNUSED-3' ]:
        fgt.firewall.shaper(action='delete', type='shared', name=shp)

    # Delete other unused Shapers
    for shp in ['CGU-UNUSED-1', 'CGU-UNUSED-2', 'CGU-UNUSED-3' ]:
        fgt.firewall.shaper(action='delete', type='shared', name=shp)
