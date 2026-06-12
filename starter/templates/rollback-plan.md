# Rollback Plan Template

Use this template when a change may affect production users, data, security,
billing, infrastructure, or release behavior.

## Target Change

<!-- What change would be rolled back? -->

## Rollback Trigger

<!-- What evidence means rollback should be considered? -->

-

## Rollback Method

<!-- How exactly can the change be disabled, reverted, or mitigated? -->

```text
[commands, feature flag steps, deployment steps, or manual recovery steps]
```

## Data Impact

- [ ] No data change is involved.
- [ ] Data can be restored.
- [ ] Data cannot be fully restored.

Notes:

-

## Verification After Rollback

<!-- What proves rollback worked? -->

```text
[commands, monitoring checks, manual checks, or expected symptoms]
```

## Owner

<!-- Who decides and who performs rollback? -->

- Decision owner:
- Operator:
- Communication channel:
