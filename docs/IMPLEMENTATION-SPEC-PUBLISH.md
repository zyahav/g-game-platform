# Implementation Spec — Publish Flow v1

**Status: Ready for implementation**
**Date: April 2026**
**Depends on: approved decisions in DECISION-STARTUP-AND-LEARNING-LAYER.md**

This spec translates three locked decisions into exact implementation tasks.
No implementation should begin before this spec is reviewed and approved.

---

## Locked Decisions

1. **First black-box publish happens after Lesson 3**
   The first publish is introduced after the student has placed their own platform
   and felt genuine ownership of the game. Lessons 1–3 come first.
   Early publish is black-box magic. How it works is explained in a later lesson.

2. **Publish request starts in Coach, not directly in Dev**
   Student asks Kaya to publish. Kaya recognizes it as a filesystem operation
   and hands it to the Dev thread using the normal envelope format.
   The student never initiates publish directly in the Dev thread.

3. **Dev always replies with a strict report envelope**
   Every publish attempt returns a structured report the student carries back to Kaya.
   See the Report Contract section below.

4. **Auth model: SSH deploy key per project**
   One SSH deploy key per project (not per student — per project).
   This matches the existing VM hosting plan and bare-repo architecture.
   No Gitea or token infrastructure required.
   Security boundary: one project cannot affect another.
   Key path stored in `publish.toml` as `ssh_key_path`.
   Agent configures SSH during `make publish-init`.

5. **`build/` excluded from generated project's parent `.gitignore`**
   The source repo must not track exported web artifacts.
   `build/web/` becomes a nested deploy working copy.
   The parent source repo `.gitignore` must include `build/`.

6. **Config format: `publish.toml` with flat fallback parser**
   Use `publish.toml` for human-readable student-facing config.
   Parse with `tomllib` on Python 3.11+.
   Use a small purpose-built fallback for older Python.
   The fallback handles only flat string key=value pairs.
   No TOML nesting, arrays, or tables in v1.

7. **Architecture lesson about how publish works is deferred**
   Early publish is black-box. The student sees magic.
   A later lesson (after Lesson 10) explains the full publish flow:
   export, deploy repo, SSH, VM, Nginx, post-receive hook.
   That lesson is the progressive exposure moment for publish.

---

## Report Contract

Every publish attempt returns this exact envelope from Dev to PM.

### Success
```
--- START: DEV TO PM ---
RESULT: SUCCESS
PUBLIC_URL: https://yourdomain.com/user/project/
EXPORT: PASS
VALIDATION: PASS
DEPLOY: PASS
NEXT_ACTION: Open the link and tell me what you see.
--- END: DEV TO PM ---
```

### Failure
```
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
- RESULT: always SUCCESS or FAIL
- PUBLIC_URL: filled on success, empty on failure
- EXPORT / VALIDATION / DEPLOY: always PASS, FAIL, or NOT_RUN
- DETAIL: include only when there is a specific failure message
- NEXT_ACTION: always one short actionable sentence

---

## What Gets Changed

### 1. Generated project `.gitignore`

Current generated `.gitignore` (in `generate_project.py`):

```
# Godot 4+ specific ignores
.godot/
/android/

# OS/editor junk
.DS_Store
Thumbs.db

# Temp/build output
*.tmp
*.temp
*.log
.home/
```

Add one line:

```
# Web export and deploy working copy
build/
```

This prevents exported web artifacts from appearing as untracked files
in the source repo.

### 2. Generated `publish.toml` template

Add to `generate_project_contents()` in `generate_project.py`:

```toml
# Publish configuration for this project.
# Fill in these values before running: make publish

[publish]
user_handle = ""
project_name = ""
vm_host = ""
public_url = ""
deploy_remote = ""
ssh_key_path = ""

# deploy_remote is optional.
# If left empty, it is derived as:
#   <user_handle>@<vm_host>:/srv/git/<user_handle>/<project_name>.git

# ssh_key_path is the path to your SSH deploy key for this project.
# Example: ~/.ssh/myproject_deploy_key
# One key per project. The agent configures this during publish-init.
```

Place at: `output_dir / "publish.toml"`

### 3. Generated Makefile — add publish targets

Add to the Makefile template in `generate_project.py`:

```makefile
VOICE ?= af_bella
TTS_TEXT ?= Hello, this is a live TTS test from Kaya.

export-web:
	@$(PYTHON_BIN) scripts/project_tasks.py export-web

publish-check:
	@$(PYTHON_BIN) scripts/project_tasks.py publish-check

publish-init:
	@$(PYTHON_BIN) scripts/project_tasks.py publish-init

publish:
	@$(PYTHON_BIN) scripts/project_tasks.py publish

publish-info:
	@$(PYTHON_BIN) scripts/project_tasks.py publish-info

publish-status:
	@$(PYTHON_BIN) scripts/project_tasks.py publish-status
```

Also add them to the `.PHONY` list.

### 4. Generated `project_tasks.py` — add publish commands

Add `publish` commands to the `choices` list in `parse_args()`:

```python
choices=[
    "doctor", "smoke", "test", "verify", "ci-verify",
    "play", "editor", "setup-hooks", "tts", "tts-test",
    "export-web", "publish-check", "publish-init",
    "publish", "publish-info", "publish-status",
]
```

Add the TOML config loader (flat fallback for older Python):

```python
def load_publish_config() -> dict[str, str]:
    config_path = PROJECT_ROOT / "publish.toml"
    if not config_path.exists():
        raise SystemExit(
            "publish.toml not found. "
            "Fill in the publish config before running this command."
        )

    if sys.version_info >= (3, 11):
        import tomllib
        with open(config_path, "rb") as f:
            raw = tomllib.load(f)
        return raw.get("publish", {})
    else:
        # Minimal flat parser for the specific publish.toml shape this project generates.
        # Handles only: key = "value" under a [publish] section.
        # Does not handle nesting, arrays, multiline, or other TOML features.
        result: dict[str, str] = {}
        in_publish = False
        for line in config_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line == "[publish]":
                in_publish = True
                continue
            if line.startswith("["):
                in_publish = False
                continue
            if in_publish and "=" in line:
                key, _, val = line.partition("=")
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                result[key] = val
        return result


def resolve_deploy_remote(config: dict[str, str]) -> str:
    if config.get("deploy_remote"):
        return config["deploy_remote"]
    user = config.get("user_handle", "")
    host = config.get("vm_host", "")
    project = config.get("project_name", "")
    if user and host and project:
        return f"{user}@{host}:/srv/git/{user}/{project}.git"
    raise SystemExit(
        "Cannot derive deploy_remote: user_handle, vm_host, or project_name is missing in publish.toml."
    )
```

Add the publish command implementations:

```python
def run_export_web() -> None:
    godot = detect_godot()
    env = ensure_local_home()
    build_dir = PROJECT_ROOT / "build" / "web"
    build_dir.mkdir(parents=True, exist_ok=True)
    result = run(
        [godot, "--headless", "--path", str(PROJECT_ROOT),
         "--export-release", "Web", str(build_dir / "index.html")],
        env=env,
    )
    if result.returncode != 0:
        raise SystemExit(
            "Web export failed. Check that a Web export preset exists in the project.\n"
            "Open Godot → Project → Export and verify the Web preset is configured."
        )
    print(f"Web export complete: {build_dir}")


def run_publish_check() -> None:
    config = load_publish_config()
    missing = [k for k in ("user_handle", "project_name", "vm_host", "public_url")
               if not config.get(k)]
    if missing:
        raise SystemExit(
            f"publish.toml is missing required fields: {', '.join(missing)}\n"
            "Fill them in before publishing."
        )

    build_dir = PROJECT_ROOT / "build" / "web"
    if not build_dir.exists():
        raise SystemExit(
            "build/web/ does not exist. Run `make export-web` first."
        )

    checks = {
        "index.html": list(build_dir.glob("index.html")),
        ".js file": list(build_dir.glob("*.js")),
        ".wasm file": list(build_dir.glob("*.wasm")),
        ".pck file": list(build_dir.glob("*.pck")),
    }
    missing_files = [name for name, found in checks.items() if not found]
    if missing_files:
        raise SystemExit(
            f"Web export is missing required files: {', '.join(missing_files)}\n"
            "Run `make export-web` to regenerate the export."
        )

    print("Publish check passed.")
    print(f"  public_url: {config.get('public_url')}")
    print(f"  deploy_remote: {resolve_deploy_remote(config)}")


def run_publish_init() -> None:
    build_dir = PROJECT_ROOT / "build" / "web"
    if not build_dir.exists():
        raise SystemExit("build/web/ does not exist. Run `make export-web` first.")

    config = load_publish_config()
    remote = resolve_deploy_remote(config)

    git_dir = build_dir / ".git"
    if not git_dir.exists():
        subprocess.run(["git", "init", "-b", "main", str(build_dir)], check=True)

    result = subprocess.run(
        ["git", "-C", str(build_dir), "remote", "get-url", "deploy"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        subprocess.run(
            ["git", "-C", str(build_dir), "remote", "add", "deploy", remote],
            check=True
        )
    else:
        existing = result.stdout.strip()
        if existing != remote:
            subprocess.run(
                ["git", "-C", str(build_dir), "remote", "set-url", "deploy", remote],
                check=True
            )

    print(f"Deploy repo initialized at build/web/")
    print(f"  remote: {remote}")


def run_publish() -> None:
    run_export_web()
    run_publish_check()
    run_publish_init()

    config = load_publish_config()
    build_dir = PROJECT_ROOT / "build" / "web"

    subprocess.run(["git", "-C", str(build_dir), "add", "--all"], check=True)

    status = subprocess.run(
        ["git", "-C", str(build_dir), "status", "--porcelain"],
        capture_output=True, text=True, check=True
    )

    if not status.stdout.strip():
        print("Nothing new to publish — build is already up to date.")
        print(f"Your game is live at: {config.get('public_url')}")
        return

    subprocess.run(
        ["git", "-C", str(build_dir), "commit", "-m", "Deploy web build"],
        check=True
    )

    result = subprocess.run(
        ["git", "-C", str(build_dir), "push", "deploy", "main"],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        raise SystemExit(
            f"Push failed.\n{result.stderr}\n"
            "Check your SSH key and deploy remote configuration."
        )

    print(f"\nYour game is live at: {config.get('public_url')}")


def run_publish_info() -> None:
    config = load_publish_config()
    print(f"public_url:     {config.get('public_url', '(not set)')}")
    print(f"deploy_remote:  {resolve_deploy_remote(config)}")
    print(f"deploy_folder:  {PROJECT_ROOT / 'build' / 'web'}")


def run_publish_status() -> None:
    config_path = PROJECT_ROOT / "publish.toml"
    build_dir = PROJECT_ROOT / "build" / "web"
    git_dir = build_dir / ".git"

    config_ok = config_path.exists()
    export_ok = (build_dir / "index.html").exists()
    repo_ok = git_dir.exists()

    try:
        config = load_publish_config() if config_ok else {}
        url = config.get("public_url", "(not set)")
    except SystemExit:
        url = "(could not read)"

    print(f"config:       {'✓' if config_ok else '✗'} publish.toml")
    print(f"export:       {'✓' if export_ok else '✗'} build/web/index.html")
    print(f"deploy_repo:  {'✓' if repo_ok else '✗'} build/web/.git")
    print(f"public_url:   {url}")
```

Add dispatch cases in `main()`:

```python
elif args.command == "export-web":
    run_export_web()
elif args.command == "publish-check":
    run_publish_check()
elif args.command == "publish-init":
    run_publish_init()
elif args.command == "publish":
    run_publish()
elif args.command == "publish-info":
    run_publish_info()
elif args.command == "publish-status":
    run_publish_status()
```

### 5. Kaya Playbook — add publish handoff

Add to `learning/kaya/Playbook.md` in the platform repo:

```markdown
## When the Student Wants to Publish

The student may say: "publish my game", "put this online", "give me a link"

This is a filesystem operation. Hand it to the Dev.

Say: "Let's get our Dev to publish it. Here's what to send them."

Envelope:
--- START: PM TO DEV ---
The student wants to publish the game.
Read publish.toml.
If any required fields are empty, ask for only those values.
Then run `make publish` or `python3 scripts/project_tasks.py publish`.
Report back with the live URL when done.
--- END: PM TO DEV ---

If publish.toml does not exist yet, tell the student:
"We need to set up your publish config first.
Our Dev will ask you for a few details — your handle, project name,
and the server address."
```

### 6. Generated publish docs

Add a short `docs/PUBLISHING.md` to generated projects:

```markdown
# Publishing Your Game

Say "publish my game" to Kaya. She will handle it.

## What Happens

1. Kaya asks the Dev to publish.
2. The Dev exports the game for the web.
3. The Dev pushes the export to your hosting server.
4. You get a live URL.

## Configuration

Edit `publish.toml` with your project details.
Required fields:
- `user_handle` — your username on the server
- `project_name` — your project name
- `vm_host` — the server address
- `public_url` — the public URL for your game

## Source vs Deploy

Your source code lives in this repo.
Your live game comes from `build/web/`, which is a separate deploy working copy.
Only exported web files are pushed live — not your source code.

## Commands (if you need them directly)

- `make export-web` — export the game for the web
- `make publish-check` — verify the export is ready
- `make publish` — export and publish in one step
- `make publish-status` — check current publish readiness
- `make publish-info` — show your public URL and deploy config
```

---

## Implementation Order

1. Add `build/` to generated `.gitignore` — one line, lowest risk
2. Add `publish.toml` template to generator
3. Add `load_publish_config()` and `resolve_deploy_remote()` to `project_tasks.py`
4. Add all six publish commands to `project_tasks.py`
5. Add publish targets to generated `Makefile`
6. Add publish handoff to platform `learning/kaya/Playbook.md`
7. Add generated `docs/PUBLISHING.md` to generator
8. Verify: fresh generated project contains all publish artifacts
9. Verify: `make publish-check` fails correctly when config is empty
10. Verify: `make publish-status` shows correct readiness state

---

## Out of Scope for v1

- VM provisioning
- Automatic bare repo creation on server
- Automatic Nginx route creation
- Automatic SSH key provisioning
- Any student-visible Git mechanics

---

## Test Acceptance

- Fresh generated project contains `publish.toml`, `docs/PUBLISHING.md`, publish Make targets
- `make publish-check` prints clear failure when config fields are empty
- `make publish-check` prints clear failure when `build/web/` is missing
- `make publish-status` accurately reports all four readiness states
- `make publish-info` shows expected values from a filled `publish.toml`
- Parent source repo `.gitignore` excludes `build/`
- `load_publish_config()` works correctly on Python 3.9 and 3.11+
- Student asking Kaya to publish results in a correct Dev envelope, not a direct Dev instruction
