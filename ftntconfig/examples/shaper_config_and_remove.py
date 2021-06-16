# -*- coding: utf-8 -*-
from ftntconfig.ftntconfig import Ftntconfig
fgt = Ftntconfig(ip='10.5.51.200', port='22', user='admin', password='', debug=True)



def shapers(start=0, action='create'):
    """
    Create/delete 1000 shapers starting from start
    """

    i = 1
    while i+start <= 1000+start:
        name = "DUMMY-SHAPE-"+str(i)
        if action == 'create':
            print ("create name={}".format(name))
            fgt.firewall.shaper(action='create', type='shared', name=name, maximum_bandwidth='1000000', per_policy='enable')
            i = i + 1
        elif action == 'delete':
            print ("delete name={}".format(name))
            fgt.firewall.shaper(action='delete', type='shared', name=name)


shapers(start=0,action="create")
shapers(start=0,action="delete")



    
