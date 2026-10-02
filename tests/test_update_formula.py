import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "update_formula", ROOT / "scripts/update_formula.py"
)
UPDATER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UPDATER)


class ReleaseUpdateTests(unittest.TestCase):
    def test_known_releases_preserve_formula_behavior(self):
        for formula, version, checksums in (
            ("mls", "1.2.3", {"aarch64_sha256": "a" * 64, "x86_64_sha256": "b" * 64}),
            ("nalcos", "2.0.0-alpha.1", {"aarch64_sha256": "c" * 64}),
        ):
            with (
                self.subTest(formula=formula),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                (root / "Formula").mkdir()
                path = root / "Formula" / f"{formula}.rb"
                original = (ROOT / "Formula" / f"{formula}.rb").read_text()
                path.write_text(original)
                result = UPDATER.update_from_event(
                    {
                        "action": f"{formula}-release",
                        "client_payload": {"version": version, **checksums},
                    },
                    root,
                )
                self.assertEqual(result, (formula, version))
                updated = path.read_text()
                self.assertIn(f'version "{version}"', updated)
                for checksum in checksums.values():
                    self.assertIn(f'sha256 "{checksum}"', updated)
                self.assertEqual(
                    [
                        line
                        for line in original.splitlines()
                        if not line.strip().startswith(("version ", "sha256 "))
                    ],
                    [
                        line
                        for line in updated.splitlines()
                        if not line.strip().startswith(("version ", "sha256 "))
                    ],
                )

    def test_invalid_payloads_do_not_modify_formula(self):
        valid = {
            "version": "1.2.3",
            "aarch64_sha256": "a" * 64,
            "x86_64_sha256": "b" * 64,
        }
        events = [
            {"action": "../../unknown-release", "client_payload": valid},
            {
                "action": "mls-release",
                "client_payload": {**valid, "version": '1.2.3"; system("bad")'},
            },
            {
                "action": "mls-release",
                "client_payload": {**valid, "aarch64_sha256": "a" * 64 + "\n"},
            },
            {
                "action": "mls-release",
                "client_payload": {**valid, "x86_64_sha256": None},
            },
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Formula").mkdir()
            path = root / "Formula/mls.rb"
            original = (ROOT / "Formula/mls.rb").read_text()
            path.write_text(original)
            for event in events:
                with self.subTest(event=event), self.assertRaises(ValueError):
                    UPDATER.update_from_event(event, root)
                self.assertEqual(path.read_text(), original)

    def test_unexpected_layout_is_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Formula").mkdir()
            path = root / "Formula/mls.rb"
            original = '  version "1.0.0"\n  sha256 "old"\n'
            path.write_text(original)
            with self.assertRaisesRegex(ValueError, "layout"):
                UPDATER.update_from_event(
                    {
                        "action": "mls-release",
                        "client_payload": {
                            "version": "1.2.3",
                            "aarch64_sha256": "a" * 64,
                            "x86_64_sha256": "b" * 64,
                        },
                    },
                    root,
                )
            self.assertEqual(path.read_text(), original)


if __name__ == "__main__":
    unittest.main()
