# OpenPak

**An open replacement online network for Nintendo, Xbox and PlayStation consoles, and for the
emulators that run their games.**

The official servers for these consoles are shutting down or are already gone. OpenPak runs the
services that let those consoles and their games go online again: accounts, friends, presence,
matchmaking, cloud saves, news and shops. You keep the real console firmware and the real games.
Only the network side is replaced.

[openpak.org](https://openpak.org) · [Docs](https://docs.openpak.org) · [Status](https://status.openpak.org) ·
[Titles](https://openpak.org/titles) · [Features](https://openpak.org/features) ·
[Downloads](https://openpak.org/downloads) ·
[Discord](https://discord.gg/nMhjnsB6F6)

**New here? Read [how OpenPak fits together](https://github.com/openpak/.github/blob/main/profile/ARCHITECTURE.md).**

> [!WARNING]
> OpenPak is in **public alpha**. Things will break. Accounts, saves and links may be reset
> without notice, and there is no uptime promise. Please report what you find.

## Where each platform stands

| Platform | State | What you need |
| --- | --- | --- |
| Nintendo Switch | Working: accounts, console link, friends, Nintendo Switch Online, avatars. Presence, invitations, matchmaking and cloud saves are partial | A console with Atmosphère and [OpenPak Switch Patcher](https://github.com/openpak/switch-patcher/releases/latest), or the Harbor emulator |
| Wii U and 3DS | Beta: accounts, friends, NAT check. Miiverse, SpotPass and eShop are alpha | [OpenPak Wii U Patcher](https://github.com/openpak/wiiu-patcher) (Aroma) or [OpenPak 3DS Patcher](https://github.com/openpak/3ds-patcher) (Luma) |
| Wii and DS | Beta: Nintendo Wi-Fi Connection | The [OpenPak Wii Patcher](https://github.com/openpak/wii-patcher) or [OpenPak DS Patcher](https://github.com/openpak/ds-patcher) |
| Xbox | In development | [OpenPak Xbox Patcher](https://github.com/openpak/xbox-patcher), not available yet |
| Xbox 360 | In development | [OpenPak Xbox 360 Patcher](https://github.com/openpak/x360-patcher), not available yet |
| PlayStation 3 | In development | [OpenPak PS3 Patcher](https://github.com/openpak/ps3-patcher), not available yet |
| PSP, PS2, Vita, later consoles | Planned | |

Per-game status is on [openpak.org/titles](https://openpak.org/titles). Each game shows what
was tested, on which hardware, and what does not work yet.

## Emulators

OpenPak keeps its own emulator forks. They boot the real console firmware (HOME menu, system
applets) and go online through OpenPak like a real console would.

| Emulator | Console | Based on |
| --- | --- | --- |
| [Harbor](https://github.com/openpak/harbor) | Switch | Eden |
| [Quay](https://github.com/openpak/quay) | Wii U | Cemu |
| [Marina](https://github.com/openpak/marina) | Wii, GameCube | Dolphin |
| [Azahar](https://github.com/openpak/azahar) | 3DS | Azahar |
| [melonDS](https://github.com/openpak/melonds) | DS | melonDS |
| [Wharf](https://github.com/openpak/wharf) | Xbox 360 | Xenia Edge |
| [Berth](https://github.com/openpak/berth) | Xbox | xemu |
| [Pier](https://github.com/openpak/pier) | PlayStation 3 | RPCS3 |

## Finding your way around

There is one repository per service. Browse them by topic:

- Platform: [`switch`](https://github.com/orgs/openpak/repositories?q=topic%3Aswitch) ·
  [`wiiu`](https://github.com/orgs/openpak/repositories?q=topic%3Awiiu) ·
  [`3ds`](https://github.com/orgs/openpak/repositories?q=topic%3A3ds) ·
  [`wii`](https://github.com/orgs/openpak/repositories?q=topic%3Awii) ·
  [`ds`](https://github.com/orgs/openpak/repositories?q=topic%3Ads) ·
  [`xbox`](https://github.com/orgs/openpak/repositories?q=topic%3Axbox) ·
  [`xbox360`](https://github.com/orgs/openpak/repositories?q=topic%3Axbox360) ·
  [`ps3`](https://github.com/orgs/openpak/repositories?q=topic%3Aps3) ·
  [`core`](https://github.com/orgs/openpak/repositories?q=topic%3Acore) (shared by every console)
- Kind: [`infra`](https://github.com/orgs/openpak/repositories?q=topic%3Ainfra) (network services) ·
  [`game-server`](https://github.com/orgs/openpak/repositories?q=topic%3Agame-server) ·
  [`client`](https://github.com/orgs/openpak/repositories?q=topic%3Aclient) (what runs on the console or your phone) ·
  [`emulator`](https://github.com/orgs/openpak/repositories?q=topic%3Aemulator) ·
  [`tool`](https://github.com/orgs/openpak/repositories?q=topic%3Atool) ·
  [`library`](https://github.com/orgs/openpak/repositories?q=topic%3Alibrary)

Good places to start:

- [`account`](https://github.com/openpak/account): the account core. It knows nothing about consoles; every platform adapter talks to it.
- [`website`](https://github.com/openpak/website): openpak.org, the account portal and the title catalogue.
- [`nx-baas`](https://github.com/openpak/nx-baas): the Switch adapter (BAAS, Nintendo Account, eShop front).
- [`nex`](https://github.com/openpak/nex): the shared NEX/PRUDP game-server host for Wii U, 3DS and Switch titles.
- [`app`](https://github.com/openpak/app): the companion app for Android and iOS (account, friends, presence, invitations).
- [`docs`](https://github.com/openpak/docs): the source of [docs.openpak.org](https://docs.openpak.org), for players, contributors and self-hosters.

## Standing on shoulders

OpenPak builds on the work of [Pretendo Network](https://github.com/PretendoNetwork),
[WiiLink](https://github.com/WiiLink24), [Kinnay](https://github.com/kinnay) (NintendoClients
and the Game Server List), [nex-go](https://github.com/PretendoNetwork/nex-go), and the
upstream emulator projects listed above. Forked code keeps its original licence and credits.

## Rules we keep

- **No game or firmware files.** We never ship games, firmware, keys or console data. Use your own console and your own games.
- **The console, not the game.** On Switch, Wii U and 3DS, OpenPak changes where the console connects and leaves game code alone. Wii and DS games have no other way in, so their patchers redirect each game.
- **Clean room.** Implementations we may not legally copy are used only for facts (ports, wire formats), never for code.
- **Copyleft.** OpenPak's own code is AGPL-3.0. Anyone may run their own network.

## Get involved

- Report a bug or a game that doesn't work: open an issue in the repository for that service, or use [Help](https://openpak.org/help) once you are signed in.
- Contribute: read [CONTRIBUTING](https://github.com/openpak/.github/blob/main/CONTRIBUTING.md).
- Security issues: read [SECURITY](https://github.com/openpak/.github/blob/main/SECURITY.md) and report them privately, never in a public issue.
- Chat with the community and the developers on [Discord](https://discord.gg/nMhjnsB6F6).
- Contact: [contact@openpak.org](mailto:contact@openpak.org)

<sub>OpenPak is an independent community project. It is not affiliated with, endorsed by or
sponsored by Nintendo, Microsoft or Sony. All trademarks belong to their owners.</sub>
