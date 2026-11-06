# Arsamk deployment plan

**Goal:** Deploy `main` to the supplied server automatically without changing existing projects.

**Architecture:** GitHub-hosted Actions validate and package only public site files into a generated `production` branch. A dedicated unprivileged systemd service polls that branch every 30 seconds, validates the archive, atomically switches Nginx's current release, and rolls back on failed HTTP verification. Docker Compose runs only the Arsamk web server and its temporary tunnel.

**Constraints:** Existing stack files, containers, credentials, networks, and Cloudflare configuration remain unchanged. No privileged runner, server SSH secret in Actions, public origin port, or execution of repository code on the host. Domain registration and permanent DNS are deferred until the user owns `arsamk.com`.

**Choices:** A self-hosted Actions runner would expose a shared host to repository jobs. SSH deployment needs non-interactive Cloudflare credentials that are not currently provisioned. A generated deployment branch provides a credential-free pull channel and avoids unauthenticated GitHub API rate limits. Work is executed inline in the clean checkout, as the user requested autonomous completion.

## Tasks

- [x] 1. Add packaging validation and tests: missing assets fail, private files stay out, symlinks/traversal fail, valid site packages successfully.
- [x] 2. Add deployment polling and tests: unsafe archives fail, releases switch atomically, failed health checks restore the previous release, old releases remain available for rollback.
- [x] 3. Add pinned GitHub Actions workflow, isolated Compose/Nginx configuration, dedicated systemd units, and operating/domain instructions.
- [ ] 4. Record baseline container identities/start times and existing configuration hashes. Install only new Arsamk resources. Run tests, deploy through a real push to `main`, verify HTTP and tunnel access, test rollback, and compare the existing stacks against baseline.

## Review focus

- Out-of-order Actions runs must not publish stale commits.
- A failed build or unavailable GitHub must leave the live release unchanged.
- Repository data must never become host executable code or escape the release directory.
- New assets must be served immediately without stale Nginx file caches.
- Polling must not overwrite a deliberate manual rollback; pause the timer for maintenance.

## Execution record

- Recon: 10 existing containers, five Compose projects, Cloudflare ingress shared by several applications; host is behind a private LAN address. Deployment will use a separate project, loopback port 8092, and dedicated tunnel.
- Python is unavailable locally; run Python verification in a new Arsamk-only staging directory on the target host using the existing system Python. Do not install or alter host dependencies.
- Independent read-only reviewer found two release-staging defects: mode 0700 inherited from the temporary directory and incomplete copies blocking retries. Regression tests reproduced both; staging now sets mode 0755 and atomically renames a validated release, repairing partial existing directories. Full suite: 10/10 passing on target Python.
- Baseline recorded 11 existing containers (including stopped containers) and eight configuration hashes before installation. No application infrastructure has been changed.
