import importlib.util
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class PackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = load_module('site_build', ROOT / 'scripts/build_site.py')

    def test_package_excludes_private_files_and_records_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source'
            source.mkdir()
            (source / 'index.html').write_text('<html><body>Arsamk</body></html>')
            (source / '.env').write_text('SECRET=private')
            (source / 'deploy.py').write_text('private')
            (source / 'assets/docs').mkdir(parents=True)
            (source / 'assets/docs/private.png').write_bytes(b'private')
            output = root / 'output'
            self.site.build(source, output, 'a' * 40)
            self.assertEqual(sorted(p.name for p in output.iterdir()),
                             ['index.html', 'release.json'])
            self.assertEqual(json.loads((output / 'release.json').read_text())['revision'], 'a' * 40)

    def test_missing_local_asset_fails_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<img src="assets/missing.webp">')
            with self.assertRaisesRegex(ValueError, 'missing'):
                self.site.build(root, root / 'output', 'a' * 40)

    def test_symlink_cannot_publish_external_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<html></html>')
            (root / 'assets/font').mkdir(parents=True)
            (root / 'assets/font/leak.txt').symlink_to('/etc/passwd')
            with self.assertRaisesRegex(ValueError, 'symlink'):
                self.site.build(root, root / 'output', 'a' * 40)


class DeploymentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deploy = load_module('site_deploy', ROOT / 'deploy/pull_site.py')

    def archive(self, files):
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w') as archive:
            for name, data in files.items():
                item = tarfile.TarInfo(name)
                item.size = len(data)
                archive.addfile(item, io.BytesIO(data))
        return stream.getvalue()

    def test_archive_traversal_and_private_files_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            for path in ('../escape', '/etc/escape', '.env', 'deploy/payload.py', 'assets/.env',
                         'assets/docs/private.png', 'assets/img/../../escape.png'):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    self.deploy.extract(self.archive({path: b'secret'}), Path(tmp))
            self.assertFalse((Path(tmp).parent / 'escape').exists())

    def test_archive_symlink_is_rejected(self):
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w') as archive:
            item = tarfile.TarInfo('assets/font/leak.txt')
            item.type = tarfile.SYMTYPE
            item.linkname = '/etc/passwd'
            archive.addfile(item)
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(ValueError):
            self.deploy.extract(stream.getvalue(), Path(tmp))

    def test_health_failure_restores_live_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'releases/old').mkdir(parents=True)
            (root / 'releases/new').mkdir()
            (root / 'current').symlink_to('releases/old')
            def failed_check():
                self.assertEqual((root / 'current').resolve(), root / 'releases/new')
                raise RuntimeError('HTTP check failed')
            with self.assertRaisesRegex(RuntimeError, 'HTTP check failed'):
                self.deploy.activate(root, 'new', failed_check)
            self.assertEqual((root / 'current').readlink(), Path('releases/old'))

    def test_successful_activation_keeps_previous_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'releases/old').mkdir(parents=True)
            (root / 'releases/new').mkdir()
            (root / 'current').symlink_to('releases/old')
            self.deploy.activate(root, 'new', lambda: None)
            self.assertEqual((root / 'current').readlink(), Path('releases/new'))
            self.assertEqual((root / 'previous').readlink(), Path('releases/old'))

    def test_tampered_release_fails_before_activation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<html>Tampered</html>')
            (root / 'release.json').write_text(json.dumps({
                'revision': 'a' * 40, 'files': {'index.html': '0' * 64}}))
            with self.assertRaisesRegex(ValueError, 'checksums'):
                self.deploy.verify_release(root)

    def valid_archive(self):
        content = b'<html>Arsamk</html>'
        manifest = json.dumps({'revision': 'a' * 40, 'files': {
            'index.html': hashlib.sha256(content).hexdigest()}}).encode()
        return self.archive({'index.html': content, 'release.json': manifest})

    def test_staged_release_is_readable_by_the_web_user(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.deploy.stage_release(root, 'b' * 40, self.valid_archive())
            release = root / 'releases' / ('b' * 40)
            self.assertEqual(release.stat().st_mode & 0o777, 0o755)
            self.assertEqual((release / 'index.html').stat().st_mode & 0o777, 0o644)

    def test_retry_repairs_a_partial_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release = root / 'releases' / ('b' * 40)
            release.mkdir(parents=True)
            (release / 'incomplete').write_text('interrupted copy')
            self.deploy.stage_release(root, 'b' * 40, self.valid_archive())
            self.assertEqual((release / 'index.html').read_bytes(), b'<html>Arsamk</html>')
            self.assertFalse((release / 'incomplete').exists())


if __name__ == '__main__':
    unittest.main()
