from ncclient import manager


m = manager.connect(
    host="192.168.32.135",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)


for capability in m.server_capabilities:
    print(capability)
   # if "Cisco-IOS-XE-cdp" in capability:
    #    print(capability)