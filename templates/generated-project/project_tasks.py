#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run generated-project tasks without depending on make.")
    parser.add_argument(
        "command",
        choices=[
            "doctor",
            "smoke",
            "test",
            "verify",
            "ci-verify",
            "play",
            "editor",
            "setup-hooks",
            "tts",
            "tts-test",
            "export-web",
            "publish-check",
            "publish-init",
            "publish",
            "publish-info",
            "publish-status",
        ],
    )
    parser.add_argument("tts_text", nargs="*", help="Optional text for the tts command")
    parser.add_argument("--voice", default=os.environ.get("VOICE", "af_bella"), help="Voice id for the tts command")
    return parser.parse_args()


def ensure_local_home() -> dict[str, str]:
    home = PROJECT_ROOT / ".home"
    data_home = home / ".local" / "share"
    config_home = home / ".config"
    roaming = home / "AppData" / "Roaming"
    local = home / "AppData" / "Local"
    for path in (home, data_home, config_home, roaming, local):
        path.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["XDG_DATA_HOME"] = str(data_home)
    env["XDG_CONFIG_HOME"] = str(config_home)
    env["APPDATA"] = str(roaming)
    env["LOCALAPPDATA"] = str(local)
    env["USERPROFILE"] = str(home)
    return env


def run(command: list[str], *, env: dict[str, str] | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=capture,
        check=False,
    )


def require_success(result: subprocess.CompletedProcess[str], context: str) -> None:
    if result.returncode == 0:
        return
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    raise SystemExit(f"{context} failed with exit code {result.returncode}")


def detect_godot() -> str:
    override = os.environ.get("GODOT_BIN")
    if override and Path(override).exists():
        return override

    for candidate in ("godot", "godot4"):
        found = shutil.which(candidate)
        if found:
            return found

    candidates = [
        Path("/Applications/Godot.app/Contents/MacOS/Godot"),
        Path("/Applications/Godot_mono.app/Contents/MacOS/Godot"),
    ]

    program_files = os.environ.get("PROGRAMFILES")
    program_files_x86 = os.environ.get("PROGRAMFILES(X86)")
    local_app_data = os.environ.get("LOCALAPPDATA")
    for base in (program_files, program_files_x86, local_app_data):
        if not base:
            continue
        root = Path(base)
        candidates.extend(
            [
                root / "Godot" / "Godot.exe",
                root / "Programs" / "Godot" / "Godot.exe",
            ]
        )
        candidates.extend(sorted(root.glob("Godot*/*.exe")))

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    raise SystemExit(
        "Godot was not found. Install Godot or set GODOT_BIN to the executable path, then retry."
    )


def ensure_safe_directory() -> None:
    result = run(["git", "-C", str(PROJECT_ROOT), "status", "--short"], capture=True)
    combined = "\n".join(filter(None, [result.stdout, result.stderr])).lower()
    if "dubious ownership" not in combined:
        return

    safe_path = PROJECT_ROOT.as_posix()
    fix = run(["git", "config", "--global", "--add", "safe.directory", safe_path], capture=True)
    require_success(fix, "git safe.directory repair")


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def load_publish_config() -> dict[str, str]:
    config_path = PROJECT_ROOT / "publish.toml"
    if not config_path.exists():
        raise SystemExit(
            "publish.toml not found. "
            "Fill in the publish config before running this command."
        )

    if sys.version_info >= (3, 11):
        import tomllib

        with open(config_path, "rb") as handle:
            raw = tomllib.load(handle)
        section = raw.get("publish", {})
        if not isinstance(section, dict):
            return {}
        return {str(key): "" if value is None else str(value) for key, value in section.items()}

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
            key, _, value = line.partition("=")
            result[key.strip()] = value.strip().strip('"').strip("'")
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


def detect_godot_version(godot_bin: str) -> str | None:
    result = run([godot_bin, "--version"], capture=True)
    version_text = "\n".join(filter(None, [result.stdout, result.stderr])).strip()
    match = re.search(r"(\d+\.\d+(?:\.\d+)?\.[A-Za-z0-9]+)", version_text)
    return match.group(1) if match else None


def export_templates_root_from_env(env: dict[str, str]) -> Path:
    if sys.platform == "darwin":
        home = env.get("HOME")
        if home:
            return Path(home) / "Library" / "Application Support" / "Godot" / "export_templates"
        return Path.home() / "Library" / "Application Support" / "Godot" / "export_templates"

    if os.name == "nt":
        appdata = env.get("APPDATA")
        if appdata:
            return Path(appdata) / "Godot" / "export_templates"
        userprofile = env.get("USERPROFILE")
        if userprofile:
            return Path(userprofile) / "AppData" / "Roaming" / "Godot" / "export_templates"
        return Path.home() / "AppData" / "Roaming" / "Godot" / "export_templates"

    xdg_data_home = env.get("XDG_DATA_HOME")
    if xdg_data_home:
        return Path(xdg_data_home) / "godot" / "export_templates"

    home = env.get("HOME")
    if home:
        return Path(home) / ".local" / "share" / "godot" / "export_templates"
    return Path.home() / ".local" / "share" / "godot" / "export_templates"


def export_templates_root() -> Path:
    return export_templates_root_from_env(os.environ)


def inspect_web_export_templates(godot_bin: str, env: dict[str, str] | None = None) -> tuple[bool, str]:
    version = detect_godot_version(godot_bin)
    if not version:
        return False, "unknown (could not determine the Godot version for export template lookup)"

    template_dir = export_templates_root_from_env(env or os.environ) / version
    required = ("web_release.zip", "web_nothreads_release.zip")
    missing = [name for name in required if not (template_dir / name).exists()]
    if missing:
        return (
            False,
            f"missing in {template_dir} (required: {', '.join(missing)})",
    )
    return True, f"ready in {template_dir}"


def bootstrap_export_templates(godot_bin: str, env: dict[str, str]) -> None:
    version = detect_godot_version(godot_bin)
    if not version:
        print("bootstrap_export_templates: could not detect Godot version, skipping")
        return

    global_dir = export_templates_root() / version
    local_dir = export_templates_root_from_env(env) / version

    required = ["web_release.zip", "web_nothreads_release.zip"]

    missing_locally = [filename for filename in required if not (local_dir / filename).exists()]
    if not missing_locally:
        return

    missing_globally = [filename for filename in missing_locally if not (global_dir / filename).exists()]
    if missing_globally:
        print(
            f"Export templates not found locally or globally for {version}.\n"
            "Install Godot export templates before publishing."
        )
        return

    local_dir.mkdir(parents=True, exist_ok=True)
    for filename in missing_locally:
        shutil.copy2(global_dir / filename, local_dir / filename)
    print(f"Bootstrapped export templates into project-local .home ({len(missing_locally)} file(s) copied)")


def print_doctor() -> None:
    ensure_safe_directory()
    env = ensure_local_home()

    print(f"project_root: {PROJECT_ROOT}")
    print(f"python: {sys.executable}")
    print(f"git: {shutil.which('git') or 'missing'}")
    print(f"make: {shutil.which('make') or 'missing'}")

    try:
        godot = detect_godot()
    except SystemExit as exc:
        print(f"godot: missing ({exc})")
        return

    print(f"godot: {godot}")
    print(f"local_home: {PROJECT_ROOT / '.home'}")
    preset_path = PROJECT_ROOT / "export_presets.cfg"
    print(f"web_export_preset: {'present' if preset_path.exists() else 'missing'}")
    templates_ok, templates_status = inspect_web_export_templates(godot, env)
    print(f"web_export_templates: {templates_status}")
    print("notes:")
    print("- use this script when make is unavailable")
    print("- git safe.directory is repaired automatically when possible")
    print("- Godot commands use a project-local writable home automatically")
    if not preset_path.exists():
        print("- export_presets.cfg is missing; copy the platform Web export preset into this project before using make export-web")
    if not templates_ok:
        print("- publish/export uses the project-local .home path shown above, not the global Godot template folder")
        print("- install or copy the matching Godot export templates into the folder shown above, then retry web export")
        print("- manual install: download the matching export_templates .tpz, extract it, and copy templates/ into the project-local export_templates folder")


def find_fixmes() -> list[tuple[Path, int, str]]:
    findings: list[tuple[Path, int, str]] = []
    for path in PROJECT_ROOT.rglob("*.gd"):
        if any(part in {".git", "node_modules"} for part in path.parts):
            continue
        for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "FIXME" in line:
                findings.append((path, index, line))
    return findings


def run_smoke() -> None:
    ensure_safe_directory()
    godot = detect_godot()
    env = ensure_local_home()
    require_success(
        run([godot, "--headless", "--path", str(PROJECT_ROOT), "--editor", "--quit-after", "1"], env=env),
        "smoke",
    )


def run_test() -> None:
    ensure_safe_directory()
    godot = detect_godot()
    env = ensure_local_home()
    require_success(
        run([godot, "--headless", "--path", str(PROJECT_ROOT), "--import", "--quit"], env=env),
        "asset import",
    )
    require_success(
        run(
            [
                godot,
                "--headless",
                "-d",
                "-s",
                "--path",
                str(PROJECT_ROOT),
                "addons/gut/gut_cmdln.gd",
                "-gconfig=res://.gutconfig.json",
                "-gexit",
            ],
            env=env,
        ),
        "test",
    )


def run_verify() -> None:
    run_test()
    run_smoke()
    print("Verification passed.")


def run_ci_verify() -> None:
    run_test()
    run_smoke()
    print("[ci] Checking for FIXME markers...")
    findings = find_fixmes()
    if findings:
        for path, line_number, line in findings:
            rel = path.relative_to(PROJECT_ROOT)
            print(f"{rel}:{line_number}:{line}")
        raise SystemExit("[ci] FIXME found in gameplay files")
    print("[ci] Full verification passed.")


def run_play() -> None:
    run_verify()
    godot = detect_godot()
    env = ensure_local_home()
    require_success(run([godot, "--path", str(PROJECT_ROOT)], env=env), "play")


def run_editor() -> None:
    ensure_safe_directory()
    godot = detect_godot()
    env = ensure_local_home()
    require_success(run([godot, "--editor", "--path", str(PROJECT_ROOT)], env=env), "editor")


def run_setup_hooks() -> None:
    ensure_safe_directory()
    hooks_dir = PROJECT_ROOT / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    src = PROJECT_ROOT / "scripts" / "hooks" / "pre-commit.sh"
    dst = hooks_dir / "pre-commit"
    shutil.copy2(src, dst)
    dst.chmod(dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print("Pre-commit hook installed.")


def run_tts(text: str, voice: str) -> None:
    script = PROJECT_ROOT / "scripts" / "kaya_tts.sh"
    if not script.exists():
        raise SystemExit(f"TTS helper not found: {script}")
    require_success(run([str(script), text], env={**os.environ, "VOICE": voice}), "tts")


def require_publish_key(config: dict[str, str]) -> Path:
    raw_path = config.get("ssh_key_path", "").strip()
    if not raw_path:
        raise SystemExit("publish.toml is missing required field: ssh_key_path\nFill it in before publishing.")

    key_path = Path(os.path.expandvars(os.path.expanduser(raw_path)))
    if not key_path.is_absolute():
        key_path = (PROJECT_ROOT / key_path).resolve()
    if not key_path.exists():
        raise SystemExit(
            f"SSH deploy key not found: {raw_path}\n"
            "Check ssh_key_path in publish.toml and make sure the key file exists."
        )
    return key_path


def run_export_web() -> None:
    godot = detect_godot()
    env = ensure_local_home()
    bootstrap_export_templates(godot, env)
    build_dir = PROJECT_ROOT / "build" / "web"
    build_dir.mkdir(parents=True, exist_ok=True)
    result = run(
        [
            godot,
            "--headless",
            "--path",
            str(PROJECT_ROOT),
            "--export-release",
            "Web",
            str(build_dir / "index.html"),
        ],
        env=env,
    )
    if result.returncode != 0:
        raise SystemExit(
            "Web export failed. Check that a Web export preset exists in the project.\n"
            "Open Godot -> Project -> Export and verify the Web preset is configured."
        )
    print(f"Web export complete: {build_dir}")


def run_publish_check() -> None:
    config = load_publish_config()
    missing = [
        key
        for key in ("user_handle", "project_name", "vm_host", "public_url")
        if not config.get(key, "").strip()
    ]
    if missing:
        raise SystemExit(
            f"publish.toml is missing required fields: {', '.join(missing)}\n"
            "Fill them in before publishing."
        )

    build_dir = PROJECT_ROOT / "build" / "web"
    if not build_dir.exists():
        raise SystemExit("build/web/ does not exist. Run `make export-web` first.")

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
    key_path = require_publish_key(config)

    if not (build_dir / ".git").exists():
        subprocess.run(["git", "init", "-b", "main", str(build_dir)], check=True)

    remote_result = subprocess.run(
        ["git", "-C", str(build_dir), "remote", "get-url", "deploy"],
        text=True,
        capture_output=True,
        check=False,
    )
    if remote_result.returncode != 0:
        subprocess.run(["git", "-C", str(build_dir), "remote", "add", "deploy", remote], check=True)
    else:
        existing = remote_result.stdout.strip()
        if existing != remote:
            subprocess.run(["git", "-C", str(build_dir), "remote", "set-url", "deploy", remote], check=True)

    ssh_command = f"ssh -i {shlex.quote(str(key_path))} -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
    subprocess.run(
        ["git", "-C", str(build_dir), "config", "core.sshCommand", ssh_command],
        check=True,
    )

    print("Deploy repo initialized at build/web/")
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
        text=True,
        capture_output=True,
        check=True,
    )

    if not status.stdout.strip():
        print("Nothing new to publish - build is already up to date.")
        print(f"Your game is live at: {config.get('public_url')}")
        return

    subprocess.run(["git", "-C", str(build_dir), "commit", "-m", "Deploy web build"], check=True)
    result = subprocess.run(
        ["git", "-C", str(build_dir), "push", "--force", "deploy", "main"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"Push failed.\n{result.stderr}\n"
            "Check your SSH key and deploy remote configuration."
        )

    print(f"Your game is live at: {config.get('public_url')}")


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


def main() -> None:
    args = parse_args()
    if args.command == "doctor":
        print_doctor()
    elif args.command == "smoke":
        run_smoke()
    elif args.command == "test":
        run_test()
    elif args.command == "verify":
        run_verify()
    elif args.command == "ci-verify":
        run_ci_verify()
    elif args.command == "play":
        run_play()
    elif args.command == "editor":
        run_editor()
    elif args.command == "setup-hooks":
        run_setup_hooks()
    elif args.command == "tts":
        text = " ".join(args.tts_text).strip() or "Hello, this is a live TTS test from Kaya."
        run_tts(text, args.voice)
    elif args.command == "tts-test":
        run_tts("Hello, this is a live TTS test from Kaya.", args.voice)
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


if __name__ == "__main__":
    main()
