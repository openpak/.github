#!/usr/bin/env python3
"""dedup-lint: fail when a console adapter adds a table or column that stores player identity as a first source.

Board card openpak/prds#131 (phase 10). A console network service is a thin adapter over the account core: it keeps
console ids, credentials and protocol state, never the player's name, display name, nickname, email, country,
birthday, language, timezone or Mii. This script scans a repo for table and column definitions and fails on any
identity-looking column that is not named in the repo's allowlist.

Scans (git-tracked files only): *.sql, *.prisma, and every other source file for CREATE TABLE / ALTER TABLE ... ADD
statements (Go, Python, C#, TypeScript and JS repos embed their schema as strings) plus EF Core CreateTable /
AddColumn calls.

Allowlist: `.dedup-allow` at the repo root, one entry per line, `table.column  # reason`. `*` works for either side
(`*.mii_name`). A reason after `#` is mandatory (a legitimate case is game data, a per-network field, a cache that is
written only from core). Entries that match nothing are reported as stale (a warning; `--strict-stale` fails).

Usage: dedup-lint.py [repo-dir]    exit 0 clean, 1 findings, 2 usage/allowlist error
"""
import fnmatch, re, subprocess, sys
from pathlib import Path

# A column is identity when one of its words says so. A bare "name" is identity in a player table (users, accounts, profiles ...); "name" after a person word always is;
# file_name, title_name, host_name and the like are not.
WORDS = {"email", "mail", "country", "birthday", "birthdate", "birth", "dob", "language", "lang", "locale", "timezone",
         "tz", "mii", "nickname", "nick", "username", "displayname", "firstname", "lastname", "fullname", "realname",
         "handle", "gamertag", "gamertags", "pnid", "gender", "profilename", "screenname", "playername"}
PERSON = {"player", "user", "display", "first", "last", "nick", "profile", "account", "owner", "screen", "real", "full",
          "gamer", "friend", "author", "maker", "member", "person", "character"}
FLAGS = {"is", "has", "show", "notify", "allow", "can", "hide", "enable", "enabled"}
KEYWORDS = {"primary", "foreign", "unique", "constraint", "check", "index", "key", "exclude", "like", "fulltext", "period"}
SRC_SKIP = re.compile(r"(^|/)(vendor|node_modules|third_party|testdata|\.github)/|_test\.go$|\.(md|json|png|jpg|lock|sum)$")


def words(col):
    col = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", col)
    return [w.lower() for w in re.split(r"[^A-Za-z0-9]+", col) if w]


# A bare `name` column is identity only in a table that holds people (courses.name, cursors.name are not).
PLAYER_TABLE = re.compile(r"(^|_)(users?|accounts?|players?|profiles?|pnids?|mii|makers?|members?|characters?|friends?|persons?|identit(y|ies)|gamers?)(_|$)", re.I)


def is_identity(col, table=""):
    w = words(col)
    if w and w[0] in FLAGS:  # is_birthday_visible, show_country: a switch about the value, not the value
        return False
    j = "".join(w)
    if j in WORDS or any(x in WORDS for x in w):
        return True
    if "name" in w:
        i = w.index("name")
        if i == 0 and len(w) == 1:
            return bool(PLAYER_TABLE.search(table))
        return i > 0 and w[i - 1] in PERSON
    return False


def strip_comments(s):
    return re.sub(r"--[^\n]*|/\*.*?\*/", "", s, flags=re.S)


def split_top(body):
    out, depth, cur, q = [], 0, [], None
    for ch in body:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
            continue
        if ch in "'\"`":
            q = ch
            cur.append(ch)
        elif ch == "(":
            depth += 1
            cur.append(ch)
        elif ch == ")":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return out


NAME = r'[`"\[]?([A-Za-z_][\w$]*)[`"\]]?'
CREATE = re.compile(r"CREATE\s+(?:UNLOGGED\s+|TEMP(?:ORARY)?\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:" + NAME + r"\s*\.\s*)?" + NAME + r"\s*\(", re.I)
ALTER = re.compile(r"ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?:ONLY\s+)?(?:" + NAME + r"\s*\.\s*)?" + NAME + r"([^;]*)", re.I)
ADD = re.compile(r"ADD\s+(?:COLUMN\s+)?(?:IF\s+NOT\s+EXISTS\s+)?" + NAME, re.I)
EF_TABLE = re.compile(r'CreateTable\(\s*name:\s*"(\w+)"')
EF_COL = re.compile(r'(\w+)\s*=\s*table\.Column<[^>]+>\(\s*(?:type:[^,]+,\s*)?(?:name:\s*"(\w+)")?')
EF_ADD = re.compile(r'AddColumn<[^>]+>\(\s*name:\s*"(\w+)",\s*table:\s*"(\w+)"')
PRISMA_MODEL = re.compile(r"^model\s+(\w+)\s*\{(.*?)^\}", re.M | re.S)


def scan_text(text, path):
    found = []  # (table, column, where)
    clean = strip_comments(text)
    for m in CREATE.finditer(clean):
        table = m.group(2).lower()
        depth, i = 1, m.end()
        while i < len(clean) and depth:
            depth += {"(": 1, ")": -1}.get(clean[i], 0)
            i += 1
        for item in split_top(clean[m.end():i - 1]):
            t = item.strip().strip("`\"")
            mm = re.match(NAME, t)
            if not mm or not t:
                continue
            if mm.group(1).lower() in KEYWORDS and not re.match(r"[`\"]", t):
                continue
            found.append((table, mm.group(1), path))
    for m in ALTER.finditer(clean):
        table = m.group(2).lower()
        for a in ADD.finditer(m.group(3)):
            if a.group(1).lower() in KEYWORDS | {"column"}:
                continue
            found.append((table, a.group(1), path))
    if path.endswith(".cs"):
        for m in EF_ADD.finditer(text):
            found.append((m.group(2).lower(), m.group(1), path))
        for t in EF_TABLE.finditer(text):
            tail = text[t.end():t.end() + 8000]
            end = tail.find("constraints:")
            for c in re.finditer(r'(\w+)\s*=\s*table\.Column<', tail[:end if end > 0 else len(tail)]):
                found.append((t.group(1).lower(), c.group(1), path))
    return found


def scan_repo(root):
    files = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=True).stdout.split("\n")
    found = []
    for f in files:
        if not f or SRC_SKIP.search(f):
            continue
        p = root / f
        try:
            if p.stat().st_size > 2_000_000:
                continue
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        if f.endswith(".prisma"):
            for m in PRISMA_MODEL.finditer(text):
                tm = re.search(r'@@map\("(\w+)"\)', m.group(2))
                table = (tm.group(1) if tm else m.group(1)).lower()
                for ln in m.group(2).splitlines():
                    mm = re.match(r"\s*(\w+)\s+\w+", ln)
                    if mm and not ln.strip().startswith(("@@", "//")):
                        cm = re.search(r'@map\("(\w+)"\)', ln)
                        found.append((table, cm.group(1) if cm else mm.group(1), f))
        elif re.search(r"CREATE\s+(?:UNLOGGED\s+|TEMP\w*\s+)?TABLE|ALTER\s+TABLE|CreateTable\(|AddColumn<", text, re.I):
            found += scan_text(text, f)
    return found


def load_allow(root):
    f = root / ".dedup-allow"
    entries, errs = [], []
    if not f.exists():
        return entries, errs
    for n, ln in enumerate(f.read_text().splitlines(), 1):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        spec, _, reason = ln.partition("#")
        spec = spec.strip().lower()
        if "." not in spec or not reason.strip():
            errs.append(f".dedup-allow:{n}: need `table.column  # reason` (a reason is mandatory)")
            continue
        entries.append((spec, reason.strip(), n))
    return entries, errs


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = Path(args[0] if args else ".").resolve()
    entries, errs = load_allow(root)
    if errs:
        print("\n".join(errs))
        return 2
    used = set()
    bad = []
    seen = set()
    for table, col, where in scan_repo(root):
        if not is_identity(col, table) or (table, col.lower()) in seen:
            continue
        seen.add((table, col.lower()))
        key = f"{table}.{col.lower()}"
        hit = [e for e in entries if fnmatch.fnmatchcase(key, e[0])]
        if hit:
            used.update(e[2] for e in hit)
        else:
            bad.append((key, where))
    stale = [e for e in entries if e[2] not in used]
    for e in stale:
        print(f"warning: .dedup-allow:{e[2]}: `{e[0]}` matches no table/column (stale)")
    for key, where in sorted(bad):
        print(f"{where}: {key} stores player identity. A console adapter reads it from the account core; "
              f"if it is game data or a per-network field, add `{key}  # reason` to .dedup-allow")
    if bad:
        print(f"dedup-lint: {len(bad)} column(s) not allowed")
        return 1
    if stale and "--strict-stale" in sys.argv:
        return 1
    print(f"dedup-lint: ok ({len(seen)} identity-looking column(s) allowed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
