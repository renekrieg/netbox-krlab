from pathlib import Path
import yaml
import numpy as np

def flatten(xss):
    return [x for xs in xss for x in xs]
  
class IndentDumper(yaml.Dumper):
# https://reorx.com/blog/python-yaml-tips/
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


path_to_device_type = Path(Path(__file__).parents[1] / "ansible" / "devices" / "roles" / "create_device_types" / "files")
items = list(path_to_device_type.rglob("*.yml"))


device_type_list = []
console_ports_list = []
interfaces_list = []
rear_ports_list = []
front_ports_list = []
power_ports_list = []
for item in items:
  with open(item, 'r') as file:
    device = (yaml.safe_load(file))
    device_type_list.append(device['device_type'])
    if device['console_ports']:
      console_ports_list.append(device['console_ports'])
    if device['interfaces']:
      interfaces_list.append(device['interfaces'])
    if device['rear_ports']:
      rear_ports_list.append(device['rear_ports'])
    if device['front_ports']:
      front_ports_list.append(device['front_ports'])
    if device['power_ports']:
      power_ports_list.append(device['power_ports'])

final_data = {
	'device_types': flatten(device_type_list),
	'console_ports': flatten(console_ports_list),
	'interfaces': flatten(interfaces_list),
	'rear_ports': flatten(rear_ports_list),
	'front_ports': flatten(front_ports_list),
	'power_ports': flatten(power_ports_list)
}

output_path = Path(Path(__file__).parents[1] / "ansible" / "devices" / "roles" / "create_device_types" / "vars" / "main.yml")

yaml_object = yaml.dump(final_data, indent=2, Dumper=IndentDumper, sort_keys=False,allow_unicode=True)

with open(output_path, 'w+', encoding='utf-8') as file:
  file.write(yaml_object)