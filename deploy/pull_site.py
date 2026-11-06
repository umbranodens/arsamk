#!/usr/bin/env python3
"""Pull static production data; never run code from the deployment branch."""
import argparse
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_site import MAX_BYTES, public_path, validate

REPOSITORY = 'https://github.com/umbranodens/arsamk.git'


def extract(data, destination):
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:') as archive:
        members = archive.getmembers()
        if sum(item.size for item in members) > MAX_BYTES or len(members) > 2000:
            raise ValueError('archive exceeds limits')
        names = set()
        for item in members:
            if item.isdir() and item.name == 'assets':
                continue
            if item.isdir() and item.name.startswith('assets/') and all(
                    not part.startswith('.') for part in Path(item.name).parts):
                continue
            if not item.isfile() or not public_path(item.name) or item.name in names:
                raise ValueError(f'unsafe archive member: {item.name}')
            names.add(item.name)
        for item in members:
            if not item.isfile():
                continue
            target = destination / item.name
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.extractfile(item) as source, target.open('wb') as output:
                shutil.copyfileobj(source, output)
            target.chmod(0o644)


def point(root, name, target):
    temporary = root / (name + '.next')
    temporary.unlink(missing_ok=True)
    temporary.symlink_to(target)
    os.replace(temporary, root / name)


def activate(root, release, health_check):
    current = root / 'current'
    previous = current.readlink() if current.is_symlink() else None
    point(root, 'current', 'releases/' + release)
    try:
        health_check()
    except Exception:
        if previous:
            point(root, 'current', previous)
        else:
            current.unlink()
        raise
    if previous and previous != Path('releases/' + release):
        point(root, 'previous', previous)


def git(repository, *args):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
    return subprocess.check_output(['git', '-C', str(repository), *args],
                                   env=env, timeout=60)


def verify_release(root):
    validate(root)
    manifest = json.loads((root / 'release.json').read_text())
    if not re.fullmatch('[0-9a-f]{40}', manifest['revision']):
        raise ValueError('invalid source revision')
    actual = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in root.rglob('*') if p.is_file() and p.name != 'release.json'}
    if manifest['files'] != actual:
        raise ValueError('release checksums do not match')
    return manifest['revision']


def check_http(url, revision):
    for attempt in range(5):
        try:
            with urlopen(url, timeout=5) as response:
                if json.load(response)['revision'] == revision:
                    return
        except (OSError, ValueError):
            pass
        time.sleep(1)
    raise RuntimeError('HTTP release verification failed')


def stage_release(root, release, archive):
    if not re.fullmatch('[0-9a-f]{40}', release):
        raise ValueError('invalid deployment revision')
    releases = root / 'releases'
    releases.mkdir(exist_ok=True)
    destination = releases / release
    with tempfile.TemporaryDirectory(prefix='candidate-', dir=root) as tmp:
        candidate = Path(tmp)
        extract(archive, candidate)
        revision = verify_release(candidate)
        if destination.is_symlink():
            destination.unlink()
        if destination.exists():
            try:
                if verify_release(destination) != revision:
                    raise ValueError('existing release has a different revision')
            except (OSError, ValueError, KeyError, TypeError):
                if destination.is_dir():
                    shutil.rmtree(destination)
                else:
                    destination.unlink()
            else:
                destination.chmod(0o755)
                return revision
        candidate.chmod(0o755)
        os.replace(candidate, destination)
    return revision


def sync(root, health_url):
    repository = root / 'repository.git'
    if not repository.exists():
        subprocess.run(['git', 'init', '--bare', str(repository)], check=True, capture_output=True)
    remote = git(repository, 'ls-remote', '--exit-code', REPOSITORY, 'refs/heads/production')
    release = remote.decode().split()[0]
    if not re.fullmatch('[0-9a-f]{40}', release):
        raise ValueError('invalid deployment revision')
    current = root / 'current'
    if current.is_symlink() and current.readlink() == Path('releases/' + release):
        return
    git(repository, 'fetch', '--depth=1', '--no-tags', REPOSITORY, release)
    archive = git(repository, 'archive', '--format=tar', 'FETCH_HEAD')
    revision = stage_release(root, release, archive)
    activate(root, release, lambda: check_http(health_url, revision))
    print(f'Deployed source {revision} (production {release})', flush=True)
    protected = {p.resolve() for p in (root / 'current', root / 'previous') if p.is_symlink()}
    releases = root / 'releases'
    old = sorted(releases.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    for path in old[5:]:
        if path.resolve() not in protected and path.parent == releases and not path.is_symlink():
            shutil.rmtree(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path('/opt/stacks/arsamk/data'))
    parser.add_argument('--health-url', default='http://127.0.0.1:8092/release.json')
    args = parser.parse_args()
    args.root.mkdir(parents=True, exist_ok=True)
    with (args.root / '.deploy.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            sys.exit(0)
        sync(args.root, args.health_url)
