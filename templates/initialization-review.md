# Initialization Review Template

初期設定を通常タスクへ進められる状態にする前のレビューです。
`docs/INITIALIZATION_REVIEW.md` として保存します。

## Review Summary

Initialization Decision: Not Ready / Ready
- Initialization track: Discovery / Build-ready
- Review date:
- Reviewer:

## Product Understanding

- [ ] 作りたいものをユーザーの言葉から要約した
- [ ] 解決したい問題を記録した
- [ ] 対象ユーザーの確度を記録した
- [ ] 提供価値の確度を記録した
- [ ] 収益化が未確定の場合、UnknownまたはHypothesisとして記録した
- [ ] MVPまたは最初の検証対象を記録した
- [ ] Non-goalsを記録した

## Uncertainty Handling

- [ ] Confirmed、Hypothesis、Unknown、Deferredを区別した
- [ ] Hypothesisを確定事項として扱っていない
- [ ] UnknownをAIが勝手に補完していない
- [ ] 最初のタスクを妨げる不明点が残っていない
- [ ] 残る不明点の解決方法を記録した

## Project Documents

- [ ] `docs/PROJECT_BRIEF.md` を作成した
- [ ] `docs/ROADMAP.md` を現在の成熟段階に合わせた
- [ ] `docs/PROJECT_STATUS.md` を初期化した
- [ ] `.ai-workflow/directory-map.json` に予定構造、責務、境界を記録した
- [ ] `docs/DIRECTORY_MAP.md` をJSON正本から生成した
- [ ] 構造チェッカーが `DIRECTORY_MAP_PROVISIONAL` または `DIRECTORY_MAP_VERIFIED` を返した
- [ ] `AGENTS.md` をプロジェクト固有のルールへ更新した

## Development Readiness

- [ ] 技術方針の確定部分と暫定部分を区別した
- [ ] テストまたは検証方法を記録した
- [ ] データ、セキュリティ、プライバシーの不明点を記録した
- [ ] 最初のタスク候補が1つの目的に絞られている
- [ ] 最初のタスク候補の対象外が明確である
- [ ] 最初のタスクで期待する証拠が明確である

## Remaining Hypotheses and Unknowns

-

## First Task Candidate

- Goal:
- Why now:
- Scope:
- Out of scope:
- Expected evidence:

## User Approval

初期設定の`ready`は、すべてが確定した意味ではありません。
現在の仮説と不明点を理解したうえで、最初のタスクを安全に開始できるという承認です。

- [ ] ユーザーへPROJECT_BRIEFの要点を提示した
- [ ] ユーザーへROADMAPの最初のフェーズを提示した
- [ ] ユーザーへAGENTS.mdの主要ルールを提示した
- [ ] ユーザーへProject Structure Mapの予定構造と責務を提示した
- [ ] ユーザーへ残る仮説と不明点を提示した
- [ ] ユーザーから明示的な開始承認を得た

Approval evidence:

- Approved by:
- Approved at:
- Confirmation summary:

## State Transition

- [ ] 承認前は `initialization_status=in_progress`、`user_approved=false` のままにした
- [ ] 承認後だけ `initialization_status=ready`、`user_approved=true` に変更した
- [ ] 判定スクリプトが `INITIALIZATION_READY` を返した

判定欄は、ユーザーの明示承認を記録した後だけ、行全体を正確に
`Initialization Decision: Ready` へ置き換えます。
