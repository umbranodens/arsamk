# Arsamk server deployment

Source: <https://github.com/umbranodens/arsamk>, branch `main`.

## How updates reach the server

1. Push to `main`. Pull requests run the same checks without publishing.
2. [GitHub Actions](https://github.com/umbranodens/arsamk/actions/workflows/deploy.yml) runs deployment tests, checks JavaScript syntax, and validates local HTML/CSS asset references.
3. After those checks pass, Actions packages the public site into the generated `production` branch. This branch contains no deployment scripts, repository metadata, private docs, or credentials. Do not edit it manually.
4. `arsamk-deploy.timer` checks this branch every 30 seconds. The server needs no GitHub token because the repository is public. CI success means publication succeeded; server logs and `/release.json` confirm runtime deployment separately.
5. The server validates paths, file types, checksums and local references, then atomically changes `data/current`. Nginx stays running. Failed HTTP verification restores the previous symlink. The latest five releases plus the current/previous targets are retained.

Normal delay is the Actions runtime plus up to about 30 seconds. If GitHub is unavailable or validation fails, the existing release continues serving. Multiple rapid pushes can be coalesced to the newest version. The pipeline intentionally does not execute repository scripts on the server or automatically update root-owned infrastructure files.

## Isolation and installed resources

- Host: `dev_armia@ssh.woodresidence.id`, through the existing Cloudflare SSH access.
- Stack: `/opt/stacks/arsamk`; Compose project `arsamk`.
- Containers: `arsamk-web`, `arsamk-preview`; dedicated `arsamk_arsamk` network.
- Origin: `127.0.0.1:8092`, unavailable directly from the internet/LAN.
- Deploy account: `arsamk-deploy`, system account, no login shell or Docker group membership.
- Services: `/etc/systemd/system/arsamk-deploy.service` and `.timer`.
- Root-owned code: `/opt/stacks/arsamk/bin/{pull_site,build_site}.py`.
- Writable deployment state: `/opt/stacks/arsamk/data`, including release directories and a bare Git cache.
- No existing stack, Cloudflare config, SSH authorized keys, router rule, firewall rule, or application database is changed.

Nginx runs as UID 101 with a read-only filesystem, all capabilities dropped, bounded CPU/memory/logs, and read-only content/config mounts. The service can write only its deployment data and private temporary files. Only public website data is fetched from `production`. HTTP responses require revalidation so updated CSS/JS are not hidden behind long browser caches.

`deploy/compose.yml` pins the Nginx and cloudflared image digests used for this installation. Review image updates separately and recreate only this project. Changes to `deploy/*` or deployment scripts in `main` do not automatically replace installed host files; copy reviewed versions deliberately.

## Access before the domain is purchased

The preview profile uses a dedicated Cloudflare Quick Tunnel. Find its current HTTPS URL:

```sh
docker logs arsamk-preview 2>&1 | grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' | tail -1
```

The URL is public. Quick Tunnels are temporary, have no uptime guarantee, and change hostname when their process restarts. See [Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/). The site sends `X-Robots-Tag: noindex, nofollow` on preview hostnames; its canonical links remain `https://arsamk.com/`.

Stable private access through SSH works independently of the preview URL. Run locally, leave the terminal open, then visit <http://127.0.0.1:8092>:

```sh
ssh -N -L 8092:127.0.0.1:8092 -o ExitOnForwardFailure=yes -o 'ProxyCommand=cloudflared access ssh --hostname %h' dev_armia@ssh.woodresidence.id
```

## Status and logs

After connecting to the server:

```sh
docker compose -p arsamk -f /opt/stacks/arsamk/compose.yml --profile preview ps
systemctl status arsamk-deploy.timer
sudo journalctl -u arsamk-deploy.service -n 50 --no-pager
curl --fail http://127.0.0.1:8092/release.json
curl --fail http://127.0.0.1:8092/healthz
```

`release.json` records the source commit and file checksums. Match its `revision` against `main`. A green container health check confirms that the origin can serve the deployed manifest. To retry immediately:

```sh
sudo systemctl start arsamk-deploy.service
```

## Rollback

For routine rollback, revert the problematic commit on `main` and push; the normal checks and deploy run again. For an urgent manual rollback, first stop polling and any active deployment, then atomically restore the previous release:

```sh
sudo systemctl stop arsamk-deploy.timer
sudo systemctl stop arsamk-deploy.service
cd /opt/stacks/arsamk/data
test -L previous
sudo -u arsamk-deploy ln -sfnT "$(readlink previous)" current.rollback
sudo -u arsamk-deploy mv -Tf current.rollback current
curl --fail http://127.0.0.1:8092/release.json
```

Keep the timer stopped until a corrected/reverted version has been published, then:

```sh
sudo systemctl start arsamk-deploy.timer
```

The timer will bring the site back to the generated `production` version. Nothing here touches another Compose project.

## Activate arsamk.com later

1. Purchase the domain, add it to the intended Cloudflare account, and activate its nameservers. No DNS changes have been made yet.
2. Create a **new dedicated tunnel for Arsamk** in Cloudflare. Add published application routes for `arsamk.com` and `www.arsamk.com`, both pointing to `http://web:8080`. The connector will join Arsamk's Docker network, so `web` resolves there. Configure a Cloudflare redirect from `www` to the apex to match the existing canonical URL.
3. Copy `deploy/domain-tunnel.yml.example` into `/opt/stacks/arsamk/domain-tunnel.yml`. Put the tunnel token in `/opt/stacks/arsamk/tunnel.token`, owned by `root:65532` with mode `0640` so the non-root connector can read it. The token is supplied through a Compose secret; never commit it.
4. Start only Arsamk's new connector:

```sh
docker compose -p arsamk -f /opt/stacks/arsamk/compose.yml -f /opt/stacks/arsamk/domain-tunnel.yml up -d domain
```

5. Verify HTTPS, `/release.json`, all assets, and both hostname routes. After confirmation, stop the temporary connector:

```sh
docker compose -p arsamk -f /opt/stacks/arsamk/compose.yml --profile preview stop preview
```

The existing host tunnel, its ingress, and all other project connectors stay untouched. CI/CD remains the same after domain activation.

## Installation / audit record

The initial installation used `deploy/install.sh` from a reviewed staging copy. It refuses existing Arsamk units/install paths, creates only the dedicated account/directories/units, validates configuration, starts the origin, pulls the first release, enables the timer, then starts the preview. It is a bootstrap script, not an updater.

`deploy/audit_existing.py record` stores only container IDs, start times, restart counts, running states, and SHA-256 hashes of existing Compose/deploy/shared-tunnel configuration. It does not persist inspected environment variables or credential contents. Running the script without arguments compares against that baseline. Baseline data is stored on the server at `/opt/stacks/arsamk/existing-baseline.json`.

Server project files and credentials were inspected only as needed to understand deployment patterns. Full-site uptime monitoring/alerts, domain purchase, permanent DNS/tunnel configuration, and branch protection policy are separate follow-ups.
