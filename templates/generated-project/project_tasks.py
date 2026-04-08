#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
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
        choices=["doctor", "smoke", "test", "verify", "ci-verify", "play", "editor", "setup-hooks", "tts", "tts-test"],
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


def print_doctor() -> None:
    ensure_safe_directory()

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
    print("notes:")
    print("- use this script when make is unavailable")
    print("- git safe.directory is repaired automatically when possible")
    print("- Godot commands use a project-local writable home automatically")


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


if __name__ == "__main__":
    main()
