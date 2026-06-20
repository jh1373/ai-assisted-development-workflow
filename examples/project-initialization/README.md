# Example: Vague Idea to Initialization Ready

「AIで献立を考えるものを作ってみたい」という曖昧なアイデアから、最初の検証タスクを安全に開始できる状態まで整理した例です。

この例では、対象ユーザーと収益化を確定していません。
未確定事項をHypothesisまたはUnknownとして残し、Discovery Trackを選んでいます。

## Flow

```text
Idea
→ user and AI discussion
→ PROJECT_BRIEF
→ Discovery ROADMAP
→ project-specific AGENTS
→ PROJECT_STATUS and provisional DIRECTORY_MAP
→ INITIALIZATION_REVIEW
→ explicit user approval
→ INITIALIZATION_READY
```

## Files

- `docs/PROJECT_BRIEF.md`: 確定事項、仮説、不明点、Deferred
- `docs/ROADMAP.md`: Discoveryから始まる全体計画
- `docs/PROJECT_STATUS.md`: 初期設定後の現在地
- `docs/DIRECTORY_MAP.md`: 初期構築前の暫定構成
- `AGENTS.md`: 初期設定で追加したプロジェクト固有ルール
- `docs/INITIALIZATION_REVIEW.md`: ユーザー承認と開始判断
- `.ai-workflow/project-state.conf`: 承認後の機械判定状態

これは事業仮説の正しさを示す例ではありません。
仮説を確定事項として扱わず、最初に何を検証するかを決める例です。
