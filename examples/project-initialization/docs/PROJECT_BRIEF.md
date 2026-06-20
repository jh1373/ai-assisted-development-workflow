# Project Brief: AI Meal Planning Experiment

## Document Status

- Initialization track: Discovery
- Last confirmed by user: 2026-06-20
- Last updated: 2026-06-20

## Product Idea

Status: Confirmed

AIを使って、毎日の献立を考える負担を減らすサービスを試作する。

## Problem

Status: Hypothesis

忙しい人は、毎日献立を考えることに負担を感じている。

## Target Users

Status: Hypothesis

平日に自炊するが、献立を考える時間を減らしたい会社員。

## Value Proposition

Status: Hypothesis

条件を入力すると、短時間で現実的な献立候補を得られる。

## Core User Flow

Status: Hypothesis

1. 人数、避けたい食材、調理時間を入力する
2. AIが献立候補を提示する
3. ユーザーが候補を採用または調整する

## Monetization

Status: Unknown

月額課金を候補とするが、継続利用されるか確認するまで確定しない。

## MVP or First Experiment

Status: Confirmed

保存、認証、課金を含まない献立提案プロトタイプを作り、5人に操作してもらう。

## Non-goals

- 認証
- 決済
- 食材購入サービスとの連携
- 栄養指導
- 医療用途

## Success Signals

Status: Hypothesis

- 5人中3人以上が提案結果を理解できる
- 5人中2人以上が再利用したいと回答する
- 献立取得までの操作で重大な迷いが発生しない

## Constraints

- 個人開発
- 最初は公開しない
- 実在ユーザーの個人情報を保存しない

## Data, Security, and Privacy

Status: Confirmed

- 扱う予定のデータ: 人数、避けたい食材、調理時間
- 個人情報: 保存しない
- 認証・権限: 初期検証では実装しない
- 外部送信: AI APIへ入力条件を送る可能性がある
- 現時点の注意点: APIへ個人情報を入力させない

## Technical Direction

Status: Hypothesis

- Runtime / platform: Web browser
- Main stack: 小さなWebアプリとして検討
- Data storage: 初期検証では永続化しない
- Deployment: Deferred
- Testing: 入力検証と主要UIのテスト
- Rationale: インストールなしで試してもらえるため

## Confirmed

- 献立提案の価値を先に検証する
- 初期検証では認証、保存、課金を作らない
- 個人情報を保存しない

## Hypotheses

| Hypothesis | Why it may be true | How to validate | Review timing |
|---|---|---|---|
| 忙しい会社員に献立決定の負担がある | ユーザー自身の経験 | 5人への操作確認と質問 | Phase 1終了時 |
| AI提案を再利用したい | 提案速度に価値がある可能性 | 再利用意向を確認 | Phase 1終了時 |

## Unknowns

| Unknown | Does it block the first task? | How to resolve |
|---|---|---|
| 最適な収益モデル | no | 継続利用意向の確認後に検討 |
| 本番デプロイ先 | no | MVP定義後に比較 |

## Deferred

| Decision | Why deferred | Revisit trigger |
|---|---|---|
| 認証方式 | 初期検証に不要 | 保存機能を採用するとき |
| 課金方式 | 支払い意思が未検証 | 継続利用が確認できたとき |

## First Validation Question

ユーザーは、短い条件入力から得た献立候補を理解し、再利用したいと感じるか。

## First Task Candidate

- Goal: 入力から固定サンプル献立を表示する操作可能な試作品を作る
- Scope: 条件入力、提案表示、入力エラー
- Out of scope: AI API、認証、保存、課金、公開
- Evidence expected: UIテストと5人に見せられる操作手順

## User Confirmation

- [x] AIの理解をユーザーへ提示した
- [x] ConfirmedとHypothesisをユーザーが確認した
- [x] UnknownとDeferredをユーザーが確認した
- [x] 最初の検証対象をユーザーが確認した
