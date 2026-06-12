# Security Review Template

Use this template for Strict mode tasks and for any change that may affect
secrets, access control, personal data, logging, external services, or production
configuration.

## Target Change

<!-- What change is being reviewed? -->

## Data and Secrets

- [ ] No API keys, tokens, passwords, cookies, or private keys are included.
- [ ] No personal, customer, or internal confidential data is included.
- [ ] Logs and screenshots were checked for sensitive information.
- [ ] New or changed logs avoid sensitive values.

Notes:

-

## Access Control

- [ ] Authentication behavior is unchanged or described below.
- [ ] Authorization behavior is unchanged or described below.
- [ ] Admin-only behavior remains protected.
- [ ] User-to-user data isolation is not weakened.

Notes:

-

## External Services and Dependencies

- [ ] No new external service is introduced, or it is described below.
- [ ] No new dependency is introduced, or it is described below.
- [ ] Data sent to external services is understood.
- [ ] Failure behavior of external services is understood.

Notes:

-

## Runtime and Configuration

- [ ] Production configuration impact is understood.
- [ ] Environment variable changes are documented.
- [ ] Deployment or hosting changes are documented.
- [ ] Monitoring or manual checks are defined where needed.

Notes:

-

## Risk Decision

<!-- What risk remains, and who accepts it? -->

- Remaining risk:
- Accepted by:
- Date:
