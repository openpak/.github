# Contributing to OpenPak

Thanks for helping. OpenPak is in public alpha. The most useful things right now are clear bug
reports and test results from real consoles and games.

## Reporting problems

- **A game doesn't work:** open an issue in the repository that serves it (the title's page on
  [openpak.org/titles](https://openpak.org/titles) says which service it uses). Include the
  console or emulator, firmware version, game version and region, the error code shown, and
  what you did just before it happened.
- **A website or account problem:** open an issue in [`website`](https://github.com/openpak/website)
  or [`account`](https://github.com/openpak/account).
- **Not sure where it goes:** use [Help](https://openpak.org/help) on the site once you are
  signed in, and we'll move it to the right place.
- **Security issues:** never in public. See [SECURITY](SECURITY.md).

Never attach game files, firmware, keys, `prod.keys`, PRODINFO or console dumps. Logs and
screenshots are welcome.

## Contributing code

1. Open an issue first for anything bigger than a small fix, so we can agree on the approach.
2. Fork, branch, and keep each pull request to one change.
3. Run the repository's tests (`go test ./...` for the Go services; each README says how).
4. Write commit messages in the imperative, describing what changed and why.

Each repository is independent and has its own README, `CHANGELOG.md` and build steps. The
shared conventions and playbooks are in [`docs`](https://github.com/openpak/docs).

### Clean room

Some implementations of the same services are source-available but not free software. Don't
copy, port or paraphrase their code into OpenPak, and don't submit code you don't have the
right to license. Facts are fine: ports, hostnames, wire formats and error codes. Say where they
come from in the pull request.

### Licence

OpenPak's own code is AGPL-3.0-only. Forks keep their upstream licence (each repository's
LICENSE says which). By opening a pull request you agree that your contribution is released
under the licence of that repository.

## Conduct

Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md).
