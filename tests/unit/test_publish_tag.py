"""Exercise release identity and ancestry against actual local Git objects."""
import importlib.util
from pathlib import Path
import subprocess

import pytest


spec = importlib.util.spec_from_file_location("verify_pypi_tag", Path(__file__).parents[2] / "scripts/verify_pypi_tag.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
TAG = "pypi-v0.1.13.post1"
BRANCH = "refs/heads/maintained"


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "--quiet")
    git(tmp_path, "config", "user.name", "Fixture")
    git(tmp_path, "config", "user.email", "fixture@example.invalid")
    (tmp_path / "pyproject.toml").write_text('[project]\nname="browser-harness-hermes-compat"\nversion="0.1.13.post1"\n')
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "--quiet", "-m", "initial")
    git(tmp_path, "tag", "-a", TAG, "-m", "release")
    git(tmp_path, "branch", "maintained")
    return tmp_path


def test_accepts_matching_annotated_tag_and_reachable_checked_out_commit(repo):
    sha = git(repo, "rev-parse", "HEAD")
    assert module.verify(repo, TAG, sha, BRANCH) == {
        "project": "browser-harness-hermes-compat", "version": "0.1.13.post1", "commit": sha,
    }


def test_rejects_official_project_namespace(repo):
    (repo / "pyproject.toml").write_text('[project]\nname="browser-harness"\nversion="0.1.13.post1"\n')
    with pytest.raises(ValueError, match="project name"):
        module.verify(repo, TAG, git(repo, "rev-parse", "HEAD"), BRANCH)


def test_rejects_wrong_version_tag(repo):
    with pytest.raises(ValueError, match="tag/version"):
        module.verify(repo, "pypi-v9.9.9", git(repo, "rev-parse", "HEAD"), BRANCH)


def test_rejects_lightweight_tag(repo):
    git(repo, "tag", "-d", TAG)
    git(repo, "tag", TAG)
    with pytest.raises(ValueError, match="annotated"):
        module.verify(repo, TAG, git(repo, "rev-parse", "HEAD"), BRANCH)


def test_rejects_tag_event_checkout_mismatch(repo):
    sha = git(repo, "rev-parse", "HEAD")
    git(repo, "commit", "--quiet", "--allow-empty", "-m", "later")
    with pytest.raises(ValueError, match="checked-out commit"):
        module.verify(repo, TAG, sha, BRANCH)


def test_rejects_commit_outside_maintained_branch(repo):
    git(repo, "commit", "--quiet", "--allow-empty", "-m", "unreviewed")
    git(repo, "tag", "-d", TAG)
    git(repo, "tag", "-a", TAG, "-m", "unreviewed release")
    with pytest.raises(ValueError, match="maintained branch"):
        module.verify(repo, TAG, git(repo, "rev-parse", "HEAD"), BRANCH)


def test_rejects_dirty_publish_checkout(repo):
    (repo / "unexpected.txt").write_text("dirty")
    with pytest.raises(ValueError, match="clean"):
        module.verify(repo, TAG, git(repo, "rev-parse", "HEAD"), BRANCH)
