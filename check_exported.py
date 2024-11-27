import xml.etree.ElementTree as ET
import sys
import difflib

def check_exported_components(manifest_path):
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    package = root.attrib.get('package')  # Get the package name
    namespace = '{http://schemas.android.com/apk/res/android}'  # XML namespace for Android attributes
    base_file = '.security/baseline.txt'
    scan_file = 'scan.txt'
    
    # Ensure the scan file exists
    open(scan_file, 'a').close()

    def is_exported(component):
        exported = component.get(namespace + 'exported')
        # Explicitly marked as not exported
        if exported == 'false':
            return False
        # Has an intent-filter -> implicitly exported
        if component.find('intent-filter') is not None:
            return True
        # Default case: no explicit 'exported' attribute -> assume not exported
        return exported == 'true' or exported is None

    # Check and log exported components
    def log_component(component_type, component):
        name = component.get(namespace + 'name')
        if name.startswith('.'):
            name = package + name  # Prefix package name for relative component names
        print(f"Exported {component_type}: {name}")
        with open(scan_file, 'a+') as file:
            file.write(f"Exported {component_type}: {name}\r\n")

    # Iterate through component types
    for component_type, tag in [
        ('Activity', 'activity'),
        ('Service', 'service'),
        ('BroadcastReceiver', 'receiver'),
        ('ContentProvider', 'provider')
    ]:
        for component in root.findall(f"application/{tag}"):
            if is_exported(component):
                log_component(component_type, component)

    print("\r\n\r\n")
    baseline(base_file, scan_file)

def baseline(base_file, scan_file):
    # Read the contents of the two files
    with open(scan_file, 'r') as file1, open(base_file, 'r') as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()

    for line1 in file1_lines:
        if line1 not in file2_lines:
            print("\r\n")
            print(f"\033[91mNew component added:\r\n{line1}\033[0m")

if len(sys.argv) == 2:
    manifest_path = sys.argv[1]
    check_exported_components(manifest_path)
else:
    print("Usage: python check_exported.py AndroidManifest.xml")

