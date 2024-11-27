import xml.etree.ElementTree as ET
import sys
import difflib

def check_exported_components(manifest_path):
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    package = root.attrib.get('package')
    namespace = '{http://schemas.android.com/apk/res/android}'
    base_file = 'baseline.txt'
    scan_file = 'scan.txt'
    open(x, scan_file).close()

    
    def is_exported(component):
        exported = component.get(namespace + 'exported')
        # Check if component is explicitly not exported
        if exported == 'false':
            return False
        # If component has intent-filter, it is considered exported
        if component.find('intent-filter') is not None:
            return True
        
        # Default case: if 'exported' is not set, assume false
        return exported is None or exported == 'true'

    #print("Checking for exported components...")
    
    # Check Activities
    for activity in root.findall("application/activity"):
        if is_exported(activity):
            if package in activity.get(namespace+'name'):
                print(f"Exported Activity: {activity.get(namespace+'name')}")
                with open(scan_file, 'a+') as file:
                    file.write("Exported Activity: {}\r\n".format(activity.get(namespace+'name')))
    
    # Check Services
    for service in root.findall("application/service"):
        if is_exported(service):
            if package in service.get(namespace+'name'):
                print(f"Exported Service: {service.get(namespace+'name')}")
                with open(scan_file, 'a+') as file:
                    file.write("Exported Service: {}\r\n".format(service.get(namespace+'name')))
    
    # Check BroadcastReceivers
    for receiver in root.findall("application/receiver"):
        if is_exported(receiver):
            if package in receiver.get(namespace+'name'):
                print(f"Exported BroadcastReceiver: {receiver.get(namespace+'name')}")
                with open(scan_file, 'a+') as file:
                    file.write("Exported BroadcastReceiver: {}\r\n".format(receiver.get(namespace+'name')))
    
    # Check ContentProviders
    for provider in root.findall("application/provider"):
        if is_exported(provider):
            if package in provider.get(namespace+'name'):
                print(f"Exported ContentProvider: {provider.get(namespace+'name')}")
                with open(scan_file, 'a+') as file:
                    file.write("Exported ContentProvider: {}\r\n".format(provider.get(namespace+'name')))
    print("\r\n\r\n")
    baseline(base_file, scan_file) 


def baseline(base_file, scan_file):
        # Read the contents of the two files
        with open(scan_file, 'r') as file1, open(base_file, 'r') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

        for line1 in file1_lines:
            if not line1 in file2_lines:
                 print("\r\n")
                 print("\033[91mNew component Added:\r\n{}\033[0m".format(line1))

if len(sys.argv) == 2:
    manifest_path = sys.argv[1]
    check_exported_components(manifest_path)
    
else:
    print("Usage check_exported.py + AndroidManifest.xml")
