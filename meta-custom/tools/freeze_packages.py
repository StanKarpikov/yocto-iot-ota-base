import re
import os
import sys

packages_required = os.popen(f'bitbake -g core-image-minimal && cat pn-buildlist | grep -ve "native" | sort | uniq').read()
packages = os.popen(f'bitbake -s').read()

lines = [line for line in packages.splitlines() if ':' in line]

for line in lines:
    # print(line)
    match = re.match(r"^(\S+)\s+(\d*:)?(\S+)-r\d+", line)
    if match:
        package, epoch, version = match.group(1), match.group(2), match.group(3)
        
        epoch = epoch[:-1] if epoch else ""
        full_version = f"{epoch}:{version}" if epoch else version
        
        if package in packages_required:
            print(f'PREFERRED_VERSION_{package} = "{full_version}"')
    else:
        # print(f"Unknown line {line}", file=sys.stderr)
        pass

print("\n")