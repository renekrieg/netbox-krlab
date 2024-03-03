from pathlib import Path
import yaml

path_to_device_type = Path(Path(__file__).parents[1] / "templates" / "device-types")
items = list(path_to_device_type.rglob("*.yaml"))

for item in items:
  with open(item, 'r') as file:
    device = yaml.safe_load(file)
  device_type_list = []
  #print(device['slug'])
  device_type_data = {
    key: value for key, value in device.items() if key not in   ['console-ports', 'interfaces', 'rear-ports', 'front-ports',  'power-ports']
    }
  device_type_list.append(device_type_data)

  console_ports_list = []
  interfaces_list = []
  rear_ports_list = []
  front_ports_list = []
  power_ports_list = []
  
  for port in device.get('console-ports', []):
    console_ports_list.append({'device_type': device['slug'], **port})

  for port in device.get('interfaces', []):
    interfaces_list.append({'device_type': device['slug'], **port})

  for port in device.get('rear-ports', []):
    rear_ports_list.append({'device_type': device['slug'], **port})

  for port in device.get('front-ports', []):
    front_ports_list.append({'device_type': device['slug'], **port})

  for port in device.get('power-ports', []):
    power_ports_list.append({'device_type': device['slug'], **port})

  final_data = {
  	'device_type': device_type_list,
  	'console_ports': console_ports_list,
  	'interfaces': interfaces_list,
  	'rear_ports': rear_ports_list,
  	'front_ports': front_ports_list,
  	'power_ports': power_ports_list
  }
  
  yaml_object = yaml.dump(final_data, indent=2, sort_keys=False,allow_unicode=True)
  filename = final_data['device_type'][0]['model'] + '.yml'
  output_path = Path(Path(__file__).parents[1] / "ansible" / "devices" / "roles" / "create_device_types" / "files" / filename)
  with open(output_path, 'w+', encoding='utf-8') as file:
    file.write(yaml_object)