(() => {
  "use strict";

  const params = new URLSearchParams(window.location.search);
  const token = params.get("token") || sessionStorage.getItem("project-structure-token") || "";
  if (token) sessionStorage.setItem("project-structure-token", token);
  if (params.has("token")) {
    params.delete("token");
    const clean = `${window.location.pathname}${params.toString() ? `?${params}` : ""}`;
    window.history.replaceState(null, "", clean);
  }

  const elements = Object.fromEntries([
    "live-indicator", "map-status", "alert", "files-count", "directories-count",
    "changes-count", "unclassified-count", "project-name", "last-checked", "search",
    "role-filter", "changes-only", "expand-all", "collapse-all", "tree-summary", "tree",
    "detail-title", "detail-path", "detail-kind", "detail-change", "detail-role",
    "detail-source", "detail-boundaries", "detail-tasks", "verification-meta"
  ].map((id) => [id, document.getElementById(id)]));

  let currentState = null;
  let selectedPath = null;
  let renderedRevision = "";

  function labelForSource(source) {
    return {
      explicit: "明示された役割",
      "explicit-pattern": "登録パターン",
      inherited: "親ディレクトリから継承",
      convention: "標準ファイル名から判定",
      unclassified: "未分類"
    }[source] || source;
  }

  function labelForKind(kind) {
    return { file: "ファイル", directory: "ディレクトリ", symlink: "シンボリックリンク" }[kind] || kind;
  }

  function labelForChange(change) {
    return { unchanged: "基準線と一致", added: "追加", removed: "削除" }[change] || change;
  }

  function statusClass(result) {
    if (result === "DIRECTORY_MAP_VERIFIED") return "verified";
    if (result === "DIRECTORY_MAP_PROVISIONAL") return "provisional";
    return "drift";
  }

  function statusLabel(result) {
    return {
      DIRECTORY_MAP_VERIFIED: "VERIFIED",
      DIRECTORY_MAP_PROVISIONAL: "PROVISIONAL",
      DIRECTORY_MAP_DRIFT_DETECTED: "DRIFT DETECTED",
      DIRECTORY_MAP_INVALID: "INVALID",
      DIRECTORY_MAP_CHECK_FAILED: "CHECK FAILED"
    }[result] || result;
  }

  function buildHierarchy(entries) {
    const root = { children: new Map(), entry: null };
    for (const entry of entries) {
      const parts = entry.path.split("/");
      let cursor = root;
      parts.forEach((part, index) => {
        if (!cursor.children.has(part)) cursor.children.set(part, { children: new Map(), entry: null });
        cursor = cursor.children.get(part);
        if (index === parts.length - 1) cursor.entry = entry;
      });
    }
    return root;
  }

  function entryMatches(entry) {
    const query = elements.search.value.trim().toLocaleLowerCase("ja");
    if (query && !`${entry.path} ${entry.role}`.toLocaleLowerCase("ja").includes(query)) return false;
    const roleFilter = elements["role-filter"].value;
    if (roleFilter === "explicit" && !entry.role_source.startsWith("explicit")) return false;
    if (roleFilter !== "all" && roleFilter !== "explicit" && entry.role_source !== roleFilter) return false;
    if (elements["changes-only"].checked && entry.change === "unchanged") return false;
    return true;
  }

  function nodeHasMatch(node) {
    if (node.entry && entryMatches(node.entry)) return true;
    return [...node.children.values()].some(nodeHasMatch);
  }

  function roleBadge(entry) {
    const badge = document.createElement("span");
    badge.className = `entry-badge ${entry.role_source}`;
    badge.textContent = entry.role_source === "unclassified" ? "未分類" : labelForSource(entry.role_source);
    return badge;
  }

  function changeBadge(entry) {
    if (entry.change === "unchanged") return null;
    const badge = document.createElement("span");
    badge.className = `change-badge ${entry.change}`;
    badge.textContent = labelForChange(entry.change);
    return badge;
  }

  function entryLine(entry, name) {
    const line = document.createElement("span");
    line.className = "entry-line";
    const title = document.createElement("span");
    title.className = "entry-name";
    title.textContent = name;
    const role = document.createElement("span");
    role.className = "entry-role";
    role.textContent = entry.role;
    line.append(title, role, roleBadge(entry));
    const change = changeBadge(entry);
    if (change) line.append(change);
    return line;
  }

  function renderNode(name, node, depth) {
    if (!nodeHasMatch(node)) return null;
    const entry = node.entry || {
      path: name,
      kind: "directory",
      role: "親ディレクトリ",
      role_source: "inherited",
      role_from: null,
      boundaries: [],
      task_types: [],
      change: "unchanged"
    };
    const isDirectory = entry.kind === "directory" || node.children.size > 0;
    if (isDirectory) {
      const details = document.createElement("details");
      details.open = depth < 2;
      details.dataset.path = entry.path;
      const summary = document.createElement("summary");
      summary.append(entryLine(entry, name));
      summary.addEventListener("click", () => selectEntry(entry));
      details.append(summary);
      [...node.children.entries()]
        .sort(([a, nodeA], [b, nodeB]) => {
          const aDir = nodeA.entry?.kind === "directory" || nodeA.children.size > 0;
          const bDir = nodeB.entry?.kind === "directory" || nodeB.children.size > 0;
          return aDir === bDir ? a.localeCompare(b, "ja") : aDir ? -1 : 1;
        })
        .forEach(([childName, childNode]) => {
          const child = renderNode(childName, childNode, depth + 1);
          if (child) details.append(child);
        });
      return details;
    }
    const button = document.createElement("button");
    button.type = "button";
    button.className = "file-row";
    button.dataset.path = entry.path;
    button.append(entryLine(entry, name));
    button.addEventListener("click", () => selectEntry(entry));
    return button;
  }

  function renderTree() {
    if (!currentState) return;
    const entries = [...currentState.entries, ...currentState.removed_entries];
    const hierarchy = buildHierarchy(entries);
    const fragment = document.createDocumentFragment();
    let shown = 0;
    [...hierarchy.children.entries()].forEach(([name, node]) => {
      const child = renderNode(name, node, 0);
      if (child) {
        shown += 1;
        fragment.append(child);
      }
    });
    elements.tree.replaceChildren(fragment);
    elements["tree-summary"].textContent = `${entries.length}項目中、現在の条件に一致するトップレベル項目は${shown}件です。`;
    if (!shown) {
      const empty = document.createElement("p");
      empty.className = "empty-state";
      empty.textContent = "条件に一致する項目がありません。";
      elements.tree.append(empty);
    }
    if (selectedPath) {
      const selected = elements.tree.querySelector(`[data-path="${CSS.escape(selectedPath)}"]`);
      selected?.classList.add("selected");
    } else if (entries.length) {
      selectEntry(entries[0]);
    }
  }

  function replaceList(element, values) {
    const items = values.length ? values : ["登録されていません"];
    element.replaceChildren(...items.map((value) => {
      const item = document.createElement("li");
      item.textContent = value;
      return item;
    }));
  }

  function selectEntry(entry) {
    selectedPath = entry.path;
    elements.tree.querySelectorAll(".selected").forEach((node) => node.classList.remove("selected"));
    elements.tree.querySelector(`[data-path="${CSS.escape(entry.path)}"]`)?.classList.add("selected");
    elements["detail-title"].textContent = entry.path.split("/").pop();
    elements["detail-path"].textContent = entry.path;
    elements["detail-kind"].textContent = labelForKind(entry.kind);
    elements["detail-change"].textContent = labelForChange(entry.change);
    elements["detail-role"].textContent = entry.role;
    elements["detail-source"].textContent = entry.role_from
      ? `${labelForSource(entry.role_source)}: ${entry.role_from}`
      : labelForSource(entry.role_source);
    replaceList(elements["detail-boundaries"], entry.boundaries || []);
    replaceList(elements["detail-tasks"], entry.task_types || []);
  }

  function updateSummary(state) {
    const summary = state.summary;
    elements["files-count"].textContent = summary.files.toLocaleString("ja-JP");
    elements["directories-count"].textContent = summary.directories.toLocaleString("ja-JP");
    elements["changes-count"].textContent = (summary.added + summary.removed + summary.type_changed).toLocaleString("ja-JP");
    elements["unclassified-count"].textContent = summary.unclassified.toLocaleString("ja-JP");
    elements["project-name"].textContent = state.project_name;
    elements["last-checked"].textContent = `最終確認 ${new Date(state.generated_at).toLocaleTimeString("ja-JP")}`;
    elements["map-status"].textContent = statusLabel(state.validation_result);
    elements["map-status"].className = `status-pill ${statusClass(state.validation_result)}`;
    elements["verification-meta"].textContent = state.verified_at
      ? `最終検証 ${state.verified_at} / ${state.verified_by}`
      : "構造の基準線はまだ確定していません。";

    const issues = [];
    if (state.validation_result === "DIRECTORY_MAP_DRIFT_DETECTED") {
      issues.push(`基準線との差分があります。追加${summary.added}件、削除${summary.removed}件です。`);
    }
    if (state.missing_declared.length) issues.push(`登録済みの必須候補が${state.missing_declared.length}件見つかりません。`);
    if (state.warnings.length) issues.push(`読み取り警告が${state.warnings.length}件あります。`);
    elements.alert.hidden = issues.length === 0;
    elements.alert.textContent = issues.join(" ");
  }

  async function fetchState() {
    if (!token) throw new Error("アクセス用トークンがありません。起動時に表示されたURLを使用してください。");
    const response = await fetch(`/api/state?token=${encodeURIComponent(token)}`, { cache: "no-store" });
    if (!response.ok) throw new Error(response.status === 403 ? "アクセス用トークンが無効です。" : `構造情報を取得できませんでした (${response.status})。`);
    return response.json();
  }

  async function refresh() {
    try {
      const state = await fetchState();
      elements["live-indicator"].textContent = "LIVE";
      elements["live-indicator"].className = "live-indicator connected";
      const revision = `${state.structure_hash}:${state.validation_result}:${state.summary.unclassified}`;
      currentState = state;
      updateSummary(state);
      if (revision !== renderedRevision) {
        renderedRevision = revision;
        renderTree();
        if (selectedPath) {
          const selected = [...state.entries, ...state.removed_entries].find((entry) => entry.path === selectedPath);
          if (selected) selectEntry(selected);
        }
      }
    } catch (error) {
      elements["live-indicator"].textContent = "切断";
      elements["live-indicator"].className = "live-indicator disconnected";
      elements.alert.hidden = false;
      elements.alert.textContent = error instanceof Error ? error.message : String(error);
    }
  }

  elements.search.addEventListener("input", renderTree);
  elements["role-filter"].addEventListener("change", renderTree);
  elements["changes-only"].addEventListener("change", renderTree);
  elements["expand-all"].addEventListener("click", () => elements.tree.querySelectorAll("details").forEach((item) => { item.open = true; }));
  elements["collapse-all"].addEventListener("click", () => elements.tree.querySelectorAll("details").forEach((item) => { item.open = false; }));

  refresh();
  window.setInterval(refresh, 2000);
})();
