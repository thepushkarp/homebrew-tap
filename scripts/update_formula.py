"""Update a known formula from a repository_dispatch release payload."""

import json
import os
import re
from pathlib import Path

RELEASES = {
    "mls-release": ("mls", ("aarch64_sha256", "x86_64_sha256")),
    "nalcos-release": ("nalcos", ("aarch64_sha256",)),
}
VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?")
SHA256 = re.compile(r"[0-9a-fA-F]{64}")


def version_key(version):
    if not VERSION.fullmatch(version):
        raise ValueError(f"unsupported formula version: {version!r}")
    core, separator, prerelease = version.partition("-")
    identifiers = tuple(
        (0, int(part)) if part.isdigit() else (1, part)
        for part in prerelease.split(".")
    )
    return (*map(int, core.split(".")), 0 if separator else 1, identifiers)


def update_from_event(event, root):
    action = event.get("action")
    if action not in RELEASES:
        raise ValueError(f"unsupported release event: {action!r}")
    formula, keys = RELEASES[action]
    payload = event.get("client_payload", {})
    version = payload.get("version")
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        raise ValueError(
            "version must be a numeric major.minor.patch with an optional prerelease suffix"
        )
    checksums = [payload.get(key) for key in keys]
    for key, checksum in zip(keys, checksums):
        if not isinstance(checksum, str) or not SHA256.fullmatch(checksum):
            raise ValueError(f"{key} must contain exactly 64 hexadecimal characters")

    path = root / "Formula" / f"{formula}.rb"
    source = path.read_text()
    versions = re.findall(r'^  version "([^"]*)"$', source, flags=re.MULTILINE)
    checksum_iter = iter(checksums)
    # Formula checksum order follows its architecture blocks: ARM first, then Intel.
    pattern = r'^(\s+)sha256 "[^"]*"$'
    if len(versions) != 1 or len(
        re.findall(pattern, source, flags=re.MULTILINE)
    ) != len(checksums):
        raise ValueError(f"unexpected version or checksum layout in {path}")
    current = versions[0]
    # Delayed dispatches must not overwrite newer releases after a push retry.
    if version_key(version) < version_key(current):
        return formula, current
    if version_key(version) == version_key(current):
        existing = re.findall(r'^\s+sha256 "([^"]*)"$', source, flags=re.MULTILINE)
        if [value.lower() for value in existing] != [
            value.lower() for value in checksums
        ]:
            raise ValueError(f"conflicting checksums for published {formula} {current}")
        return formula, current
    source = re.sub(
        r'^  version "[^"]*"$', f'  version "{version}"', source, flags=re.MULTILINE
    )
    source = re.sub(
        pattern,
        lambda match: f'{match[1]}sha256 "{next(checksum_iter).lower()}"',
        source,
        flags=re.MULTILINE,
    )
    path.write_text(source)
    return formula, version


def main():
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    formula, version = update_from_event(event, Path.cwd())
    if output := os.environ.get("GITHUB_OUTPUT"):
        with Path(output).open("a") as handle:
            handle.write(f"formula={formula}\nversion={version}\n")
    print(f"Selected {formula} {version}")


if __name__ == "__main__":
    main()
