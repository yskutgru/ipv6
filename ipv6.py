#!/usr/bin/env python3
import subprocess
import re
import datetime
from oracle_rest import send_to

service_url = "https://mis.gte.local/ords/mis/inv/ip6"
vlan_native = 4
cmd = [
    'sudo', 'tcpdump', '-enli', 'any', 'ip6'
    # ,'host', '10.40.101.236'
    # ,
    # '2>/dev/null'
    # 'host', '10.250.3.4',
    # 'and', 'dst', 'port', '25',
    # '-l'  # For line-by-line output
]


def parse_command(line):
    """Parse a tcpdump output line and extract timestamp, src MAC and VLAN."""
    timestamp_pattern = r'(\d+:\d+:\d+\.\d+)'
    mac_pattern = r'([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})'
    vlan_pattern = r'vlan\s+(\d+)'
    try:
        timestamp_match = re.search(timestamp_pattern, line)
        timestamp = timestamp_match.group(1) if timestamp_match else datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        mac_address = re.findall(mac_pattern, line)
        src_mac = mac_address[0].replace(':', '').lower() if len(mac_address) > 0 else "N/A"
        vlan_match = re.search(vlan_pattern, line)
        vlan_id = vlan_match.group(1) if vlan_match else vlan_native
        return {
            'timestamp': timestamp,
            'src_mac': src_mac,
            'vlan_id': vlan_id
        }
    except Exception:
        return {
            'timestamp': datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3],
            'src_mac': "N/A",
            'vlan_id': "N/A"
        }


def main():
    print(cmd)
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)

        print("Start")
        print("=" * 60)

        for line in process.stdout:
            data = parse_command(line)
            json_data = [data]
            print("json_data:", json_data)

            # Send json
            result = send_to(
                data=json_data,
                url=service_url,
                timeout=15
            )

    except KeyboardInterrupt:
        print("\nStopped by user")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'process' in locals():
            process.terminate()


if __name__ == '__main__':
    main()
