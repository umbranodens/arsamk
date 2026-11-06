#!/usr/bin/env python3
"""Snapshot existing workloads without reading environment values or credentials."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

STACK = Path('/opt/stacks/arsamk')
BASELINE = STACK / 'existing-baseline.json'


def snapshot():
    ids = subprocess.check_output(['docker', 'ps', '-aq']).decode().split()
    containers = json.loads(subprocess.check_output(['docker', 'inspect', *ids])) if ids else []
    workloads = {c['Name']: {'id': c['Id'], 'started': c['State']['StartedAt'],
                             'running': c['State']['Running'],
                             'restarts': c['RestartCount']}
                 for c in containers if not c['Name'].startswith('/arsamk-')}
    paths = []
    for stack in Path('/opt/stacks').iterdir():
        if stack.name != 'arsamk':
            paths.extend(stack.glob('compose.y*ml'))
            paths.extend(stack.glob('*deploy.sh'))
    paths.extend(Path('/opt/wr/compose').glob('*.yml'))
    paths.append(Path('/etc/cloudflared/config.yml'))
    hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    return {'containers': workloads, 'configuration_sha256': hashes}


if __name__ == '__main__':
    state = snapshot()
    if sys.argv[1:] == ['record']:
        with BASELINE.open('x') as output:
            json.dump(state, output, indent=2)
        print(f'Recorded {len(state["containers"])} existing containers and '
              f'{len(state["configuration_sha256"])} configuration hashes')
    else:
        previous = json.loads(BASELINE.read_text())
        if previous != state:
            print(json.dumps({'before': previous, 'after': state}, indent=2))
            raise SystemExit('Existing workload baseline changed')
        print(f'PASS: all {len(state["containers"])} existing containers retain their IDs, '
              'start times, restart counts and running state; all configuration hashes match')
