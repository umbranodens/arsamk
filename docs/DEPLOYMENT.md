# Arsamk server deployment

Source: <https://github.com/umbranodens/arsamk>, branch `main`.

## Production domain activated on 7 November 2026

- Public URL: <https://arsamk.com/>. HTTP and `www.arsamk.com` redirect permanently to the HTTPS apex while preserving paths and query strings.
- Dedicated remotely managed Cloudflare Tunnel: `arsamk`, ID `92d2cdf3-3acb-43ea-8a46-447c9c1067c4`. Both hostname routes target `http://web:8080`; unmatched hostnames return 404.
- Connector: `arsamk-domain`, configured by `deploy/domain-tunnel.yml` alongside the base Compose file. The token remains only on the server at `/opt/stacks/arsamk/tunnel.token`, owned by `root:65532`, mode `0640`.
- Apex and `www` DNS records are proxied CNAMEs to the dedicated tunnel. The former parking records were replaced; other DNS records and existing project tunnels were not changed.
- HTTPS certificate validation, all 39 site files (allowing Cloudflare-managed additions to robots.txt), six private/missing URL probes, redirects, and production indexing headers passed verification.
- The preview connector was stopped after the production domain passed verification. Its former URL is no longer the public site address. The optional preview profile remains available for diagnostics.
- Temporary Cloudflare management credentials and setup/rollback files were removed from the host. The runtime connector has only its tunnel-specific token. Website content deployment remains unchanged.
- After activation, all 11 pre-existing containers retained their IDs, start times, running states and restart counts, and all eight existing configuration hashes matched the pre-activation snapshot. Arsamk's Nginx configuration was reloaded without restarting its container.

## Verified on 6 November 2026

- Temporary public URL: <https://wyoming-diagram-criteria-applies.trycloudflare.com>. Retrieve the current URL from container logs if the preview connector restarts.
- Real push-to-deploy verified with source commit `0c4088479d1ffa39b412ccdd38caadebb4430681`: [Actions run](https://github.com/umbranodens/arsamk/actions/runs/42214377277). Nginx retained its original container/start time across the update.
- Ten deployment tests passed. All 39 origin files matched their manifest checksums. Public HTTPS preserved 38 file checksums; Cloudflare prepends managed crawler rules to `robots.txt` while preserving the original rules and sitemap. This is controlled by the temporary Cloudflare hostname.
- Six private/missing URL probes returned 403/404. Preview indexing headers and response headers were verified.
- The installed activation/HTTP verification functions restored the previous symlink after a forced revision mismatch in an isolated test directory. The live site and polling timer were not interrupted for this rollback test.
- All 11 existing containers (including stopped containers) retained their IDs, start times, running states and restart counts. Eight hashes of existing stack/deploy/shared-tunnel configuration matched the pre-installation baseline.
- Nginx is healthy; the polling timer is enabled and active. Port 8092 binds only to loopback. No public IP/router/firewall changes were required.

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
- Active containers: `arsamk-web`, `arsamk-domain`; dedicated `arsamk_arsamk` network. `arsamk-preview` is stopped.
- Origin: `127.0.0.1:8092`, unavailable directly from the internet/LAN.
- Deploy account: `arsamk-deploy`, system account, no login shell or Docker group membership.
- Services: `/etc/systemd/system/arsamk-deploy.service` and `.timer`.
- Root-owned code: `/opt/stacks/arsamk/bin/{pull_site,build_site}.py`.
- Writable deployment state: `/opt/stacks/arsamk/data`, including release directories and a bare Git cache.
- No existing stack, Cloudflare config, SSH authorized keys, router rule, firewall rule, or application database is changed.

Nginx runs as UID 101 with a read-only filesystem, all capabilities dropped, bounded CPU/memory/logs, and read-only content/config mounts. The service can write only its deployment data and private temporary files. Only public website data is fetched from `production`. HTTP responses require revalidation so updated CSS/JS are not hidden behind long browser caches. `Cache-Control: no-transform` keeps Cloudflare from rewriting the deployed HTML (including its email links), allowing public responses to match the release checksums.

`deploy/compose.yml` pins the Nginx and cloudflared image digests used for this installation. Review image updates separately and recreate only this project. Changes to `deploy/*` or deployment scripts in `main` do not automatically replace installed host files; copy reviewed versions deliberately.

## Production and diagnostic access

Use <https://arsamk.com/> for normal access. The domain and its HTTPS connection are now served by the permanent connector. The old Quick Tunnel was retired after verification.

For temporary diagnostics only, the preview profile can start a separate Quick Tunnel. This is optional and is not needed for deployment or the production domain:

```sh
docker compose -p arsamk -f /opt/stacks/arsamk/compose.yml --profile preview up -d --no-deps preview
```

Find that diagnostic tunnel's current URL:

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
docker compose -p arsamk -f /opt/stacks/arsamk/compose.yml -f /opt/stacks/arsamk/domain-tunnel.yml ps
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

## Rebuild or maintain the domain connector

The domain is already active. To rebuild the connector on a replacement server, reuse the dedicated `arsamk` tunnel in Cloudflare. Its published application routes for `arsamk.com` and `www.arsamk.com` must both point to `http://web:8080`. Nginx handles the canonical HTTPS redirects; no shared host tunnel needs editing.

Copy `deploy/domain-tunnel.yml` into `/opt/stacks/arsamk/domain-tunnel.yml`. Put the tunnel token in `/opt/stacks/arsamk/tunnel.token`, owned by `root:65532` with mode `0640` so the non-root connector can read it. The token is supplied through a Compose secret; never commit it.

Start or recreate only Arsamk's connector:

```sh
docker compose -p arsamk -f /opt/stacks/arsamk/compose.yml -f /opt/stacks/arsamk/domain-tunnel.yml up -d --no-deps domain
```

Verify HTTPS, `/release.json`, all assets, and both hostname routes. If the temporary diagnostic connector was enabled, stop it when finished:

```sh
docker compose -p arsamk -f /opt/stacks/arsamk/compose.yml --profile preview stop preview
```

For a connector-token rotation, obtain a replacement for this tunnel from Cloudflare, update only `tunnel.token` with the same ownership/mode, and recreate only the `domain` service. The existing host tunnel, its ingress, and all other project connectors stay untouched. CI/CD does not depend on this token or change during domain maintenance.

## Installation / audit record

The initial installation used `deploy/install.sh` from a reviewed staging copy. It refuses existing Arsamk units/install paths, creates only the dedicated account/directories/units, validates configuration, starts the origin, pulls the first release, enables the timer, then starts the preview. Keep this script for rebuilding on a replacement server; it is not used during routine deployments.

The one-time audit script and completed implementation plan have been removed from the repository after installation. They are not part of CI/CD; the audit results are recorded above and their original source remains available in Git history. Temporary staging/build directories used for installation are not needed by the running site or polling service.

On 7 November 2026, `/opt/stacks/arsamk/staging`, `staging-built`, `validated-site`, and `existing-baseline.json` were removed after checking container mounts and service references. This freed approximately 40 MiB. Existing workloads/configuration matched before and after cleanup, and neither Arsamk container was restarted. The active `bin/`, `data/`, Compose/Nginx configuration, and systemd units remain installed.

Server project files and credentials were inspected only as needed to understand deployment patterns. Full-site uptime monitoring/alerts and branch protection policy remain separate follow-ups.
