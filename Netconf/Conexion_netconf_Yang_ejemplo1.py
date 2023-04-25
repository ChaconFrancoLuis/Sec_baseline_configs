from ncclient import manager
import xml.etree.ElementTree as ET 

router = {"host":"192.168.32.135",
          "port":830,
          "username":"cisco",
          "password":"cisco123!"}

with manager.connect(host=router['host'],
     port=router['port'],
     username=router['username'],
     password=router['password'],
     hostkey_verify=False) as m:
     ip_schema = m.get_schema('Cisco-IOS-XE-cdp')
     root=ET.fromstring(ip_schema.xml)
     yang_tree = list(root)[0].text
     f = open('Cisco-IOS-XE-cdp.yang','w')
     f.write(yang_tree)
     f.close()
