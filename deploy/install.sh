#!/bin/sh
# Run only after reviewing and copying this deployment directory to the new stack.
set -eu
stack=/opt/stacks/arsamk
source_dir=$stack/staging
[ "$(id -u)" -eq 0 ] || { echo 'Run as root' >&2; exit 1; }
[ -d "$source_dir/deploy" ] || exit 1
for unit in arsamk-deploy.service arsamk-deploy.timer; do
    [ ! -e "/etc/systemd/system/$unit" ] || { echo "$unit already exists" >&2; exit 1; }
done
[ ! -e "$stack/bin" ] || { echo 'Arsamk is already installed' >&2; exit 1; }
if ! id arsamk-deploy >/dev/null 2>&1; then
    useradd --system --user-group --home-dir "$stack/data" --no-create-home --shell /usr/sbin/nologin arsamk-deploy
fi
install -d -o root -g root -m 0755 "$stack/bin"
install -d -o arsamk-deploy -g arsamk-deploy -m 0755 "$stack/data"
install -o root -g root -m 0644 "$source_dir/deploy/pull_site.py" "$stack/bin/pull_site.py"
install -o root -g root -m 0644 "$source_dir/scripts/build_site.py" "$stack/bin/build_site.py"
for file in compose.yml nginx.conf; do
    install -o root -g root -m 0644 "$source_dir/deploy/$file" "$stack/$file"
done
for unit in arsamk-deploy.service arsamk-deploy.timer; do
    install -o root -g root -m 0644 "$source_dir/deploy/$unit" "/etc/systemd/system/$unit"
done
chown root:root "$stack"
chmod 0755 "$stack"
systemd-analyze verify /etc/systemd/system/arsamk-deploy.service /etc/systemd/system/arsamk-deploy.timer
docker compose --project-name arsamk --file "$stack/compose.yml" config --quiet
docker compose --project-name arsamk --file "$stack/compose.yml" up -d web
systemctl daemon-reload
systemctl start arsamk-deploy.service
systemctl enable --now arsamk-deploy.timer
docker compose --project-name arsamk --file "$stack/compose.yml" --profile preview up -d preview
