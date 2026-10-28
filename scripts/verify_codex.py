#!/usr/bin/env python3
"""Offline structural smoke test of the Codex port (Python >= 3.9, stdlib only)."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "rodokmen"
REQUIRED = [
    "SKILL.md", "VERZE", "tools/novy_projekt.py",
    "tools/kontrola.py", "tools/aron_search.py",
    "reference/data.md", "reference/matriky.md", "reference/portaly.md",
    "reference/soukromi.md", "reference/web.md",
    "template/AGENTS.md", "template/.codex/config.toml",
    "template/.codex/agents/matrika-reader.toml",
    "template/.codex/agents/matrika-verifier.toml",
    "template/web/package.json", "template/web/package-lock.json",
    "template/ukazka/osoby.py", "template/ukazka_vyrezy/ukazka_krest_jan_novak_1890.jpg",
]


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run() -> None:
    for rel in REQUIRED:
        check((SKILL / rel).is_file(), "Missing " + rel)
    check((ROOT / "AGENTS.md").is_file(), "Missing root AGENTS.md")
    check((ROOT / "README.md").is_file(), "Missing README.md")
    check((ROOT / "LICENSE").is_file(), "Missing original MIT attribution")

    manifest = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    check(manifest.startswith("---\nname: rodokmen\n"), "Skill front matter invalid")
    check("$rodokmen" in manifest and "AGENTS.md" in manifest, "No Codex references")

    # Do not ship commands requiring the older, incompatible agent runtime.
    old_name = "Cl" + "aude"
    for f in ROOT.rglob("*"):
        if not f.is_file() or any(p in f.parts for p in (".git", "__pycache__")):
            continue
        if f.suffix.lower() not in {".md", ".py", ".toml", ".yaml", ".yml", ".json", ".sh"}:
            continue
        body = f.read_text(encoding="utf-8")
        check(old_name.lower() not in body.lower(), "Legacy runtime reference in " + str(f))
        if f.suffix == ".py":
            ast.parse(body, filename=str(f))
        if f.suffix == ".json":
            json.loads(body)
        if f.suffix == ".toml" and sys.version_info >= (3, 11):
            import tomllib
            tomllib.loads(body)

    with tempfile.TemporaryDirectory(prefix="rodokmen-smoke-") as folder:
        root = Path(folder)
        init = SKILL / "tools" / "novy_projekt.py"
        for name, is_demo in (("normal", False), ("demo", True)):
            dest = root / name
            cmd = [sys.executable, "-I", "-X", "utf8", str(init), str(dest)]
            if is_demo:
                cmd.append("--ukazka")
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for rel in (
                "AGENTS.md", ".skill_verze", ".codex/config.toml",
                ".codex/agents/matrika-verifier.toml", "data/STAV.md",
                "tools/kontrola.py", "web/package.json", "pracovni", "dokumenty",
            ):
                check((dest / rel).exists(), f"{name} missing {rel}")
            check(
                (dest / ".skill_verze").read_text(encoding="utf-8") ==
                (SKILL / "VERZE").read_text(encoding="utf-8"),
                "Version marker mismatch",
            )
            check(not (dest / (old_name.upper() + ".md")).exists(), "Legacy project file generated")
            check(not (dest / ("." + old_name.lower())).exists(), "Legacy project folder generated")
            if is_demo:
                check((dest / "vyrezy" / "ukazka_krest_jan_novak_1890.jpg").is_file(), "Demo image missing")
                check((dest / "data" / "osoby.py").stat().st_size > 10000, "Sample data missing")
            else:
                state = dest / "data" / "STAV.md"
                state.write_text("STAV BEZE ZMENY\n", encoding="utf-8")
                agent = dest / "AGENTS.md"
                agent.write_text("VLASTNI PRAVIDLA\n", encoding="utf-8")
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                check(state.read_text(encoding="utf-8") == "STAV BEZE ZMENY\n", "State overwritten")
                check(agent.read_text(encoding="utf-8") == "VLASTNI PRAVIDLA\n", "AGENTS overwritten")

    print("OK: Codex skill, metadata, 2 project initializations, syntax, privacy checks")


if __name__ == "__main__":
    run()
