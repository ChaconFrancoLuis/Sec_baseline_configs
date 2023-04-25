from ncclient import manager
import xml.dom.minidom
import xmltodict


m = manager.connect(
    host="192.168.32.135",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

netconf_filter = """
<filter>
 <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
"""

netconf_reply = m.get(filter = netconf_filter)
netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

#print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

for interface in netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]:
    print("name: {} MAC: {} Input: {} output {}".format(
        interface["name"],
        interface["phys-address"],
        interface["statistics"]["in-octets"],
        interface["statistics"]["out-octets"]
    ))