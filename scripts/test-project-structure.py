#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from unittest import mock
from pathlib import Path
from urllib.parse import parse_qs, urlparse


SCRIPT = Path(__file__).resolve().parent / "project-structure.py"
SPEC = importlib.util.spec_from_file_location("project_structure", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Cannot import project-structure.py")
project_structure = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(project_structure)


def base_map(status: str = "provisional") -> dict:
    value = {
        "schema_version": 1,
        "status": status,
        "project_name": "Fixture Project",
        "verified_at": None,
        "verified_by": None,
        "ignore_file": ".ai-workflow/directory-map.ignore",
        "nodes": [
            {
                "path": ".ai-workflow",
                "kind": "directory",
                "role": "Workflow state and structure contracts",
                "boundaries": ["Do not store secrets"],
                "task_types": ["Workflow maintenance"],
            },
            {
                "path": "src",
                "kind": "directory",
                "role": "Application source",
                "boundaries": ["Do not store secrets"],
                "task_types": ["Feature implementation"],
            },
            {
                "path": "docs",
                "kind": "directory",
                "role": "Generated project documentation",
                "boundaries": [],
                "task_types": ["Documentation"],
            }
        ],
        "conventions": [{"pattern": "README.md", "role": "Project guide"}],
    }
    if status == "verified":
        value["verified_at"] = "2026-06-20T00:00:00Z"
        value["verified_by"] = "User"
    return value


class Fixture:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="project-structure-")
        self.root = Path(self.temp.name)
        (self.root / ".ai-workflow").mkdir()
        (self.root / "src").mkdir()
        (self.root / "src" / "app.py").write_text("TOP_SECRET_CONTENT\n", encoding="utf-8")
        (self.root / "src" / "README.md").write_text("Source guide\n", encoding="utf-8")
        (self.root / "README.md").write_text("Fixture\n", encoding="utf-8")
        (self.root / "notes.bin").write_bytes(b"binary")
        (self.root / "node_modules" / "package").mkdir(parents=True)
        (self.root / "node_modules" / "package" / "index.js").write_text("ignored", encoding="utf-8")
        self.write_map(base_map())
        (self.root / ".ai-workflow" / "directory-map.ignore").write_text(
            ".git/\nnode_modules/\n.env\n", encoding="utf-8"
        )

    def write_map(self, value: dict) -> None:
        (self.root / ".ai-workflow" / "directory-map.json").write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    def close(self) -> None:
        self.temp.cleanup()


class ProjectStructureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = Fixture()

    def tearDown(self) -> None:
        self.fixture.close()

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.fixture.root), *args],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_scan_ignore_and_role_sources(self) -> None:
        state = project_structure.build_state(self.fixture.root)
        paths = {entry["path"] for entry in state["entries"]}
        self.assertIn("src/app.py", paths)
        self.assertNotIn("node_modules/package/index.js", paths)
        by_path = {entry["path"]: entry for entry in state["entries"]}
        self.assertEqual(by_path["src"]["role_source"], "explicit")
        self.assertEqual(by_path["src/app.py"]["role_source"], "inherited")
        self.assertEqual(by_path["src/README.md"]["role_source"], "inherited")
        self.assertIn("Do not store secrets", by_path["src/README.md"]["boundaries"])
        self.assertEqual(by_path["README.md"]["role_source"], "convention")
        self.assertEqual(by_path["notes.bin"]["role_source"], "unclassified")
        self.assertNotIn("TOP_SECRET_CONTENT", json.dumps(state))

    def test_schema_v2_atlas_passports_flows_and_health(self) -> None:
        value = base_map()
        value["schema_version"] = 2
        value["areas"] = [{
            "id": "application", "name": "Application", "beginner_summary": "User-facing application code",
            "layer": "feature", "paths": ["src/**"], "entry_points": ["src/app.py"], "depends_on": [],
        }]
        value["nodes"][1].update({
            "area": "application", "layer": "feature", "display_name": "Application source",
            "beginner_summary": "Implements the application", "responsibility": "Application behavior",
            "depends_on": ["missing.py"], "importance": "core", "evidence": "project-initialization",
        })
        value["flows"] = [{
            "id": "start", "name": "Application start", "beginner_summary": "How the app starts",
            "steps": [{"path": "src/app.py", "summary": "Runs the application"}],
        }]
        value["task_lenses"] = [{
            "id": "change-app", "name": "Change application", "beginner_summary": "Where to look",
            "primary_paths": ["src/**"], "related_paths": ["README.md"], "avoid_paths": ["docs/**"],
        }]
        self.fixture.write_map(value)
        (self.fixture.root / "notes.bin").unlink()
        state = project_structure.build_state(self.fixture.root)
        self.assertEqual(state["schema_version"], 2)
        self.assertEqual(state["areas"][0]["file_count"], 2)
        self.assertEqual(state["flows"][0]["steps"][0]["path"], "src/app.py")
        self.assertEqual(state["task_lenses"][0]["primary_paths"], ["src/**"])
        self.assertEqual(state["health"]["semantic_coverage"], 100.0)
        self.assertEqual(state["health"]["broken_references"][0]["target"], "missing.py")
        ci = self.run_cli("validate", "--ci")
        self.assertEqual(ci.returncode, 1)
        self.assertEqual(ci.stdout.strip(), "DIRECTORY_MAP_INVALID")

    def test_provisional_verify_and_drift_lifecycle(self) -> None:
        self.assertEqual(self.run_cli("validate").stdout.strip(), "DIRECTORY_MAP_PROVISIONAL")
        self.assertNotEqual(self.run_cli("verify", "--verified-by", "User").returncode, 0)
        (self.fixture.root / "notes.bin").unlink()
        verified = self.run_cli("verify", "--verified-by", "User")
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertEqual(self.run_cli("validate").stdout.strip(), "DIRECTORY_MAP_VERIFIED")
        snapshot = json.loads((self.fixture.root / ".ai-workflow" / "directory-snapshot.json").read_text(encoding="utf-8"))
        self.assertNotIn(".ai-workflow/directory-snapshot.json", {entry["path"] for entry in snapshot["paths"]})
        (self.fixture.root / "src" / "new.py").write_text("pass\n", encoding="utf-8")
        self.assertEqual(self.run_cli("validate").stdout.strip(), "DIRECTORY_MAP_DRIFT_DETECTED")
        self.assertEqual(self.run_cli("validate", "--ci").returncode, 1)
        refreshed = self.run_cli("refresh", "--by", "User")
        self.assertEqual(refreshed.returncode, 0, refreshed.stderr)
        self.assertEqual(self.run_cli("validate").stdout.strip(), "DIRECTORY_MAP_VERIFIED")

    def test_generated_markdown_uses_json_source(self) -> None:
        result = self.run_cli("generate")
        self.assertEqual(result.returncode, 0, result.stderr)
        output = (self.fixture.root / "docs" / "DIRECTORY_MAP.md").read_text(encoding="utf-8")
        self.assertIn("Generated by scripts/project-structure.py", output)
        self.assertIn("Application source", output)
        self.assertIn("案内図の状態: 準備中", output)
        self.assertEqual(self.run_cli("generate", "--check").returncode, 0)
        self.assertEqual(
            self.run_cli("validate", "--require-generated").stdout.strip(),
            "DIRECTORY_MAP_PROVISIONAL",
        )
        (self.fixture.root / ".ai-workflow" / "directory-map.json").write_text(
            (self.fixture.root / ".ai-workflow" / "directory-map.json").read_text(encoding="utf-8").replace(
                "Application source", "Changed application source"
            ),
            encoding="utf-8",
        )
        self.assertEqual(self.run_cli("generate", "--check").returncode, 1)
        self.assertEqual(
            self.run_cli("validate", "--require-generated").stdout.strip(),
            "DIRECTORY_MAP_INVALID",
        )

    def test_invalid_map_has_fixed_output(self) -> None:
        invalid = base_map()
        invalid["nodes"].append(dict(invalid["nodes"][0]))
        self.fixture.write_map(invalid)
        result = self.run_cli("validate")
        self.assertEqual(result.stdout.strip(), "DIRECTORY_MAP_INVALID")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.run_cli("validate", "--ci").returncode, 1)

    def test_path_escape_is_rejected(self) -> None:
        invalid = base_map()
        invalid["nodes"][0]["path"] = "../outside"
        self.fixture.write_map(invalid)
        self.assertEqual(self.run_cli("validate").stdout.strip(), "DIRECTORY_MAP_INVALID")

    def test_symlink_is_not_traversed(self) -> None:
        if not hasattr(Path, "symlink_to"):
            self.skipTest("Symlinks unavailable")
        outside = self.fixture.root.parent / f"outside-{self.fixture.root.name}"
        outside.mkdir(exist_ok=True)
        (outside / "secret.txt").write_text("outside", encoding="utf-8")
        link = self.fixture.root / "external-link"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation is not permitted")
        try:
            state = project_structure.build_state(self.fixture.root)
            paths = {entry["path"] for entry in state["entries"]}
            self.assertIn("external-link", paths)
            self.assertNotIn("external-link/secret.txt", paths)
        finally:
            link.unlink(missing_ok=True)
            (outside / "secret.txt").unlink(missing_ok=True)
            outside.rmdir()

    def test_local_server_token_and_live_update(self) -> None:
        process = subprocess.Popen(
            [sys.executable, str(SCRIPT), "--root", str(self.fixture.root), "serve", "--port", "0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        try:
            assert process.stdout is not None
            first_line = process.stdout.readline().strip()
            self.assertTrue(first_line.startswith("Project Structure Map: "), first_line)
            url = first_line.split(": ", 1)[1]
            parsed = urlparse(url)
            token = parse_qs(parsed.query)["token"][0]
            base = f"http://127.0.0.1:{parsed.port}"

            with self.assertRaises(urllib.error.HTTPError) as denied:
                urllib.request.urlopen(f"{base}/api/state", timeout=5)
            self.assertEqual(denied.exception.code, 403)

            with urllib.request.urlopen(f"{base}/api/state?token={token}", timeout=5) as response:
                state_before = json.loads(response.read().decode("utf-8"))
                self.assertEqual(response.headers["X-Frame-Options"], "DENY")
                self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])
            serialized = json.dumps(state_before)
            self.assertNotIn("TOP_SECRET_CONTENT", serialized)

            with self.assertRaises(urllib.error.HTTPError) as repository_file:
                urllib.request.urlopen(f"{base}/README.md", timeout=5)
            self.assertEqual(repository_file.exception.code, 404)

            with self.assertRaises(urllib.error.HTTPError) as traversal:
                urllib.request.urlopen(f"{base}/..%2F..%2FREADME.md", timeout=5)
            self.assertEqual(traversal.exception.code, 404)

            (self.fixture.root / "src" / "live.py").write_text("pass\n", encoding="utf-8")
            time.sleep(1.2)
            with urllib.request.urlopen(f"{base}/api/state?token={token}", timeout=5) as response:
                state_after = json.loads(response.read().decode("utf-8"))
            self.assertNotEqual(state_before["structure_hash"], state_after["structure_hash"])
            self.assertIn("src/live.py", {entry["path"] for entry in state_after["entries"]})
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
            if process.stdout:
                process.stdout.close()
            if process.stderr:
                process.stderr.close()

    def test_open_browser_option_and_helper(self) -> None:
        args = project_structure.build_parser().parse_args(["serve", "--open-browser"])
        self.assertTrue(args.open_browser)

        url = "http://127.0.0.1:4173/?token=test"
        with mock.patch.object(project_structure.webbrowser, "open", return_value=True) as opener:
            project_structure.launch_browser(url)
        opener.assert_called_once_with(url, new=2)

        with mock.patch.object(project_structure.webbrowser, "open", side_effect=OSError("no browser")):
            project_structure.launch_browser(url)

    def test_viewer_exposes_project_atlas_views(self) -> None:
        html = (SCRIPT.parent / "project-structure-viewer" / "index.html").read_text(encoding="utf-8")
        for view in ("atlas", "tour", "lens", "explorer", "health"):
            self.assertIn(f'data-view="{view}"', html)
            self.assertIn(f'id="view-{view}"', html)
        self.assertIn("このファイルの役割", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
