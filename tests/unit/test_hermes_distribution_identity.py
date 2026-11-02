"""The fork must never query or upgrade the upstream PyPI distribution."""
import importlib.metadata
import io
import json

from browser_harness import admin, telemetry


NAME = "browser-harness-hermes-compat"


def test_version_readers_use_compat_distribution_not_upstream(monkeypatch):
    versions = {NAME: "0.1.13.post1", "browser-harness": "9.9.9"}
    monkeypatch.setattr(importlib.metadata, "version", versions.__getitem__)
    monkeypatch.setattr(telemetry, "version", versions.__getitem__)
    assert admin._version() == "0.1.13.post1"
    assert telemetry._version() == "0.1.13.post1"


def test_update_lookup_queries_only_the_compat_registry_project(tmp_path, monkeypatch):
    calls = []

    def request(url, timeout):
        calls.append(url)
        return io.BytesIO(json.dumps({"info": {"version": "0.1.14"}}).encode())

    monkeypatch.setattr(admin, "VERSION_CACHE", tmp_path / "compat-cache.json")
    monkeypatch.setattr(admin.urllib.request, "urlopen", request)
    assert admin._latest_release_tag(force=True) == "0.1.14"
    assert calls == [f"https://pypi.org/pypi/{NAME}/json"]
