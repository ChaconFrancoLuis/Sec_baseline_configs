from ncclient import manager
import xml.dom.minidom
import xmltodict


devices = [
    {
        "host":"192.168.32.135",
        "username":"cisco",
        "password":"cisco123!"
    },
    {
        "host":"192.168.32.134",
        "username":"cisco",
        "password":"cisco123!"
    },
]

netconf_data = """
<config>
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
 <interface>
 <Loopback>
 <name>112</name>
 <description>configuration multi equipo</description>
 <ip>
 <address>
 <primary>
 <address>11.11.11.11</address>
 <mask>255.255.255.0</mask>
 </primary>
 </address>
 </ip>
 </Loopback>
 </interface>
</native>
</config>
"""

for device in devices:
    m = manager.connect(
        host=device["host"],
        port=830,
        username=device["username"],
        password=device["password"],
        hostkey_verify=False
    )
    netconf_reply = m.edit_config(target="running", config=netconf_data)
    print(f"Configuracion aplicada en {device['host']}:")
    print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
