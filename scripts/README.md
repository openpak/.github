# scripts

`dedup-lint.py` is the CI guard against player-data duplication (board card openpak/prds#131, phase 10). A console
adapter keeps console ids, credentials and protocol state; a player's name, display name, nickname, email, country,
birthday, language, timezone and Mii live in the account core. The lint reads every `CREATE TABLE`, `ALTER TABLE ... ADD`,
Prisma model and EF Core migration in a repo and fails on an identity-looking column that is not in the repo's
`.dedup-allow`.

Use it from a repo with a 10-line workflow (also runs on pull requests and pushes to the default branch):

```yaml
name: dedup-lint
on:
  pull_request:
  push:
    branches: [main, master]
  workflow_dispatch:
permissions:
  contents: read
jobs:
  lint:
    uses: openpak/.github/.github/workflows/dedup-lint.yml@main
```

`.dedup-allow` at the repo root: `table.column  # reason`, one per line, the reason is mandatory (game data, a
per-network field, a cache of the core that is watched by `openpak-dedup-check`). Locally: `python3 scripts/dedup-lint.py <repo>`;
self-test: `scripts/tests/dedup-lint-test.sh`.
