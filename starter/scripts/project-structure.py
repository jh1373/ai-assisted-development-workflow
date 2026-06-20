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
import webbrowser
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import parse_qs, urlparse


SCHEMA_VERSION = 2
SNAPSHOT_SCHEMA_VERSION = 1
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


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise StructureError(f"{label} must contain non-empty strings.")
    return [item.strip() for item in value]


def _validate_flows(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise StructureError("flows must be an array.")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, flow in enumerate(value):
        if not isinstance(flow, dict):
            raise StructureError(f"flows[{index}] must be an object.")
        flow_id, name, summary = flow.get("id"), flow.get("name"), flow.get("beginner_summary")
        if not isinstance(flow_id, str) or not flow_id.strip() or flow_id in seen:
            raise StructureError(f"flows[{index}].id must be unique and non-empty.")
        if not isinstance(name, str) or not name.strip() or not isinstance(summary, str) or not summary.strip():
            raise StructureError(f"flows[{index}] requires name and beginner_summary.")
        steps = flow.get("steps")
        if not isinstance(steps, list) or not steps:
            raise StructureError(f"flows[{index}].steps must be a non-empty array.")
        normalized_steps = []
        for step_index, step in enumerate(steps):
            if not isinstance(step, dict) or not isinstance(step.get("summary"), str) or not step["summary"].strip():
                raise StructureError(f"flows[{index}].steps[{step_index}] requires a summary.")
            normalized_steps.append({
                "path": normalize_relative(step.get("path", ""), allow_pattern=True),
                "summary": step["summary"].strip(),
            })
        seen.add(flow_id.strip())
        result.append({"id": flow_id.strip(), "name": name.strip(), "beginner_summary": summary.strip(), "steps": normalized_steps})
    return result


def _validate_task_lenses(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise StructureError("task_lenses must be an array.")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, lens in enumerate(value):
        if not isinstance(lens, dict):
            raise StructureError(f"task_lenses[{index}] must be an object.")
        lens_id, name, summary = lens.get("id"), lens.get("name"), lens.get("beginner_summary")
        if not isinstance(lens_id, str) or not lens_id.strip() or lens_id in seen:
            raise StructureError(f"task_lenses[{index}].id must be unique and non-empty.")
        if not isinstance(name, str) or not name.strip() or not isinstance(summary, str) or not summary.strip():
            raise StructureError(f"task_lenses[{index}] requires name and beginner_summary.")
        seen.add(lens_id.strip())
        result.append({
            "id": lens_id.strip(), "name": name.strip(), "beginner_summary": summary.strip(),
            **{key: [normalize_relative(item, allow_pattern=True) for item in _string_list(lens.get(key, []), f"task_lenses[{index}].{key}")]
               for key in ("primary_paths", "related_paths", "avoid_paths")},
        })
    return result


def validate_map(data: dict[str, Any]) -> dict[str, Any]:
    source_schema = data.get("schema_version")
    if source_schema not in {1, SCHEMA_VERSION}:
        raise StructureError(f"schema_version must be 1 or {SCHEMA_VERSION}.")
    data["_source_schema_version"] = source_schema
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
                "display_name": str(node.get("display_name") or PurePosixPath(path).name).strip(),
                "beginner_summary": str(node.get("beginner_summary") or role).strip(),
                "responsibility": str(node.get("responsibility") or role).strip(),
                "not_responsible_for": _string_list(node.get("not_responsible_for", []), f"nodes[{index}].not_responsible_for"),
                "when_to_change": _string_list(node.get("when_to_change", []), f"nodes[{index}].when_to_change"),
                "inputs": _string_list(node.get("inputs", []), f"nodes[{index}].inputs"),
                "outputs": _string_list(node.get("outputs", []), f"nodes[{index}].outputs"),
                "depends_on": [normalize_relative(value, allow_pattern=True) for value in _string_list(node.get("depends_on", []), f"nodes[{index}].depends_on")],
                "area": node.get("area"),
                "layer": node.get("layer"),
                "importance": node.get("importance", "support"),
                "evidence": node.get("evidence", "human-confirmed" if kind != "pattern" else "project-initialization"),
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

    areas = data.get("areas", [])
    if not isinstance(areas, list):
        raise StructureError("areas must be an array.")
    normalized_areas: list[dict[str, Any]] = []
    area_ids: set[str] = set()
    for index, area in enumerate(areas):
        if not isinstance(area, dict):
            raise StructureError(f"areas[{index}] must be an object.")
        area_id = area.get("id")
        name = area.get("name")
        summary = area.get("beginner_summary")
        layer = area.get("layer")
        if not isinstance(area_id, str) or not area_id.strip() or area_id in area_ids:
            raise StructureError(f"areas[{index}].id must be unique and non-empty.")
        if not isinstance(name, str) or not name.strip() or not isinstance(summary, str) or not summary.strip():
            raise StructureError(f"areas[{index}] requires name and beginner_summary.")
        if layer not in {"experience", "feature", "data", "platform", "workflow", "documentation"}:
            raise StructureError(f"areas[{index}].layer is invalid.")
        area_ids.add(area_id.strip())
        normalized_areas.append({
            "id": area_id.strip(), "name": name.strip(), "beginner_summary": summary.strip(), "layer": layer,
            "paths": [normalize_relative(value, allow_pattern=True) for value in _string_list(area.get("paths", []), f"areas[{index}].paths")],
            "entry_points": [normalize_relative(value, allow_pattern=True) for value in _string_list(area.get("entry_points", []), f"areas[{index}].entry_points")],
            "depends_on": _string_list(area.get("depends_on", []), f"areas[{index}].depends_on"),
        })
    for area in normalized_areas:
        unknown = set(area["depends_on"]) - area_ids
        if unknown:
            raise StructureError(f"area {area['id']} depends on unknown areas: {', '.join(sorted(unknown))}")
    data["areas"] = normalized_areas

    for index, node in enumerate(normalized_nodes):
        if node["area"] is not None and node["area"] not in area_ids:
            raise StructureError(f"nodes[{index}].area references an unknown area.")
        if node["layer"] is not None and node["layer"] not in {area["layer"] for area in normalized_areas}:
            raise StructureError(f"nodes[{index}].layer is invalid.")
        if node["importance"] not in {"entry-point", "core", "support"}:
            raise StructureError(f"nodes[{index}].importance is invalid.")
        if node["evidence"] not in {"human-confirmed", "registered-when-created", "project-initialization", "convention"}:
            raise StructureError(f"nodes[{index}].evidence is invalid.")

    data["flows"] = _validate_flows(data.get("flows", []))
    data["task_lenses"] = _validate_task_lenses(data.get("task_lenses", []))

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
    if data.get("schema_version") != SNAPSHOT_SCHEMA_VERSION:
        raise StructureError(f"snapshot schema_version must be {SNAPSHOT_SCHEMA_VERSION}.")
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


PASSPORT_FIELDS = (
    "display_name", "beginner_summary", "responsibility", "not_responsible_for", "when_to_change",
    "inputs", "outputs", "depends_on", "area", "layer", "importance", "evidence",
)


def fallback_passport(path: str, role: str, *, evidence: str = "convention") -> dict[str, Any]:
    return {
        "display_name": PurePosixPath(path).name,
        "beginner_summary": role,
        "responsibility": role,
        "not_responsible_for": [], "when_to_change": [], "inputs": [], "outputs": [], "depends_on": [],
        "area": None, "layer": None, "importance": "support", "evidence": evidence,
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
    for convention in mapping["conventions"]:
        if fnmatch.fnmatchcase(path, convention["pattern"]) or fnmatch.fnmatchcase(PurePosixPath(path).name, convention["pattern"]):
            return {
                "path": path,
                "kind": kind,
                "role": convention["role"],
                **fallback_passport(path, convention["role"]),
                **merged_context(ancestors),
                "role_source": "convention",
                "role_from": convention["pattern"],
            }
    return {
        "path": path,
        "kind": kind,
        "role": "未分類",
        **fallback_passport(path, "この項目の役割はまだ説明されていません。", evidence="convention"),
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
        enriched.append({**entry, **{k: role[k] for k in ("role", "role_source", "role_from", "boundaries", "task_types", *PASSPORT_FIELDS)}, "change": change})
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
    current_map = {entry["path"]: entry for entry in enriched}

    def declared_matches(pattern: str) -> list[str]:
        return [path for path in current_paths if fnmatch.fnmatchcase(path, pattern) or path == pattern.removesuffix("/**")]

    def reference_known(target: str) -> bool:
        if declared_matches(target):
            return True
        target_prefix = target.split("*", 1)[0].split("?", 1)[0].rstrip("/")
        for node in mapping["nodes"]:
            node_path = node["path"]
            node_prefix = node_path.split("*", 1)[0].split("?", 1)[0].rstrip("/")
            if fnmatch.fnmatchcase(target, node_path) or fnmatch.fnmatchcase(node_path, target):
                return True
            if target_prefix and node_prefix and (target_prefix.startswith(node_prefix) or node_prefix.startswith(target_prefix)):
                return True
        return False

    broken_references = []
    for node in mapping["nodes"]:
        for target in node["depends_on"]:
            if not reference_known(target):
                broken_references.append({"source": node["path"], "target": target, "kind": "dependency"})
    for flow in mapping["flows"]:
        for step in flow["steps"]:
            if not reference_known(step["path"]):
                broken_references.append({"source": flow["id"], "target": step["path"], "kind": "flow"})
    for lens in mapping["task_lenses"]:
        for key in ("primary_paths", "related_paths", "avoid_paths"):
            for target in lens[key]:
                if not reference_known(target):
                    broken_references.append({"source": lens["id"], "target": target, "kind": "task-lens"})

    resolved_areas = []
    for area in mapping["areas"]:
        paths = sorted({path for pattern in area["paths"] for path in declared_matches(pattern)}, key=str.casefold)
        resolved_areas.append({
            **area,
            "resolved_paths": paths,
            "entry_points_present": [path for pattern in area["entry_points"] for path in declared_matches(pattern)],
            "file_count": sum(current_map[path]["kind"] == "file" for path in paths),
        })

    explained = [entry for entry in enriched if entry["role_source"] != "unclassified"]
    exact_passports = [entry for entry in enriched if entry["kind"] == "file" and entry["role_source"] == "explicit"]
    specific_passports = [entry for entry in enriched if entry["kind"] == "file" and entry["role_source"] not in {"convention", "unclassified"}]
    generic_passports = [entry for entry in enriched if entry["kind"] == "file" and entry["role_source"] == "convention"]
    health = {
        "semantic_coverage": round(100 * len(explained) / len(enriched), 1) if enriched else 100.0,
        "passport_coverage": round(100 * len(specific_passports) / max(1, sum(entry["kind"] == "file" for entry in enriched)), 1),
        "individual_passport_coverage": round(100 * len(exact_passports) / max(1, sum(entry["kind"] == "file" for entry in enriched)), 1),
        "unexplained_paths": [entry["path"] for entry in enriched if entry["role_source"] == "unclassified"],
        "generic_passports": [entry["path"] for entry in generic_passports],
        "broken_references": broken_references,
    }
    health["issue_count"] = len(health["unexplained_paths"]) + len(health["generic_passports"]) + len(broken_references)
    return {
        "schema_version": SCHEMA_VERSION,
        "map_schema_version": mapping["_source_schema_version"],
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
        "areas": resolved_areas,
        "flows": mapping["flows"],
        "task_lenses": mapping["task_lenses"],
        "health": health,
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
    status_labels = {"provisional": "準備中", "verified": "確認済み"}
    layer_labels = {
        "experience": "ユーザーが触れる画面",
        "feature": "プロダクトの機能",
        "data": "データと外部通信",
        "platform": "自動化と運用基盤",
        "workflow": "AIと人間の開発手順",
        "documentation": "計画と判断の記録",
    }
    kind_labels = {"directory": "フォルダ", "file": "ファイル", "pattern": "まとめて適用する規則"}
    lines = [
        "# プロジェクト案内図",
        "",
        "<!-- Generated by scripts/project-structure.py. Edit .ai-workflow/directory-map.json instead. -->",
        "",
        f"案内図の状態: {status_labels[mapping['status']]}",
        "",
        "この文書は `.ai-workflow/directory-map.json` から生成されます。直接編集しません。",
        "全ファイルの最新状態と変更点は、localhostのプロジェクト案内図で確認します。",
        "",
        "## 構成と説明の確認",
        "",
        f"- 機械判定: `{state['validation_result']}`",
        f"- 現在の構成を表す値: `{state['structure_hash']}`",
        f"- 確認済み構成を表す値: `{state['baseline_hash'] or '未作成'}`",
        f"- 最終確認日時: {mapping.get('verified_at') or '未確認'}",
        f"- 確認者: {mapping.get('verified_by') or '未確認'}",
        f"- ファイル数: {state['summary']['files']}",
        f"- フォルダ数: {state['summary']['directories']}",
        f"- 役割説明なし: {state['summary']['unclassified']}",
        f"- 役割が分かる割合: {state['health']['semantic_coverage']}%",
        f"- プロジェクト固有の説明がある割合: {state['health']['passport_coverage']}%",
        f"- 個別説明がある割合: {state['health']['individual_passport_coverage']}%",
        f"- 説明の見直し件数: {state['health']['issue_count']}",
        "",
        "## プロジェクトの主な役割",
        "",
        "| 役割 | 分類 | 初心者向け説明 | ファイル数 |",
        "|---|---|---|---:|",
    ]
    for area in state["areas"]:
        lines.append(f"| {markdown_escape(area['name'])} | {layer_labels.get(area['layer'], area['layer'])} | {markdown_escape(area['beginner_summary'])} | {area['file_count']} |")
    if not state["areas"]:
        lines.append("| 未設定 | - | 初回設定でプロジェクトの主な役割を決めます | 0 |")

    lines.extend([
        "",
        "## ファイルとフォルダの役割",
        "",
        "| 場所 | 種類 | 表示名 | 何をする場所か |",
        "|---|---|---|---|",
    ])
    for node in mapping["nodes"]:
        lines.append(f"| `{markdown_escape(node['path'])}` | {kind_labels.get(node['kind'], node['kind'])} | {markdown_escape(node['display_name'])} | {markdown_escape(node['beginner_summary'])} |")
    if not mapping["nodes"]:
        lines.append("| 未登録 | - | 確認済みの役割説明はありません |")

    lines.extend(["", "## 処理の流れ", ""])
    for flow in mapping["flows"]:
        lines.extend([f"### {flow['name']}", "", flow["beginner_summary"], ""])
        for number, step in enumerate(flow["steps"], 1):
            lines.append(f"{number}. `{step['path']}` — {step['summary']}")
        lines.append("")
    if not mapping["flows"]:
        lines.append("- 処理の流れはまだ登録されていません。")

    lines.extend(["", "## 作業場所の案内", "", "| 作業 | 最初に見る場所 | 関連して見る場所 | 今回触らない場所 |", "|---|---|---|---|"])
    for lens in mapping["task_lenses"]:
        lines.append(f"| {markdown_escape(lens['name'])} | {markdown_escape(', '.join(lens['primary_paths']))} | {markdown_escape(', '.join(lens['related_paths']))} | {markdown_escape(', '.join(lens['avoid_paths']))} |")
    if not mapping["task_lenses"]:
        lines.append("| 未登録 | - | - | - |")

    lines.extend(["", "## 作業内容ごとの確認場所", "", "| 作業内容 | 最初に見る場所 |", "|---|---|"])
    routes = [(task, node["path"]) for node in mapping["nodes"] for task in node["task_types"]]
    for task, path in routes:
        lines.append(f"| {markdown_escape(task)} | `{markdown_escape(path)}` |")
    if not routes:
        lines.append("| 未登録 | 計画を立てる前に現在の構成を確認してください |")

    lines.extend(["", "## 変更するときの注意", ""])
    boundaries = [(node["path"], boundary) for node in mapping["nodes"] for boundary in node["boundaries"]]
    for path, boundary in boundaries:
        lines.append(f"- `{path}`: {boundary}")
    if not boundaries:
        lines.append("- プロジェクト固有の注意事項はまだ登録されていません。")

    lines.extend(
        [
            "",
            "## 構成の変更",
            "",
            f"- 追加: {state['summary']['added']}",
            f"- 削除: {state['summary']['removed']}",
            f"- 種類変更: {state['summary']['type_changed']}",
            "",
            "## 確認コマンド",
            "",
            "```bash",
            "python scripts/project-structure.py validate",
            "python scripts/project-structure.py diff",
            "python scripts/project-structure.py generate",
            "python scripts/project-structure.py serve --open-browser",
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
    if mapping["_source_schema_version"] >= 2 and candidate["health"]["issue_count"]:
        raise StructureError(
            f"Cannot accept a baseline with {candidate['health']['issue_count']} semantic health issues."
        )
    if candidate["missing_declared"]:
        raise StructureError(
            f"Cannot accept a baseline with {len(candidate['missing_declared'])} missing declared paths."
        )
    if candidate["warnings"]:
        raise StructureError(f"Cannot accept a baseline with {len(candidate['warnings'])} scan warnings.")
    entries, _ = scan_project(root, mapping)
    snapshot = {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
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
        write_json(map_path, {key: value for key, value in mapping.items() if not key.startswith("_")})
    elif mapping["status"] == "verified":
        mapping["verified_at"] = utc_now()
        if actor and actor.strip():
            mapping["verified_by"] = actor.strip()
        write_json(map_path, {key: value for key, value in mapping.items() if not key.startswith("_")})
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


def launch_browser(url: str) -> None:
    try:
        opened = webbrowser.open(url, new=2)
    except Exception as exc:  # Browser registration differs across operating systems.
        print(f"Browser could not be opened automatically: {exc}", file=sys.stderr, flush=True)
        return
    if not opened:
        print("Browser could not be opened automatically. Open the URL above manually.", file=sys.stderr, flush=True)


def serve(root: Path, port: int, open_browser: bool = False) -> None:
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
    url = f"http://127.0.0.1:{actual_port}/?token={token}"
    print(f"Project Structure Map: {url}", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    if open_browser:
        threading.Thread(target=launch_browser, args=(url,), daemon=True).start()
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
    serve_parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Open the token-protected viewer URL in the default browser.",
    )
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
            if args.ci and state["map_schema_version"] >= 2 and state["health"]["issue_count"]:
                state["validation_result"] = TOKENS["invalid"]
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
            serve(root, args.port, open_browser=args.open_browser)
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
