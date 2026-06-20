#!/usr/bin/env python3
"""Project Structure Map: deterministic structure validation and local viewer.

This tool deliberately reads path metadata only. It never reads or serves project
file contents. Human-approved roles live in directory-map.json; the generated
snapshot contains only relative paths and entry kinds.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import secrets
import sys
import threading
import time
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import parse_qs, urlparse


SCHEMA_VERSION = 1
TOKENS = {
    "provisional": "DIRECTORY_MAP_PROVISIONAL",
    "verified": "DIRECTORY_MAP_VERIFIED",
    "drift": "DIRECTORY_MAP_DRIFT_DETECTED",
    "invalid": "DIRECTORY_MAP_INVALID",
    "failed": "DIRECTORY_MAP_CHECK_FAILED",
}
KINDS = {"directory", "file", "pattern"}
BUILTIN_IGNORE = (
    ".git/",
    ".ai-workflow/directory-snapshot.json",
    ".ai-workflow/runtime/",
    "node_modules/",
    "dist/",
    "build/",
    "coverage/",
    ".next/",
    ".cache/",
    ".pytest_cache/",
    "__pycache__/",
    "*.pyc",
)
MAX_ENTRIES = 100_000


class StructureError(ValueError):
    """Raised when tracked structure configuration is invalid."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_relative(value: str, *, allow_pattern: bool = False) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StructureError("Path must be a non-empty string.")
    raw = value.strip().replace("\\", "/")
    if raw.startswith("/") or (len(raw) > 1 and raw[1] == ":"):
        raise StructureError(f"Absolute path is not allowed: {value}")
    parts = PurePosixPath(raw).parts
    if any(part in {"", ".", ".."} for part in parts):
        raise StructureError(f"Path must stay inside the project: {value}")
    if not allow_pattern and any(char in raw for char in "*?["):
        raise StructureError(f"Wildcards require kind=pattern: {value}")
    return "/".join(parts)


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except (OSError, json.JSONDecodeError) as exc:
        raise StructureError(f"Cannot read valid JSON from {path.name}: {exc}") from exc
    if not isinstance(data, dict):
        raise StructureError(f"{path.name} must contain a JSON object.")
    return data


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    os.replace(temporary, path)


def write_json(path: Path, value: dict[str, Any]) -> None:
    atomic_write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


class IgnoreMatcher:
    def __init__(self, root: Path, custom_file: str):
        self.root = root
        self.patterns: list[tuple[str, bool, bool]] = []
        for pattern in BUILTIN_IGNORE:
            self._add(pattern)
        gitignore = root / ".gitignore"
        if gitignore.is_file():
            self._load(gitignore)
        custom = root / custom_file
        if custom.is_file():
            self._load(custom)

    def _load(self, path: Path) -> None:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            raise StructureError(f"Cannot read ignore file {path}: {exc}") from exc
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                self._add(stripped)

    def _add(self, raw: str) -> None:
        negated = raw.startswith("!")
        pattern = raw[1:] if negated else raw
        pattern = pattern.replace("\\", "/").lstrip("/")
        directory_only = pattern.endswith("/")
        pattern = pattern.rstrip("/")
        if pattern:
            self.patterns.append((pattern, negated, directory_only))

    @staticmethod
    def _matches(path: str, pattern: str, is_dir: bool, directory_only: bool) -> bool:
        if directory_only and not is_dir:
            return False
        if "/" in pattern:
            return fnmatch.fnmatchcase(path, pattern) or path.startswith(pattern + "/")
        return any(fnmatch.fnmatchcase(part, pattern) for part in path.split("/"))

    def ignored(self, path: str, is_dir: bool) -> bool:
        if path == ".git" or path.startswith(".git/"):
            return True
        ignored = False
        for pattern, negated, directory_only in self.patterns:
            if self._matches(path, pattern, is_dir, directory_only):
                ignored = not negated
        return ignored


def validate_map(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("schema_version") != SCHEMA_VERSION:
        raise StructureError(f"schema_version must be {SCHEMA_VERSION}.")
    if data.get("status") not in {"provisional", "verified"}:
        raise StructureError("status must be provisional or verified.")
    project_name = data.get("project_name")
    if project_name is not None and (not isinstance(project_name, str) or not project_name.strip()):
        raise StructureError("project_name must be a non-empty string when provided.")
    ignore_file = normalize_relative(data.get("ignore_file", ".ai-workflow/directory-map.ignore"))
    data["ignore_file"] = ignore_file

    nodes = data.get("nodes")
    if not isinstance(nodes, list):
        raise StructureError("nodes must be an array.")
    seen: set[str] = set()
    normalized_nodes: list[dict[str, Any]] = []
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise StructureError(f"nodes[{index}] must be an object.")
        kind = node.get("kind")
        if kind not in KINDS:
            raise StructureError(f"nodes[{index}].kind must be directory, file, or pattern.")
        path = normalize_relative(node.get("path", ""), allow_pattern=kind == "pattern")
        if path in seen:
            raise StructureError(f"Duplicate node path: {path}")
        seen.add(path)
        role = node.get("role")
        if not isinstance(role, str) or not role.strip():
            raise StructureError(f"nodes[{index}].role must be non-empty.")
        boundaries = node.get("boundaries", [])
        task_types = node.get("task_types", [])
        if not isinstance(boundaries, list) or not all(isinstance(v, str) and v.strip() for v in boundaries):
            raise StructureError(f"nodes[{index}].boundaries must contain non-empty strings.")
        if not isinstance(task_types, list) or not all(isinstance(v, str) and v.strip() for v in task_types):
            raise StructureError(f"nodes[{index}].task_types must contain non-empty strings.")
        normalized_nodes.append(
            {
                "path": path,
                "kind": kind,
                "role": role.strip(),
                "boundaries": [v.strip() for v in boundaries],
                "task_types": [v.strip() for v in task_types],
            }
        )
    data["nodes"] = normalized_nodes

    conventions = data.get("conventions", [])
    if not isinstance(conventions, list):
        raise StructureError("conventions must be an array.")
    normalized_conventions: list[dict[str, str]] = []
    for index, convention in enumerate(conventions):
        if not isinstance(convention, dict):
            raise StructureError(f"conventions[{index}] must be an object.")
        pattern = convention.get("pattern")
        role = convention.get("role")
        if not isinstance(pattern, str) or not pattern.strip():
            raise StructureError(f"conventions[{index}].pattern must be non-empty.")
        if not isinstance(role, str) or not role.strip():
            raise StructureError(f"conventions[{index}].role must be non-empty.")
        normalized_conventions.append({"pattern": pattern.strip().replace("\\", "/"), "role": role.strip()})
    data["conventions"] = normalized_conventions

    verified_at = data.get("verified_at")
    verified_by = data.get("verified_by")
    if data["status"] == "verified":
        if not isinstance(verified_at, str) or not verified_at.strip():
            raise StructureError("verified maps require verified_at.")
        if not isinstance(verified_by, str) or not verified_by.strip():
            raise StructureError("verified maps require verified_by.")
    return data


def load_map(root: Path) -> tuple[dict[str, Any], Path]:
    path = root / ".ai-workflow" / "directory-map.json"
    return validate_map(read_json(path)), path


def scan_project(root: Path, mapping: dict[str, Any]) -> tuple[list[dict[str, str]], list[str]]:
    matcher = IgnoreMatcher(root, mapping["ignore_file"])
    entries: list[dict[str, str]] = []
    warnings: list[str] = []

    def visit(directory: Path, prefix: str = "") -> None:
        try:
            children = sorted(directory.iterdir(), key=lambda item: (not item.is_dir(), item.name.casefold()))
        except (OSError, PermissionError) as exc:
            warnings.append(f"Cannot read {prefix or '.'}: {exc}")
            return
        for child in children:
            relative = f"{prefix}/{child.name}" if prefix else child.name
            relative = relative.replace("\\", "/")
            try:
                is_symlink = child.is_symlink()
                is_directory = child.is_dir() and not is_symlink
            except OSError as exc:
                warnings.append(f"Cannot inspect {relative}: {exc}")
                continue
            if matcher.ignored(relative, is_directory):
                continue
            kind = "symlink" if is_symlink else "directory" if is_directory else "file"
            entries.append({"path": relative, "kind": kind})
            if len(entries) > MAX_ENTRIES:
                raise StructureError(f"Project exceeds the {MAX_ENTRIES} entry safety limit.")
            if is_directory:
                visit(child, relative)

    visit(root)
    entries.sort(key=lambda item: (item["path"].casefold(), item["kind"]))
    return entries, warnings


def structure_hash(entries: list[dict[str, str]]) -> str:
    material = "\n".join(f"{entry['kind']}:{entry['path']}" for entry in entries)
    return "sha256:" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def validate_snapshot(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("schema_version") != SCHEMA_VERSION:
        raise StructureError(f"snapshot schema_version must be {SCHEMA_VERSION}.")
    paths = data.get("paths")
    if not isinstance(paths, list):
        raise StructureError("snapshot paths must be an array.")
    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, entry in enumerate(paths):
        if not isinstance(entry, dict) or entry.get("kind") not in {"directory", "file", "symlink"}:
            raise StructureError(f"snapshot paths[{index}] is invalid.")
        path = normalize_relative(entry.get("path", ""))
        if path in seen:
            raise StructureError(f"snapshot contains duplicate path: {path}")
        seen.add(path)
        normalized.append({"path": path, "kind": entry["kind"]})
    normalized.sort(key=lambda item: (item["path"].casefold(), item["kind"]))
    expected_hash = structure_hash(normalized)
    if data.get("structure_hash") != expected_hash:
        raise StructureError("snapshot structure_hash does not match its paths.")
    data["paths"] = normalized
    return data


def load_snapshot(root: Path) -> tuple[dict[str, Any] | None, Path]:
    path = root / ".ai-workflow" / "directory-snapshot.json"
    if not path.is_file():
        return None, path
    return validate_snapshot(read_json(path)), path


def compare_entries(
    current: list[dict[str, str]], baseline: list[dict[str, str]] | None
) -> dict[str, list[dict[str, str]]]:
    if baseline is None:
        return {"added": [], "removed": [], "type_changed": []}
    current_map = {entry["path"]: entry["kind"] for entry in current}
    baseline_map = {entry["path"]: entry["kind"] for entry in baseline}
    added = [
        {"path": path, "kind": current_map[path]}
        for path in sorted(current_map.keys() - baseline_map.keys(), key=str.casefold)
    ]
    removed = [
        {"path": path, "kind": baseline_map[path]}
        for path in sorted(baseline_map.keys() - current_map.keys(), key=str.casefold)
    ]
    changed = [
        {"path": path, "before": baseline_map[path], "after": current_map[path]}
        for path in sorted(current_map.keys() & baseline_map.keys(), key=str.casefold)
        if current_map[path] != baseline_map[path]
    ]
    return {"added": added, "removed": removed, "type_changed": changed}


def status_for(mapping: dict[str, Any], snapshot: dict[str, Any] | None, current_hash: str) -> str:
    if mapping["status"] == "provisional":
        return TOKENS["provisional"]
    if snapshot is None:
        return TOKENS["invalid"]
    return TOKENS["verified"] if snapshot["structure_hash"] == current_hash else TOKENS["drift"]


def explicit_ancestors(path: str, mapping: dict[str, Any]) -> list[dict[str, Any]]:
    ancestors: list[dict[str, Any]] = []
    parent = PurePosixPath(path).parent
    while str(parent) not in {"", "."}:
        parent_path = str(parent)
        node = next(
            (item for item in mapping["nodes"] if item["kind"] == "directory" and item["path"] == parent_path),
            None,
        )
        if node:
            ancestors.append(node)
        parent = parent.parent
    ancestors.reverse()
    return ancestors


def merged_context(nodes: list[dict[str, Any]]) -> dict[str, list[str]]:
    return {
        key: list(dict.fromkeys(value for node in nodes for value in node.get(key, [])))
        for key in ("boundaries", "task_types")
    }


def role_for(path: str, kind: str, mapping: dict[str, Any]) -> dict[str, Any]:
    ancestors = explicit_ancestors(path, mapping)
    exact = next((node for node in mapping["nodes"] if node["kind"] != "pattern" and node["path"] == path), None)
    if exact:
        return {**exact, **merged_context([*ancestors, exact]), "role_source": "explicit", "role_from": path}
    for node in mapping["nodes"]:
        if node["kind"] == "pattern" and fnmatch.fnmatchcase(path, node["path"]):
            return {
                **node,
                **merged_context([*ancestors, node]),
                "role_source": "explicit-pattern",
                "role_from": node["path"],
            }
    for convention in mapping["conventions"]:
        if fnmatch.fnmatchcase(path, convention["pattern"]) or fnmatch.fnmatchcase(PurePosixPath(path).name, convention["pattern"]):
            return {
                "path": path,
                "kind": kind,
                "role": convention["role"],
                **merged_context(ancestors),
                "role_source": "convention",
                "role_from": convention["pattern"],
            }
    if ancestors:
        inherited = ancestors[-1]
        return {
            **inherited,
            **merged_context(ancestors),
            "path": path,
            "kind": kind,
            "role_source": "inherited",
            "role_from": inherited["path"],
        }
    return {
        "path": path,
        "kind": kind,
        "role": "未分類",
        "boundaries": [],
        "task_types": [],
        "role_source": "unclassified",
        "role_from": None,
    }


def build_state(root: Path) -> dict[str, Any]:
    mapping, _ = load_map(root)
    snapshot, _ = load_snapshot(root)
    entries, warnings = scan_project(root, mapping)
    current_hash = structure_hash(entries)
    baseline_entries = snapshot["paths"] if snapshot else None
    diff = compare_entries(entries, baseline_entries)
    baseline_paths = {entry["path"] for entry in (baseline_entries or [])}
    current_paths = {entry["path"] for entry in entries}
    removed_paths = baseline_paths - current_paths
    enriched = []
    for entry in entries:
        role = role_for(entry["path"], entry["kind"], mapping)
        change = "added" if snapshot is not None and entry["path"] not in baseline_paths else "unchanged"
        enriched.append({**entry, **{k: role[k] for k in ("role", "role_source", "role_from", "boundaries", "task_types")}, "change": change})
    removed = [
        {**entry, **role_for(entry["path"], entry["kind"], mapping), "change": "removed"}
        for entry in (baseline_entries or [])
        if entry["path"] in removed_paths
    ]
    role_counts = {"explicit": 0, "explicit-pattern": 0, "convention": 0, "inherited": 0, "unclassified": 0}
    for entry in enriched:
        role_counts[entry["role_source"]] += 1
    missing_declared = [
        node for node in mapping["nodes"] if node["kind"] != "pattern" and node["path"] not in current_paths
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "project_name": mapping.get("project_name") or root.name,
        "map_status": mapping["status"],
        "validation_result": status_for(mapping, snapshot, current_hash),
        "generated_at": utc_now(),
        "verified_at": mapping.get("verified_at"),
        "verified_by": mapping.get("verified_by"),
        "structure_hash": current_hash,
        "baseline_hash": snapshot.get("structure_hash") if snapshot else None,
        "entries": enriched,
        "removed_entries": removed,
        "diff": diff,
        "missing_declared": missing_declared,
        "warnings": warnings,
        "summary": {
            "files": sum(entry["kind"] == "file" for entry in entries),
            "directories": sum(entry["kind"] == "directory" for entry in entries),
            "symlinks": sum(entry["kind"] == "symlink" for entry in entries),
            "added": len(diff["added"]),
            "removed": len(diff["removed"]),
            "type_changed": len(diff["type_changed"]),
            "unclassified": role_counts["unclassified"],
            "role_counts": role_counts,
        },
    }


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_markdown(state: dict[str, Any], mapping: dict[str, Any]) -> str:
    lines = [
        "# Directory Map",
        "",
        "<!-- Generated by scripts/project-structure.py. Edit .ai-workflow/directory-map.json instead. -->",
        "",
        f"Map Status: {mapping['status'].capitalize()}",
        "",
        "この文書は `.ai-workflow/directory-map.json` から生成されます。直接編集しません。",
        "全ファイルの最新状態と差分は、Project Structure Mapのlocalhost画面で確認します。",
        "",
        "## Verification",
        "",
        f"- Validation result: `{state['validation_result']}`",
        f"- Structure hash: `{state['structure_hash']}`",
        f"- Baseline hash: `{state['baseline_hash'] or 'Not created'}`",
        f"- Verified at: {mapping.get('verified_at') or 'Not verified'}",
        f"- Verified by: {mapping.get('verified_by') or 'Not verified'}",
        f"- Files: {state['summary']['files']}",
        f"- Directories: {state['summary']['directories']}",
        f"- Unclassified entries: {state['summary']['unclassified']}",
        "",
        "## Responsibilities",
        "",
        "| Path | Kind | Role |",
        "|---|---|---|",
    ]
    for node in mapping["nodes"]:
        lines.append(f"| `{markdown_escape(node['path'])}` | {node['kind']} | {markdown_escape(node['role'])} |")
    if not mapping["nodes"]:
        lines.append("| None | - | No approved roles recorded |")

    lines.extend(["", "## Task Routing Guide", "", "| Task Type | Start Here |", "|---|---|"])
    routes = [(task, node["path"]) for node in mapping["nodes"] for task in node["task_types"]]
    for task, path in routes:
        lines.append(f"| {markdown_escape(task)} | `{markdown_escape(path)}` |")
    if not routes:
        lines.append("| None recorded | Review the live structure before planning |")

    lines.extend(["", "## Boundaries", ""])
    boundaries = [(node["path"], boundary) for node in mapping["nodes"] for boundary in node["boundaries"]]
    for path, boundary in boundaries:
        lines.append(f"- `{path}`: {boundary}")
    if not boundaries:
        lines.append("- No project-specific boundaries recorded.")

    lines.extend(
        [
            "",
            "## Structure Changes",
            "",
            f"- Added: {state['summary']['added']}",
            f"- Removed: {state['summary']['removed']}",
            f"- Type changed: {state['summary']['type_changed']}",
            "",
            "## Commands",
            "",
            "```bash",
            "python scripts/project-structure.py validate",
            "python scripts/project-structure.py diff",
            "python scripts/project-structure.py generate",
            "python scripts/project-structure.py serve",
            "```",
            "",
            "構造の基準線を更新するのは、差分を確認した後だけです。",
        ]
    )
    return "\n".join(lines) + "\n"


def generate_markdown(root: Path) -> Path:
    mapping, _ = load_map(root)
    output = root / "docs" / "DIRECTORY_MAP.md"
    if not output.is_file():
        atomic_write(output, "# Directory Map\n")
    state = build_state(root)
    atomic_write(output, render_markdown(state, mapping))
    return output


def generated_markdown_matches(root: Path) -> bool:
    mapping, _ = load_map(root)
    state = build_state(root)
    output = root / "docs" / "DIRECTORY_MAP.md"
    if not output.is_file():
        return False
    return output.read_text(encoding="utf-8") == render_markdown(state, mapping)


def refresh_snapshot(root: Path, actor: str | None, verify: bool) -> tuple[dict[str, Any], Path]:
    mapping, map_path = load_map(root)
    if verify and (not actor or not actor.strip()):
        raise StructureError("verify requires --verified-by with the approving person or role.")
    # Ensure the generated document exists before taking the path-only baseline.
    # Otherwise the first generation would immediately create false drift.
    generate_markdown(root)
    candidate = build_state(root)
    if candidate["summary"]["unclassified"]:
        raise StructureError(
            f"Cannot accept a baseline with {candidate['summary']['unclassified']} unclassified entries."
        )
    if candidate["missing_declared"]:
        raise StructureError(
            f"Cannot accept a baseline with {len(candidate['missing_declared'])} missing declared paths."
        )
    if candidate["warnings"]:
        raise StructureError(f"Cannot accept a baseline with {len(candidate['warnings'])} scan warnings.")
    entries, _ = scan_project(root, mapping)
    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "structure_hash": structure_hash(entries),
        "paths": entries,
    }
    snapshot_path = root / ".ai-workflow" / "directory-snapshot.json"
    write_json(snapshot_path, snapshot)
    if verify:
        mapping["status"] = "verified"
        mapping["verified_at"] = utc_now()
        mapping["verified_by"] = actor.strip()
        write_json(map_path, mapping)
    elif mapping["status"] == "verified":
        mapping["verified_at"] = utc_now()
        if actor and actor.strip():
            mapping["verified_by"] = actor.strip()
        write_json(map_path, mapping)
    generate_markdown(root)
    return snapshot, snapshot_path


class LiveState:
    def __init__(self, root: Path, interval: float = 1.0):
        self.root = root
        self.interval = interval
        self.lock = threading.Lock()
        self.last_checked = 0.0
        self.cached: dict[str, Any] | None = None

    def get(self, force: bool = False) -> dict[str, Any]:
        with self.lock:
            now = time.monotonic()
            if force or self.cached is None or now - self.last_checked >= self.interval:
                self.cached = build_state(self.root)
                self.last_checked = now
            return self.cached


def serve(root: Path, port: int) -> None:
    token = secrets.token_urlsafe(24)
    static_root = Path(__file__).resolve().parent / "project-structure-viewer"
    if not static_root.is_dir():
        raise StructureError(f"Viewer assets are missing: {static_root}")
    live = LiveState(root)

    class Handler(BaseHTTPRequestHandler):
        server_version = "ProjectStructureMap/1.0"

        def log_message(self, format: str, *args: Any) -> None:
            sys.stderr.write("[project-structure] " + format % args + "\n")

        def security_headers(self, content_type: str) -> None:
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; "
                "img-src 'self' data:; object-src 'none'; frame-ancestors 'none'; base-uri 'none'",
            )

        def send_bytes(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.security_headers(content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def send_json(self, status: int, value: Any) -> None:
            body = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            self.send_bytes(status, body, "application/json; charset=utf-8")

        def authorized(self, query: dict[str, list[str]]) -> bool:
            supplied = query.get("token", [""])[0]
            return secrets.compare_digest(supplied, token)

        def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)
            if parsed.path.startswith("/api/"):
                if not self.authorized(query):
                    self.send_json(HTTPStatus.FORBIDDEN, {"error": "Access token required."})
                    return
                try:
                    state = live.get(force=query.get("force") == ["1"])
                except (OSError, StructureError) as exc:
                    self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
                    return
                if parsed.path == "/api/health":
                    self.send_json(HTTPStatus.OK, {"ok": True, "validation_result": state["validation_result"]})
                elif parsed.path == "/api/state":
                    self.send_json(HTTPStatus.OK, state)
                else:
                    self.send_json(HTTPStatus.NOT_FOUND, {"error": "Not found."})
                return

            assets = {
                "/": ("index.html", "text/html; charset=utf-8"),
                "/index.html": ("index.html", "text/html; charset=utf-8"),
                "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                "/styles.css": ("styles.css", "text/css; charset=utf-8"),
            }
            asset = assets.get(parsed.path)
            if asset is None:
                self.send_bytes(HTTPStatus.NOT_FOUND, b"Not found", "text/plain; charset=utf-8")
                return
            file_path = static_root / asset[0]
            try:
                body = file_path.read_bytes()
            except OSError:
                self.send_bytes(HTTPStatus.INTERNAL_SERVER_ERROR, b"Viewer asset missing", "text/plain; charset=utf-8")
                return
            self.send_bytes(HTTPStatus.OK, body, asset[1])

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    actual_port = server.server_address[1]
    print(f"Project Structure Map: http://127.0.0.1:{actual_port}/?token={token}", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def default_root() -> Path:
    return Path(__file__).resolve().parent.parent


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate and visualize the project directory structure.")
    parser.add_argument("--root", type=Path, default=default_root(), help="Project root (defaults to script parent).")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Print a fixed structure status token.")
    validate.add_argument("--ci", action="store_true", help="Return non-zero for verified drift or invalid state.")
    validate.add_argument("--json", action="store_true", dest="as_json", help="Print the complete state as JSON.")
    validate.add_argument(
        "--require-generated",
        action="store_true",
        help="Treat a stale generated docs/DIRECTORY_MAP.md as invalid when structure otherwise passes.",
    )

    scan = sub.add_parser("scan", help="Print the live structure state as JSON.")
    scan.add_argument("--compact", action="store_true")

    sub.add_parser("diff", help="Print structure changes since the verified snapshot.")
    generate = sub.add_parser("generate", help="Regenerate docs/DIRECTORY_MAP.md from the JSON source.")
    generate.add_argument("--check", action="store_true", help="Fail instead of writing when the document is stale.")

    refresh = sub.add_parser("refresh", help="Accept the current path structure as the new baseline.")
    refresh.add_argument("--by", help="Person or role accepting this baseline.")

    verify = sub.add_parser("verify", help="Create a baseline and mark the map verified after approval.")
    verify.add_argument("--verified-by", required=True, help="Approving person or role.")

    serve_parser = sub.add_parser("serve", help="Start the read-only localhost viewer.")
    serve_parser.add_argument("--port", type=int, default=4173)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if not root.is_dir():
            raise FileNotFoundError(f"Project root does not exist: {root}")
        if args.command == "validate":
            state = build_state(root)
            if (
                args.require_generated
                and state["validation_result"] in {TOKENS["provisional"], TOKENS["verified"]}
                and not generated_markdown_matches(root)
            ):
                state["validation_result"] = TOKENS["invalid"]
            if args.as_json:
                print_json(state)
            else:
                print(state["validation_result"])
            if args.ci and state["validation_result"] in {
                TOKENS["drift"],
                TOKENS["invalid"],
                TOKENS["failed"],
            }:
                return 1
            return 0
        if args.command == "scan":
            state = build_state(root)
            if args.compact:
                print(json.dumps(state, ensure_ascii=False, separators=(",", ":")))
            else:
                print_json(state)
            return 0
        if args.command == "diff":
            state = build_state(root)
            print_json(
                {
                    "validation_result": state["validation_result"],
                    "diff": state["diff"],
                    "missing_declared": state["missing_declared"],
                    "warnings": state["warnings"],
                }
            )
            return 0
        if args.command == "generate":
            if args.check:
                if generated_markdown_matches(root):
                    print("DIRECTORY_MAP_GENERATED_DOCUMENT_CURRENT")
                    return 0
                print("DIRECTORY_MAP_GENERATED_DOCUMENT_STALE")
                return 1
            print(generate_markdown(root).relative_to(root).as_posix())
            return 0
        if args.command == "refresh":
            _, path = refresh_snapshot(root, args.by, verify=False)
            print(path.relative_to(root).as_posix())
            return 0
        if args.command == "verify":
            _, path = refresh_snapshot(root, args.verified_by, verify=True)
            print(path.relative_to(root).as_posix())
            return 0
        if args.command == "serve":
            if args.port < 0 or args.port > 65535:
                raise StructureError("port must be between 0 and 65535.")
            serve(root, args.port)
            return 0
    except FileNotFoundError as exc:
        if args.command == "validate":
            print(TOKENS["failed"])
            return 1 if args.ci else 0
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except StructureError as exc:
        if args.command == "validate":
            print(TOKENS["invalid"])
            return 1 if args.ci else 0
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        if args.command == "validate":
            print(TOKENS["failed"])
            return 1 if args.ci else 0
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
