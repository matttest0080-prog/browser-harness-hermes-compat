"""Fail-closed preflight for the independent distribution's publish workflow."""
from pathlib import Path
import argparse
import json
import re
import subprocess
import tomllib


NAME = "browser-harness-hermes-compat"


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def verify(repo: Path, tag: str, sha: str, branch_ref: str) -> dict:
    project = tomllib.loads((repo / "pyproject.toml").read_text())["project"]
    if project["name"] != NAME or tag != f"pypi-v{project['version']}":
        raise ValueError("independent project name or release tag/version mismatch")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("invalid GitHub event SHA")
    if git(repo, "cat-file", "-t", tag) != "tag":
        raise ValueError("release tag must be annotated")
    commit = git(repo, "rev-parse", f"{tag}^{{commit}}")
    if commit != git(repo, "rev-parse", f"{sha}^{{commit}}") or commit != git(repo, "rev-parse", "HEAD"):
        raise ValueError("tag, event and checked-out commit must agree")
    ancestor = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", commit, branch_ref], check=False)
    if ancestor.returncode != 0:
        raise ValueError("tag is not reachable from the maintained branch")
    if git(repo, "status", "--porcelain"):
        raise ValueError("publish checkout must be clean")
    return {"project": NAME, "version": project["version"], "commit": commit}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag")
    parser.add_argument("sha")
    parser.add_argument("branch_ref")
    args = parser.parse_args()
    print(json.dumps(verify(Path.cwd(), args.tag, args.sha, args.branch_ref)))
