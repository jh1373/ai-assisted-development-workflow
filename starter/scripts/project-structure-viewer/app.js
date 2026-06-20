(() => {
  "use strict";
  const params = new URLSearchParams(location.search);
  const token = params.get("token") || sessionStorage.getItem("project-atlas-token") || "";
  if (token) sessionStorage.setItem("project-atlas-token", token);
  if (params.has("token")) {
    params.delete("token");
    history.replaceState(null, "", location.pathname + (params.toString() ? "?" + params : ""));
  }
  const byId = (id) => document.getElementById(id);
  const els = Object.fromEntries([
    "live-indicator","map-status","alert","areas-count","semantic-coverage","passport-coverage","health-issues",
    "project-name","last-checked","atlas-layers","flow-select","flow-intro","flow-steps","lens-select","lens-intro",
    "lens-primary","lens-related","lens-avoid","search","role-filter","changes-only","tree-summary","tree",
    "detail-title","detail-path","detail-summary","passport-fields","detail-not-responsible","detail-when",
    "detail-dependencies","detail-boundaries","health-unexplained-count","health-generic-count","health-broken-count",
    "health-unexplained","health-generic","health-broken","verification-meta"
  ].map((id) => [id, byId(id)]));
  let state = null;
  let selectedPath = null;
  let revision = "";
  const layerLabels = {
    experience: "ユーザーが触れる画面", feature: "プロダクトの機能", data: "データと外部通信",
    platform: "自動化と運用基盤", workflow: "AIと人間の開発手順", documentation: "計画と判断の記録"
  };
  function statusLabel(value) {
    return {
      DIRECTORY_MAP_PROVISIONAL: "準備中",
      DIRECTORY_MAP_VERIFIED: "確認済み",
      DIRECTORY_MAP_DRIFT_DETECTED: "構成変更あり",
      DIRECTORY_MAP_INVALID: "設定エラー",
      DIRECTORY_MAP_CHECK_FAILED: "確認できません"
    }[value] || value;
  }
  function sourceLabel(value) {
    return {
      explicit: "このファイル専用の説明",
      "explicit-pattern": "登録したまとめ説明",
      inherited: "フォルダの説明を使用",
      convention: "共通ルールの説明",
      unclassified: "説明なし"
    }[value] || value;
  }
  function evidenceLabel(value) {
    return {
      "human-confirmed": "ユーザーまたは開発者が確認",
      "registered-when-created": "ファイル作成時に登録",
      "project-initialization": "初期設定で登録",
      convention: "共通ルールから判定"
    }[value] || value;
  }
  function importanceLabel(value) {
    return { "entry-point": "最初に見るファイル", core: "中心となるファイル", support: "補助ファイル" }[value] || value;
  }
  function make(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function switchView(name) {
    document.querySelectorAll(".view").forEach((view) => view.classList.toggle("active", view.id === "view-" + name));
    document.querySelectorAll(".tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.view === name));
  }
  function patternRegex(pattern) {
    const escaped = pattern.replace(/[.+^$(){}|[\]\\]/g, "\\$&").replace(/\*\*/g, "§§").replace(/\*/g, "[^/]*").replace(/§§/g, ".*").replace(/\?/g, ".");
    return new RegExp("^" + escaped + "$");
  }
  function entriesFor(pattern) {
    if (!state) return [];
    const base = pattern.endsWith("/**") ? pattern.slice(0, -3) : null;
    const regex = patternRegex(pattern);
    return state.entries.filter((entry) => entry.path === pattern || entry.path === base || regex.test(entry.path));
  }
  function openPath(pattern) {
    const entry = entriesFor(pattern)[0] || state?.entries.find((item) => item.path === pattern);
    switchView("explorer");
    if (entry) {
      selectedPath = entry.path;
      renderTree();
      selectEntry(entry);
      els.tree.querySelector('[data-path="' + CSS.escape(entry.path) + '"]')?.scrollIntoView({ block: "center" });
    } else {
      els.search.value = pattern;
      renderTree();
    }
  }
  function pathButton(path, summary) {
    const button = make("button", "path-card");
    button.type = "button";
    button.append(make("code", "", path));
    if (summary) button.append(make("span", "", summary));
    button.addEventListener("click", () => openPath(path));
    return button;
  }
  function renderAtlas() {
    const container = els["atlas-layers"];
    container.replaceChildren();
    const grouped = new Map();
    state.areas.forEach((area) => {
      if (!grouped.has(area.layer)) grouped.set(area.layer, []);
      grouped.get(area.layer).push(area);
    });
    Object.keys(layerLabels).forEach((layer) => {
      const areas = grouped.get(layer);
      if (!areas?.length) return;
      const lane = make("section", "atlas-lane");
      const heading = make("div", "lane-heading");
      heading.append(make("span", "lane-number", String(areas.length)), make("h3", "", layerLabels[layer]));
      lane.append(heading);
      const cards = make("div", "area-cards");
      areas.forEach((area) => {
        const card = make("button", "area-card");
        card.type = "button";
        card.append(make("span", "area-kicker", layerLabels[area.layer] || area.layer), make("h4", "", area.name), make("p", "", area.beginner_summary));
        const meta = make("div", "area-meta");
        meta.append(make("span", "", "含まれるファイル " + area.file_count + "個"), make("span", "", "最初に見るファイル " + area.entry_points_present.length + "個"));
        card.append(meta);
        if (area.depends_on.length) {
          const names = area.depends_on.map((id) => state.areas.find((item) => item.id === id)?.name || id);
          card.append(make("small", "", "関係する役割: " + names.join("、")));
        }
        card.addEventListener("click", () => openPath(area.resolved_paths[0] || area.paths[0]));
        cards.append(card);
      });
      lane.append(cards);
      container.append(lane);
    });
    if (!state.areas.length) container.append(make("p", "empty", "区域がまだ定義されていません。Project Initializationで役割区域を登録してください。"));
  }
  function fillSelect(select, values) {
    const previous = select.value;
    select.replaceChildren(...values.map((value) => {
      const option = make("option", "", value.name);
      option.value = value.id;
      return option;
    }));
    if (values.some((value) => value.id === previous)) select.value = previous;
  }
  function renderFlow() {
    const flow = state.flows.find((item) => item.id === els["flow-select"].value) || state.flows[0];
    els["flow-intro"].textContent = flow?.beginner_summary || "処理の流れがまだ登録されていません。";
    els["flow-steps"].replaceChildren();
    flow?.steps.forEach((step, index) => {
      const item = make("li", "flow-step");
      item.append(make("span", "step-number", String(index + 1)), pathButton(step.path, step.summary));
      els["flow-steps"].append(item);
    });
  }
  function renderLensColumn(element, paths, emptyText) {
    element.replaceChildren();
    if (!paths.length) element.append(make("p", "empty-small", emptyText));
    paths.forEach((path) => element.append(pathButton(path)));
  }
  function renderLens() {
    const lens = state.task_lenses.find((item) => item.id === els["lens-select"].value) || state.task_lenses[0];
    els["lens-intro"].textContent = lens?.beginner_summary || "この作業に対応する案内はまだ登録されていません。";
    renderLensColumn(els["lens-primary"], lens?.primary_paths || [], "最初に見る場所は未登録です。");
    renderLensColumn(els["lens-related"], lens?.related_paths || [], "関連場所は未登録です。");
    renderLensColumn(els["lens-avoid"], lens?.avoid_paths || [], "除外範囲は未登録です。");
  }
  function buildHierarchy(entries) {
    const root = { children: new Map(), entry: null };
    entries.forEach((entry) => {
      let cursor = root;
      entry.path.split("/").forEach((part, index, parts) => {
        if (!cursor.children.has(part)) cursor.children.set(part, { children: new Map(), entry: null });
        cursor = cursor.children.get(part);
        if (index === parts.length - 1) cursor.entry = entry;
      });
    });
    return root;
  }
  function entryMatches(entry) {
    const query = els.search.value.trim().toLocaleLowerCase("ja");
    if (query && ![entry.path, entry.beginner_summary, entry.responsibility].join(" ").toLocaleLowerCase("ja").includes(query)) return false;
    const filter = els["role-filter"].value;
    if (filter === "explicit" && !entry.role_source.startsWith("explicit")) return false;
    if (!["all", "explicit"].includes(filter) && entry.role_source !== filter) return false;
    return !(els["changes-only"].checked && entry.change === "unchanged");
  }
  function nodeMatches(node) {
    return (node.entry && entryMatches(node.entry)) || [...node.children.values()].some(nodeMatches);
  }
  function treeLine(entry, name) {
    const line = make("span", "entry-line");
    line.append(make("span", "entry-name", name), make("span", "entry-summary", entry.beginner_summary));
    const label = sourceLabel(entry.role_source);
    line.append(make("span", "badge " + entry.role_source, label));
    if (entry.change !== "unchanged") line.append(make("span", "badge changed", entry.change === "added" ? "追加" : "削除"));
    return line;
  }
  function renderTreeNode(name, node, depth) {
    if (!nodeMatches(node)) return null;
    const entry = node.entry || { path: name, kind: "directory", beginner_summary: "親フォルダ", role_source: "inherited", change: "unchanged" };
    const isDirectory = entry.kind === "directory" || node.children.size;
    if (isDirectory) {
      const details = make("details", "");
      details.open = depth < 1;
      details.dataset.path = entry.path;
      const summary = make("summary", "");
      summary.append(treeLine(entry, name));
      summary.addEventListener("click", () => selectEntry(entry));
      details.append(summary);
      [...node.children.entries()].sort(([a],[b]) => a.localeCompare(b, "ja")).forEach(([childName, childNode]) => {
        const child = renderTreeNode(childName, childNode, depth + 1);
        if (child) details.append(child);
      });
      return details;
    }
    const button = make("button", "file-row");
    button.type = "button";
    button.dataset.path = entry.path;
    button.append(treeLine(entry, name));
    button.addEventListener("click", () => selectEntry(entry));
    return button;
  }
  function renderTree() {
    const entries = [...state.entries, ...state.removed_entries];
    const hierarchy = buildHierarchy(entries);
    const fragment = document.createDocumentFragment();
    let shown = 0;
    [...hierarchy.children.entries()].forEach(([name, node]) => {
      const child = renderTreeNode(name, node, 0);
      if (child) { shown += 1; fragment.append(child); }
    });
    els.tree.replaceChildren(fragment);
    els["tree-summary"].textContent = entries.length + "項目中、条件に一致するトップレベル項目は" + shown + "件です。";
    if (!shown) els.tree.append(make("p", "empty", "条件に一致する項目がありません。"));
    if (selectedPath) els.tree.querySelector('[data-path="' + CSS.escape(selectedPath) + '"]')?.classList.add("selected");
  }
  function replaceList(element, values, emptyText = "登録されていません") {
    element.replaceChildren(...(values.length ? values : [emptyText]).map((value) => make("li", "", value)));
  }
  function selectEntry(entry) {
    selectedPath = entry.path;
    els.tree.querySelectorAll(".selected").forEach((node) => node.classList.remove("selected"));
    els.tree.querySelector('[data-path="' + CSS.escape(entry.path) + '"]')?.classList.add("selected");
    els["detail-title"].textContent = entry.display_name || entry.path.split("/").pop();
    els["detail-path"].textContent = entry.path;
    els["detail-summary"].textContent = entry.beginner_summary;
    const fields = [
      ["このファイルがすること", entry.responsibility],
      ["どの役割に属するか", state.areas.find((item) => item.id === entry.area)?.name || "役割グループ未設定"],
      ["このファイルの位置づけ", importanceLabel(entry.importance)],
      ["この説明はどこから来たか", sourceLabel(entry.role_source) + " / " + evidenceLabel(entry.evidence)],
      ["受け取るもの", (entry.inputs || []).join(" / ") || "特になし"],
      ["ほかへ渡すもの", (entry.outputs || []).join(" / ") || "特になし"]
    ];
    els["passport-fields"].replaceChildren(...fields.map(([term, value]) => {
      const row = make("div", "passport-row");
      row.append(make("dt", "", term), make("dd", "", value));
      return row;
    }));
    replaceList(els["detail-not-responsible"], entry.not_responsible_for || []);
    replaceList(els["detail-when"], entry.when_to_change || []);
    replaceList(els["detail-dependencies"], entry.depends_on || []);
    replaceList(els["detail-boundaries"], entry.boundaries || []);
  }
  function healthList(element, values, formatter = (value) => value) {
    element.replaceChildren();
    if (!values.length) element.append(make("p", "healthy", "問題はありません"));
    values.slice(0, 30).forEach((value) => element.append(make("div", "health-item", formatter(value))));
    if (values.length > 30) element.append(make("p", "muted", "ほか" + (values.length - 30) + "件"));
  }
  function renderHealth() {
    const health = state.health;
    els["health-unexplained-count"].textContent = health.unexplained_paths.length;
    els["health-generic-count"].textContent = health.generic_passports.length;
    els["health-broken-count"].textContent = health.broken_references.length;
    healthList(els["health-unexplained"], health.unexplained_paths);
    healthList(els["health-generic"], health.generic_passports);
    healthList(els["health-broken"], health.broken_references, (item) => item.source + " → " + item.target);
  }
  function renderAll() {
    const explained = state.entries.length - state.health.unexplained_paths.length;
    const individual = state.entries.filter((entry) => entry.kind === "file" && entry.role_source === "explicit").length;
    els["areas-count"].textContent = state.areas.length + "個";
    els["semantic-coverage"].textContent = explained + "個";
    els["passport-coverage"].textContent = individual + "個";
    els["health-issues"].textContent = state.health.issue_count + "個";
    els["project-name"].textContent = state.project_name;
    els["last-checked"].textContent = "最終確認 " + new Date(state.generated_at).toLocaleTimeString("ja-JP");
    els["map-status"].textContent = statusLabel(state.validation_result);
    els["verification-meta"].textContent = state.verified_at ? "構成の最終確認 " + state.verified_at + " / 確認者 " + state.verified_by : "プロジェクト構成はまだ最終確認されていません";
    fillSelect(els["flow-select"], state.flows);
    fillSelect(els["lens-select"], state.task_lenses);
    renderAtlas(); renderFlow(); renderLens(); renderTree(); renderHealth();
    const issues = [];
    if (state.validation_result === "DIRECTORY_MAP_DRIFT_DETECTED") issues.push("承認済み構造との差分があります。");
    if (state.health.broken_references.length) issues.push("壊れた意味参照があります。");
    if (state.summary.unclassified) issues.push("説明できない項目があります。");
    els.alert.hidden = !issues.length;
    els.alert.textContent = issues.join(" ");
  }
  async function refresh() {
    try {
      if (!token) throw new Error("アクセス用トークンがありません。起動時に表示されたURLを使用してください。");
      const response = await fetch("/api/state?token=" + encodeURIComponent(token), { cache: "no-store" });
      if (!response.ok) throw new Error(response.status === 403 ? "アクセス用トークンが無効です。" : "状態を取得できません。");
      const next = await response.json();
      const nextRevision = JSON.stringify([next.structure_hash, next.areas, next.flows, next.task_lenses, next.health]);
      state = next;
      els["live-indicator"].textContent = "自動更新中";
      els["live-indicator"].className = "pill connected";
      if (nextRevision !== revision) { revision = nextRevision; renderAll(); }
      else els["last-checked"].textContent = "最終確認 " + new Date(next.generated_at).toLocaleTimeString("ja-JP");
    } catch (error) {
      els["live-indicator"].textContent = "接続エラー";
      els["live-indicator"].className = "pill disconnected";
      els.alert.hidden = false;
      els.alert.textContent = error.message;
    }
  }
  document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => switchView(tab.dataset.view)));
  els["flow-select"].addEventListener("change", renderFlow);
  els["lens-select"].addEventListener("change", renderLens);
  els.search.addEventListener("input", renderTree);
  els["role-filter"].addEventListener("change", renderTree);
  els["changes-only"].addEventListener("change", renderTree);
  refresh();
  setInterval(refresh, 2000);
})();
