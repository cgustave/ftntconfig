# Ftntconfig

##### Disclaimer :
This is not a Fortinet official product. It is provided as-is without official support.  
I have made this tool for my own use. It can be used at your own risk.  

##### Author :
Cedric GUSTAVE

#### Description :
Ftntconfig is a simple python library to automate Fortinet device configuration. 
It has been created for lab testing scenario where Fortinet devices requires configuration loops.
All configuration is done through an SSH connection.
It is an evolutive framework where each new configuration requirement can be added in an organized framework. 
Each device configuration section is accessed through a corresponding attribut:
Example to access 'config firewall policy' section:
~~~
from Ftntconfig import Ftntconfig
fgt = Ftntconfig(ip='10.5.51.200', port='22', user='admin', password='', debug=True)
fgt.firewall.policy()
~~~

For more details on the configuration syntax, refer to corresponding module:

Ftntconfig_firewall.py : `config firewall`

