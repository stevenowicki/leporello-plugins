# What you need to run this skill

This skill builds broadcast graphics on your computer, checks them against the
Leporello design standards, and uploads them. A few base tools have to be on your
machine first — and a few it installs for you. This page is the full list.

> **Quick start:** run `scripts/check_deps.sh`. It tells you exactly what (if
> anything) is missing and installs the rest. The skill runs this for you on first
> use; you only need this page if it reports something missing.

## You install these (one time)

These are standard developer tools. They can't be installed automatically — they're
the foundation everything else runs on. Install them, then reopen your terminal.

| Tool | Why the skill needs it | How to get it |
|---|---|---|
| **Node.js** (LTS) | Renders your graphic and runs the design checks; packages the file. | Download the **LTS** installer from **https://nodejs.org** and run it. (This also gives you `npx`.) |
| **Python 3** (3.10+) | Validates the bundle's structure and checks it only uses approved design tokens. | Download from **https://www.python.org/downloads/** and run it. On macOS you can instead use Homebrew: `brew install python`. |

That's it for manual installs on **macOS or Linux**.

### Windows

This skill's helper scripts expect a Unix-style shell (they use `bash`, `zip`,
`unzip`). The simplest path on Windows is to run the skill inside **WSL** (Windows
Subsystem for Linux) or **Git Bash**, then install Node.js and Python *inside* that
environment. Native Windows (PowerShell/CMD) is a known gap — flag it if that's your
setup and we'll prioritize it.

## The skill installs these for you

You don't need to do anything for these — `check_deps.sh` handles them:

- **Playwright + a Chromium browser engine** — used to *render* your graphic and check
  the things a producer shouldn't have to catch by eye: that the type is in our
  typeface, that nothing important sits where the presenter stands, that there's no
  on-frame source line, that the headline is broadcast-big. First run downloads the
  browser (a few hundred MB); after that it's instant.
- **`serve`** (for local preview) and **`zip`/`unzip` usage** are run on demand.

## Two different machines — don't confuse them

- **The authoring machine** (this one) — where you run Claude + this skill to *build*
  content. It needs the tools above.
- **The on-air touchscreen** — where a presenter *displays* content during a show. It
  only needs a browser pointed at Leporello; it does **not** need Node, Python, or any
  of this. Building and presenting are separate machines.

## If something's wrong

Run `scripts/check_deps.sh` and read its output — every line is either `[ok]` or
`[MISS]` with the exact fix. If a check still fails after installing, reopen your
terminal (so it picks up the newly installed tools) and run it again.
