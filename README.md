# Homebrew tap

Homebrew formulae for tools by [Pushkar](https://github.com/thepushkarp).

## Install

```bash
brew tap thepushkarp/tap
```

| Tool | Install | Supported platform |
| --- | --- | --- |
| [MLS](https://github.com/thepushkarp/mls) — terminal media browser | `brew install thepushkarp/tap/mls` | Apple Silicon and Intel macOS |
| [NaLCoS](https://github.com/thepushkarp/nalcos) — local Git history search | `brew install thepushkarp/tap/nalcos` | Apple Silicon macOS |

MLS installs `ffmpeg` and `mpv` for metadata probing and playback. For safe delete functionality in triage mode, optionally install `trash`:

```bash
brew install trash
```

NaLCoS installs Git. Run `nalcos init` inside a repository to install its default MiniLM INT8 CPU embedding model and index the history. Models use Hugging Face's shared cache and are downloaded during setup, not by Homebrew. See the [NaLCoS documentation](https://github.com/thepushkarp/nalcos#readme) for configuration and lexical-only search.

## Update

```bash
brew update
brew upgrade mls nalcos
```

## Release updates

The update workflow accepts repository dispatch events with a version (without a `v` prefix) and SHA-256 checksums for published release archives:

| Event | Required `client_payload` fields |
| --- | --- |
| `mls-release` | `version`, `aarch64_sha256`, `x86_64_sha256` |
| `nalcos-release` | `version`, `aarch64_sha256` |

The updater validates the event, version, and checksums before changing the selected formula. Formula syntax and runtime dependencies are checked before committing the update. Concurrent releases run independently; when another update wins the push, the workflow regenerates its formula on the latest `main` and retries up to five times without force-pushing. Release assets must already be available at the formula's GitHub release URLs.
