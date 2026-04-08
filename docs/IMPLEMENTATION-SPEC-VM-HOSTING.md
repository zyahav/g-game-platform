# Implementation Spec — VM Hosting for Publish Flow v1

**Audience: Operator / VM administrator**
**Status: Ready for review**
**Date: April 2026**
**Companion spec:** `docs/IMPLEMENTATION-SPEC-PUBLISH.md`

This spec covers the server-side setup required so that `make publish` in a generated
student project results in a live public URL.

This document is for the operator who manages the VM.
It does not describe generated-project code changes in detail. Those are specified in
`docs/IMPLEMENTATION-SPEC-PUBLISH.md`.

Use both specs together. They implement the same publish contract.

---

## 1. Shared Contract

This section must stay identical in meaning to `IMPLEMENTATION-SPEC-PUBLISH.md`.

### `publish.toml` shape

Generated projects use this exact config shape:

```toml
[publish]
user_handle = ""
project_name = ""
vm_host = ""
public_url = ""
deploy_remote = ""
ssh_key_path = ""
```

Field meanings:
- `user_handle`: stable namespace for the student on the VM
- `project_name`: stable project identity under that namespace
- `vm_host`: SSH host the agent will push to
- `public_url`: final public URL the student opens in the browser
- `deploy_remote`: optional explicit remote; if empty it is derived
- `ssh_key_path`: local path to the private SSH deploy key for this project

### `deploy_remote` derivation rule

If `deploy_remote` is empty, the generated-project tooling derives it as:

```text
<user_handle>@<vm_host>:/srv/git/<user_handle>/<project_name>.git
```

The VM setup in this spec must match that path exactly.

### Report envelope contract

Every publish attempt returns this exact Dev → PM envelope:

#### Success
```text
--- START: DEV TO PM ---
RESULT: SUCCESS
PUBLIC_URL: https://yourdomain.com/user/project/
EXPORT: PASS
VALIDATION: PASS
DEPLOY: PASS
NEXT_ACTION: Open the link and tell me what you see.
--- END: DEV TO PM ---
```

#### Failure
```text
--- START: DEV TO PM ---
RESULT: FAIL
PUBLIC_URL:
EXPORT: PASS
VALIDATION: FAIL
DEPLOY: NOT_RUN
DETAIL: Missing index.html in build/web/
NEXT_ACTION: Ask me to fix the web export preset.
--- END: DEV TO PM ---
```

Field rules:
- `RESULT`: `SUCCESS` or `FAIL`
- `PUBLIC_URL`: filled on success, empty on failure
- `EXPORT`, `VALIDATION`, `DEPLOY`: `PASS`, `FAIL`, or `NOT_RUN`
- `DETAIL`: optional on success, required on failure when there is a concrete issue
- `NEXT_ACTION`: always one short actionable sentence

### SSH key model

The auth model for v1 is:
- one SSH deploy key per project
- operator creates and installs the keypair
- the generated project holds the private key at `ssh_key_path`
- the agent uses the key during `make publish-init` / `make publish`

Security boundary:
- one project key must not be usable for any other project repo

---

## 2. VM Prerequisites

These must already exist before any project-specific setup begins.

### Required baseline

- Nginx installed and running
- Git installed
- operator has SSH access to the VM with sudo privileges
- `/srv/git` exists
- `/var/www/projects` exists

Recommended baseline commands:

```bash
sudo apt-get update
sudo apt-get install -y nginx git
sudo systemctl enable nginx
sudo systemctl start nginx
sudo mkdir -p /srv/git
sudo mkdir -p /var/www/projects
```

### Repo-restricted SSH helper

To enforce one-key-per-project while still using one system user per student,
install this helper once per VM:

Path:

```text
/usr/local/bin/allow-one-repo-push
```

Content:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: allow-one-repo-push <bare-repo-path>" >&2
  exit 1
fi

ALLOWED_REPO="$1"
CMD="${SSH_ORIGINAL_COMMAND:-}"

case "$CMD" in
  "git-receive-pack '$ALLOWED_REPO'"|"git-receive-pack \"$ALLOWED_REPO\""|"git-receive-pack $ALLOWED_REPO")
    exec git-shell -c "$CMD"
    ;;
  *)
    echo "This key is only authorized to push to $ALLOWED_REPO" >&2
    exit 1
    ;;
esac
```

Install it with:

```bash
sudo tee /usr/local/bin/allow-one-repo-push >/dev/null <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: allow-one-repo-push <bare-repo-path>" >&2
  exit 1
fi

ALLOWED_REPO="$1"
CMD="${SSH_ORIGINAL_COMMAND:-}"

case "$CMD" in
  "git-receive-pack '$ALLOWED_REPO'"|"git-receive-pack \"$ALLOWED_REPO\""|"git-receive-pack $ALLOWED_REPO")
    exec git-shell -c "$CMD"
    ;;
  *)
    echo "This key is only authorized to push to $ALLOWED_REPO" >&2
    exit 1
    ;;
esac
EOF
sudo chmod 755 /usr/local/bin/allow-one-repo-push
```

This helper is what makes the per-project key boundary real.

---

## 3. Operator Setup Steps

This section is one-time **per project**, except where noted.

### 3.1 Create the system user (one-time per student)

Each student gets one dedicated system user named after `user_handle`.

Example:

```bash
export USER_HANDLE="alice"
sudo adduser \
  --system \
  --home /srv/git/${USER_HANDLE} \
  --shell /usr/bin/git-shell \
  --group \
  "${USER_HANDLE}"
sudo mkdir -p /srv/git/${USER_HANDLE}/.ssh
sudo chown -R ${USER_HANDLE}:${USER_HANDLE} /srv/git/${USER_HANDLE}
sudo chmod 700 /srv/git/${USER_HANDLE}/.ssh
```

This user owns that student namespace under `/srv/git/<user_handle>/`.

### 3.2 Create the bare repo (one-time per project)

Example:

```bash
export USER_HANDLE="alice"
export PROJECT_NAME="platformer"

sudo -u ${USER_HANDLE} git init --bare /srv/git/${USER_HANDLE}/${PROJECT_NAME}.git
```

Expected path:

```text
/srv/git/<user_handle>/<project_name>.git
```

### 3.3 Create the live deploy folder with explicit ownership and permissions

Example:

```bash
export USER_HANDLE="alice"
export PROJECT_NAME="platformer"

sudo mkdir -p /var/www/projects/${USER_HANDLE}/${PROJECT_NAME}/current
sudo chown -R ${USER_HANDLE}:${USER_HANDLE} /var/www/projects/${USER_HANDLE}/${PROJECT_NAME}
sudo find /var/www/projects/${USER_HANDLE}/${PROJECT_NAME} -type d -exec chmod 755 {} +
sudo find /var/www/projects/${USER_HANDLE}/${PROJECT_NAME} -type f -exec chmod 644 {} +
```

Required meaning:
- owner = student system user
- group = same student system user
- directories = writable by owner, readable/executable by Nginx
- files = writable by owner, readable by Nginx

This is the required `chown` / `chmod` baseline.

### 3.4 Install the post-receive hook with exact content

Hook path:

```text
/srv/git/<user_handle>/<project_name>.git/hooks/post-receive
```

Hook content:

```bash
#!/usr/bin/env bash
set -euo pipefail

USER_HANDLE="alice"
PROJECT_NAME="platformer"
REPO_DIR="/srv/git/${USER_HANDLE}/${PROJECT_NAME}.git"
DEPLOY_ROOT="/var/www/projects/${USER_HANDLE}/${PROJECT_NAME}"
DEPLOY_DIR="${DEPLOY_ROOT}/current"
LOG_FILE="${DEPLOY_ROOT}/deploy-hook.log"

mkdir -p "${DEPLOY_DIR}"
touch "${LOG_FILE}"

{
  echo "=== $(date -Iseconds) post-receive start ==="
  echo "repo=${REPO_DIR}"
  echo "deploy_dir=${DEPLOY_DIR}"

  if [ ! -w "${DEPLOY_DIR}" ]; then
    echo "deploy target is not writable: ${DEPLOY_DIR}"
    exit 1
  fi

  export GIT_WORK_TREE="${DEPLOY_DIR}"
  git --git-dir="${REPO_DIR}" --work-tree="${DEPLOY_DIR}" checkout -f main
  git --git-dir="${REPO_DIR}" --work-tree="${DEPLOY_DIR}" clean -fdx

  find "${DEPLOY_DIR}" -type d -exec chmod 755 {} +
  find "${DEPLOY_DIR}" -type f -exec chmod 644 {} +

  echo "=== $(date -Iseconds) post-receive success ==="
} >>"${LOG_FILE}" 2>&1
```

Install it with:

```bash
export USER_HANDLE="alice"
export PROJECT_NAME="platformer"
HOOK_PATH="/srv/git/${USER_HANDLE}/${PROJECT_NAME}.git/hooks/post-receive"

sudo tee "${HOOK_PATH}" >/dev/null <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

USER_HANDLE="alice"
PROJECT_NAME="platformer"
REPO_DIR="/srv/git/${USER_HANDLE}/${PROJECT_NAME}.git"
DEPLOY_ROOT="/var/www/projects/${USER_HANDLE}/${PROJECT_NAME}"
DEPLOY_DIR="${DEPLOY_ROOT}/current"
LOG_FILE="${DEPLOY_ROOT}/deploy-hook.log"

mkdir -p "${DEPLOY_DIR}"
touch "${LOG_FILE}"

{
  echo "=== $(date -Iseconds) post-receive start ==="
  echo "repo=${REPO_DIR}"
  echo "deploy_dir=${DEPLOY_DIR}"

  if [ ! -w "${DEPLOY_DIR}" ]; then
    echo "deploy target is not writable: ${DEPLOY_DIR}"
    exit 1
  fi

  export GIT_WORK_TREE="${DEPLOY_DIR}"
  git --git-dir="${REPO_DIR}" --work-tree="${DEPLOY_DIR}" checkout -f main
  git --git-dir="${REPO_DIR}" --work-tree="${DEPLOY_DIR}" clean -fdx

  find "${DEPLOY_DIR}" -type d -exec chmod 755 {} +
  find "${DEPLOY_DIR}" -type f -exec chmod 644 {} +

  echo "=== $(date -Iseconds) post-receive success ==="
} >>"${LOG_FILE}" 2>&1
EOF

sudo chown ${USER_HANDLE}:${USER_HANDLE} "${HOOK_PATH}"
sudo chmod 755 "${HOOK_PATH}"
```

Before saving, replace the placeholder `USER_HANDLE` and `PROJECT_NAME` values inside
the hook with the real project values.

### 3.5 Generate the SSH keypair (one-time per project)

The operator generates one SSH keypair per project in a trusted environment.

Example command on the operator machine:

```bash
export USER_HANDLE="alice"
export PROJECT_NAME="platformer"
ssh-keygen \
  -t ed25519 \
  -f "${HOME}/.ssh/${USER_HANDLE}_${PROJECT_NAME}_deploy" \
  -N "" \
  -C "${USER_HANDLE}/${PROJECT_NAME} deploy"
```

This produces:
- private key: `~/.ssh/<user_handle>_<project_name>_deploy`
- public key: `~/.ssh/<user_handle>_<project_name>_deploy.pub`

### 3.6 Install the public key on the VM (one-time per project)

The public key must be restricted to exactly one bare repo using the helper script.

Example:

```bash
export USER_HANDLE="alice"
export PROJECT_NAME="platformer"
export REPO_PATH="/srv/git/${USER_HANDLE}/${PROJECT_NAME}.git"
export PUBKEY="$(cat "${HOME}/.ssh/${USER_HANDLE}_${PROJECT_NAME}_deploy.pub")"

printf 'command="/usr/local/bin/allow-one-repo-push %s",no-agent-forwarding,no-port-forwarding,no-pty,no-user-rc,no-X11-forwarding %s\n' \
  "${REPO_PATH}" \
  "${PUBKEY}" \
| sudo tee -a /srv/git/${USER_HANDLE}/.ssh/authorized_keys >/dev/null

sudo chown ${USER_HANDLE}:${USER_HANDLE} /srv/git/${USER_HANDLE}/.ssh/authorized_keys
sudo chmod 600 /srv/git/${USER_HANDLE}/.ssh/authorized_keys
```

This is what enforces:
- one SSH key per project
- one key cannot push to another project repo

### 3.7 Add the Nginx location block with WASM MIME type explicitly included

Server config snippet:

```nginx
types {
    application/wasm wasm;
}

location /alice/platformer/ {
    alias /var/www/projects/alice/platformer/current/;
    index index.html;
    try_files $uri $uri/ /alice/platformer/index.html;
}
```

Install a site snippet like:

```bash
sudo tee /etc/nginx/snippets/alice-platformer.conf >/dev/null <<'EOF'
types {
    application/wasm wasm;
}

location /alice/platformer/ {
    alias /var/www/projects/alice/platformer/current/;
    index index.html;
    try_files $uri $uri/ /alice/platformer/index.html;
}
EOF
```

Then include it from the active server block and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Important:
- The `types { application/wasm wasm; }` line is required
- Without it, Godot Web exports may load files but fail to run in the browser

### 3.8 Prepare the student handoff values

These exact values must be ready before the student project uses publish:

```toml
[publish]
user_handle = "alice"
project_name = "platformer"
vm_host = "games.example.com"
public_url = "https://games.example.com/alice/platformer/"
deploy_remote = ""
ssh_key_path = "~/.ssh/alice_platformer_deploy"
```

Notes:
- Leave `deploy_remote` empty if you want the generated-project tooling to derive it
- `ssh_key_path` must point to the private key on the student machine
- The operator must deliver the private key securely to the student project environment

---

## 4. Failure Modes

Each failure mode below must be diagnosable by the operator and understandable from
the agent’s publish report.

### 4.1 Post-receive hook silent failure

#### What it looks like
- `git push` appears to succeed
- the student opens the URL and still sees the old version

#### How to diagnose

Check the hook log:

```bash
export USER_HANDLE="alice"
export PROJECT_NAME="platformer"
sudo tail -n 100 /var/www/projects/${USER_HANDLE}/${PROJECT_NAME}/deploy-hook.log
```

Also confirm the hook is executable:

```bash
sudo ls -l /srv/git/${USER_HANDLE}/${PROJECT_NAME}.git/hooks/post-receive
```

#### What the agent report says

If push succeeds but the operator later confirms the site did not update, the agent report
from the student side may still say:

```text
DEPLOY: PASS
```

That is why the operator must check the hook log first.

Operator action:
- treat this as a VM-side failure
- inspect `deploy-hook.log`
- inspect ownership and permissions on the deploy folder

### 4.2 WASM MIME type missing

#### What it looks like
- the site opens
- browser console shows MIME or WebAssembly load errors
- the game does not actually run

#### How to diagnose

Check the Nginx config for:

```nginx
types {
    application/wasm wasm;
}
```

Confirm the exported `.wasm` file is served with the correct content type:

```bash
curl -I https://games.example.com/alice/platformer/<yourfile>.wasm
```

Expected header:

```text
Content-Type: application/wasm
```

#### What the agent report says

The agent will usually report:

```text
EXPORT: PASS
VALIDATION: PASS
DEPLOY: PASS
```

because the failure is in serving, not exporting or pushing.

Operator action:
- fix the Nginx config
- reload Nginx
- hard refresh the page

### 4.3 Deploy folder permission errors

#### What it looks like
- push may succeed
- hook log shows write errors
- site stays stale or partially updates

#### How to diagnose

Check ownership and permissions:

```bash
export USER_HANDLE="alice"
export PROJECT_NAME="platformer"
sudo ls -ld /var/www/projects/${USER_HANDLE}/${PROJECT_NAME}
sudo ls -ld /var/www/projects/${USER_HANDLE}/${PROJECT_NAME}/current
```

Required baseline:
- owner = `<user_handle>`
- group = `<user_handle>`
- directories writable by owner

Fix with:

```bash
sudo chown -R ${USER_HANDLE}:${USER_HANDLE} /var/www/projects/${USER_HANDLE}/${PROJECT_NAME}
sudo find /var/www/projects/${USER_HANDLE}/${PROJECT_NAME} -type d -exec chmod 755 {} +
sudo find /var/www/projects/${USER_HANDLE}/${PROJECT_NAME} -type f -exec chmod 644 {} +
```

#### What the agent report says

If push succeeds but deploy folder updates fail in the hook, the student-side report may still show:

```text
DEPLOY: PASS
```

because the Git push completed. This is another reason the hook log is part of the operator runbook.

### 4.4 SSH key not authorized

#### What it looks like
- `make publish` fails during push
- git reports permission denied or access denied

#### How to diagnose

Check:
- the authorized key entry exists
- the forced command points to the correct repo
- the private key path matches `ssh_key_path`

Commands:

```bash
export USER_HANDLE="alice"
sudo cat /srv/git/${USER_HANDLE}/.ssh/authorized_keys
```

On the student machine, the agent/operator should also confirm:
- the key file exists
- the key file has permission `600`

#### What the agent report says

Expected failure report:

```text
RESULT: FAIL
PUBLIC_URL:
EXPORT: PASS
VALIDATION: PASS
DEPLOY: FAIL
DETAIL: SSH authentication failed for deploy remote.
NEXT_ACTION: Ask the operator to verify the authorized key and ssh_key_path for this project.
```

---

## 5. Key Lifecycle

### 5.1 Who generates the keypair

The operator generates the keypair.

Reason:
- trusted environment
- consistent naming
- controlled security boundary

### 5.2 Who installs the public key

The operator installs the public key on the VM.

Method:
- append to `/srv/git/<user_handle>/.ssh/authorized_keys`
- use the forced-command wrapper for the exact project repo

### 5.3 Who holds the private key

The student project environment holds the private key locally at:

```text
ssh_key_path
```

This path is stored in `publish.toml`.

The operator must deliver the private key securely to the project machine.

### 5.4 Who rotates the key

The operator rotates the key.

Rotation method:
1. generate a new keypair
2. replace the old `authorized_keys` entry for that project
3. deliver the new private key securely
4. update `ssh_key_path` if the local filename changed

### 5.5 Who revokes the key

The operator revokes the key.

Revocation method:
1. remove the matching entry from `/srv/git/<user_handle>/.ssh/authorized_keys`
2. optionally archive or delete the private key copy held for that project

### 5.6 What the agent sees on a revoked key

When a revoked key is still configured in the generated project:
- export may still pass
- validation may still pass
- push fails with auth error

Expected report:

```text
RESULT: FAIL
PUBLIC_URL:
EXPORT: PASS
VALIDATION: PASS
DEPLOY: FAIL
DETAIL: SSH authentication failed for deploy remote.
NEXT_ACTION: Ask the operator to rotate or reinstall the deploy key for this project.
```

---

## 6. Agent Behavior Reference

This is a short reference only. Full generated-project behavior belongs in
`docs/IMPLEMENTATION-SPEC-PUBLISH.md`.

### What `make publish-init` does on the agent side

The generated-project agent is expected to:
- read `[publish]` from `publish.toml`
- derive `deploy_remote` if it is empty
- ensure `build/web/` exists after export
- initialize a nested Git repo in `build/web/` if missing
- configure the `deploy` remote
- configure SSH usage from `ssh_key_path`

The operator-side setup in this VM spec is what makes those agent steps succeed.

### Cross-spec consistency checks

Before either spec is considered ready for implementation, verify side by side that:
- `[publish]` table shape matches exactly
- `deploy_remote` derivation rule matches exactly
- `ssh_key_path` handling is consistent
- report field names match exactly:
  - `RESULT`
  - `PUBLIC_URL`
  - `EXPORT`
  - `VALIDATION`
  - `DEPLOY`
  - `DETAIL`
  - `NEXT_ACTION`
