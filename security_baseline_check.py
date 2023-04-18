from netmiko import ConnectHandler
import re
from router_devices import devices_info

class SecurityCheck:
    def __init__(self,devices_info):
        self.devices = []
        for device_info in devices_info:
            try:
                connection = ConnectHandler(**device_info)
                connection.enable()
                self.devices.append({
                    'connection':connection,
                    'ip':device_info['ip'],
                    'hostname': self.get_hostname(connection),
                })
            except Exception as e:
                print(f"Error connection to device{device_info['ip']}:{e}")    
 
    def get_hostname(self,connection):
        return connection.send_command("show running-config | include hostname").split()[1]

    def is_password_encryption_enabled(self,connection):
        return 'service password-encryption' in connection.send_command("show running-config | include service password-encryption")

    def is_ssh_enable_and_telnet_disabled(self,connection):
        output = connection.send_command('show running-config | section line vty')
        return 'transport input ssh' in output and 'transport input telnet' not in output

    def is_source_routing_disable(self,connection):
        return 'no ip source-route' in connection.send_command('show running-config | include no ip source-route')

    def are_directed_broadcast_disable(self,connection):
        interfaces = re.findall(r'interface(\S+)',connection.send_command('show interfaces'))
        for interface in interfaces:
            output = connection.send_command(f'show running-config interface {interface}|include no ip directed-broadcast')
            if 'no ip directed-broadcast' not in output:
                return False
        return True

    def print_results(self):
        for device in self.devices:
            print(f"\n Device IP:{device['ip']}")
            print(f"Device Hostname:{device['hostname']}")
            connection = device['connection']
            print("Password Encryption is enabled." if self.is_password_encryption_enabled(connection) else "Password encryption is NOT ENABLED")
            print("SSH is enabled, and telnet is disabled" if self.is_ssh_enable_and_telnet_disabled(connection)else "SSH is not enabled, or telnet is disabled")
            print("IP Source Routing is disabled" if self.is_source_routing_disable(connection)else "IP source routing is NOT disabled.")
            print("IP Directed Broadcast are disable on all int" if self.are_directed_broadcast_disable(connection) else "IP direct Broadcast are not disabled on interfaces")

    def close_connections(self):
        for device in self.devices:
            device['connection'].disconnect()




def main():
    Security_check = SecurityCheck(devices_info)
    Security_check.print_results()
    Security_check.close_connections()


if __name__ == "__main__":
    main()