#!/usr/bin/env python3
"""Package public assets and reject broken local resource references."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import shutil
from urllib.parse import unquote, urlsplit

ROOT_FILES = {'index.html', 'robots.txt', 'sitemap.xml', 'favicon.ico', 'release.json'}
ASSET_TYPES = {'.css', '.js', '.woff2', '.woff', '.png', '.webp', '.jpg', '.jpeg', '.svg', '.ico', '.txt'}
MAX_BYTES = 100 * 1024 * 1024


def public_path(name):
    path = PurePosixPath(name)
    if path.is_absolute() or not path.parts or any(p.startswith('.') for p in path.parts):
        return False
    return name in ROOT_FILES or (
        path.parts[0] == 'assets' and len(path.parts) > 2
        and path.parts[1] in {'css', 'js', 'font', 'img'} and path.suffix.lower() in ASSET_TYPES
    )


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if value and key in ('src', 'href', 'poster'):
                self.urls.append(value)
            if value and key == 'srcset':
                self.urls.extend(part.strip().split()[0] for part in value.split(','))


def validate(root):
    root = Path(root).resolve()
    if not (root / 'index.html').is_file():
        raise ValueError('missing index.html')
    total = 0
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'symlink is not allowed: {path}')
        if not path.is_file():
            continue
        name = path.relative_to(root).as_posix()
        if not public_path(name):
            raise ValueError(f'non-public file: {name}')
        total += path.stat().st_size
        if total > MAX_BYTES:
            raise ValueError('site exceeds 100 MiB')
        urls = []
        if path.suffix == '.html':
            parser = References()
            parser.feed(path.read_text(encoding='utf-8'))
            urls = parser.urls
        elif path.suffix == '.css':
            urls = re.findall(r'url\([\s\x22\x27]*([^\)\x22\x27]+)', path.read_text(encoding='utf-8'))
        for url in urls:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (root / unquote(parsed.path).lstrip('/') if parsed.path.startswith('/')
                      else path.parent / unquote(parsed.path)).resolve()
            if target == root:
                target = root / 'index.html'
            if not target.is_relative_to(root) or not target.is_file():
                raise ValueError(f'missing or unsafe asset: {name}: {url}')


def build(source, output, revision):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not re.fullmatch('[0-9a-f]{40}', revision):
        raise ValueError('revision must be a full Git SHA')
    if output.exists():
        raise ValueError('output must not already exist')
    paths = [source / name for name in ROOT_FILES - {'release.json'} if (source / name).exists()]
    assets = source / 'assets'
    if assets.is_symlink():
        raise ValueError('assets symlink is not allowed')
    if assets.exists():
        paths.extend(assets.rglob('*'))
    for path in paths:
        if path.is_symlink():
            raise ValueError(f'symlink is not allowed: {path}')
    output.mkdir(parents=True)
    for path in paths:
        name = path.relative_to(source).as_posix()
        if path.is_file() and public_path(name):
            target = output / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    validate(output)
    files = {path.relative_to(output).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
             for path in sorted(output.rglob('*')) if path.is_file()}
    (output / 'release.json').write_text(json.dumps({'revision': revision, 'files': files}, indent=2) + '\n')
    print(f'Packaged {len(files)} public files for {revision}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--revision', required=True)
    args = parser.parse_args()
    build(args.source, args.output, args.revision)
