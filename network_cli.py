from netmiko import ConnectHandler

cisco_881 = {
    'device_type': 'cisco_ios',
    'host':   '192.168.32.135',
    'username': 'cisco',
    'password': 'cisco123!',
    'port' : 22,          
}

net_connect = ConnectHandler(**cisco_881)

config_commands = ['interface loopback 112']


output = net_connect.send_config_set(config_commands)

output = net_connect.send_command('show ip int brief')
print(output)