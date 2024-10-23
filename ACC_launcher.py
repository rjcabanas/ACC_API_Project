
import json
import subprocess

config_path = r'C:\Users\Michael\Documents\Assetto Corsa Competizione\Config\broadcasting.json'

config = {
    "udpListenerIp": "127.0.0.1",
    "updListenerPort": 9000,
    "connectionPassword": "",
    "commandPassword": "",
    "maxConnections": 5
}

with open(config_path, 'w') as f:
    json.dump(config, f, indent=4)

acc_path = r'C:\Program Files (x86)\Steam\steamapps\common\Assetto Corsa Competizione\acc.exe'

subprocess.Popen([acc_path])
