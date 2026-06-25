# Cross-harness adaptation (Claude Code / Codex / Gemini CLI / Copilot CLI)

> AIDD's **package structure is harness-agnostic**: Claude Code / ZCode / Gemini CLI / Codex all use this skill format of "one subdirectory + `SKILL.md` (with `name`/`description` frontmatter)," as a single skill subdirectory (`aidd/`, carrying its own `references/`). **Copilot CLI (1.0.63) was found by actual testing to lack this skills mechanism** and needs separate adaptation — see "Tested status" below.
> Only three things differ: **which directory to install into, how to invoke, and which tool name to use for read/write/run commands**. This page spells it out once. The methodology body always "states the action" (read/write/run/search); map the tool name to your harness via this table.

---

## 0. Tested status (2026-06-23)

The table below is the **result of actually installing and running**, not a paper inference:

| harness | version | install | discover | route | execute |
|---------|------|------|------|------|------|
| Claude Code (native · real project) | — | ✅ | ✅ | ✅ | ✅ |
| ZCode (Claude-family desktop) | 3.1.3 | ✅ | ✅ | ✅ | ✅ |
| Gemini CLI (Google · cross-vendor) | 0.47 | ✅ | ✅ | ✅ | ✅ |
| Codex (OpenAI · cross-vendor) | 0.140 | ✅ | ✅ | ✅ | ✅ |
| Copilot CLI (GitHub) | 1.0.63 | ❌ no skills mechanism | — | — | — |

- **Gemini**: `gemini skills install https://github.com/<owner>/<repo>` (without `--path` it discovers all skills in the repo and installs them all at once), installs to `~/.gemini/skills/`. The free OAuth personal tier has been retired by Google (it prompts migration to Antigravity) → use AI Studio's `GEMINI_API_KEY`.
- **Codex**: user skills go in `$CODEX_HOME/skills/<name>` (default `~/.codex/skills/`), as siblings of the built-in `.system`; **restart Codex after installing**. You can also have its bundled skill-installer install from GitHub: `install-skill-from-github.py --repo <owner>/<repo> --path aidd`.
- **Copilot CLI 1.0.63**: the commands are only `login/mcp/plugin/init/config…`, with no skills concept; aidd's SKILL.md can't be installed; to use it you'd have to go via `AGENTS.md`/MCP/plugin adaptation.
- Conclusion: the SKILL.md skill mechanism is common to and tested-working on **Claude Code / ZCode / Gemini / Codex** (including the two cross-vendor ones, Gemini and Codex); **Copilot is currently incompatible**.

---

## 1. Where to install + how to invoke

| harness | skills directory | invocation | instruction file (this package doesn't depend on it) |
|---------|------------|----------|----------------------|
| **Claude Code** | `.claude/skills/` (project) or `~/.claude/skills/` (user) | the `Skill` tool | `CLAUDE.md` |
| **Codex** | `~/.codex/skills/` **or** `~/.agents/skills/` | native loading, goes straight by SKILL.md (no explicit invocation tool) | `AGENTS.md` |
| **Gemini CLI** | `~/.gemini/skills/` **or** `~/.agents/skills/` | the `activate_skill` tool | `GEMINI.md` |
| **Copilot CLI** | — (1.0.63 has no skills mechanism) | doesn't support SKILL.md; go via `AGENTS.md`/MCP/plugin adaptation | `AGENTS.md` |

> **Shared path**: `~/.agents/skills/` is, per the docs, a cross-runtime shared path for Codex/Gemini etc.; but this round of testing used each harness's own `~/.<harness>/skills/` (`~/.codex/skills/`, `~/.gemini/skills/`, `~/.zcode/skills/`, all valid). Claude Code uses `.claude/skills/`. **Copilot 1.0.63 has no skills mechanism and doesn't apply** (see "Tested status" above).
> Install the **single `aidd/` folder** — its `references/` (methodology, scripts, templates, examples) travel with it; nothing else to place.

---

## 2. Tool-name mapping (methodology "states the action" → each harness's tool)

| action | Claude Code | Codex | Gemini CLI |
|------|-------------|-------|-----------|
| read file | `Read` | `shell` (`cat`/`head`) | `read_file` / `read_many_files` |
| write new file | `Write` | `apply_patch` | `write_file` |
| edit file | `Edit` | `apply_patch` | `replace` |
| run command | `Bash` | `shell` | `run_shell_command` |
| search content | `Grep` | `shell` (`grep`/`rg`) | `grep_search` |
| find file | `Glob` | `shell` (`find`/`ls`) | `glob` / `list_directory` |
| spawn sub-agent | `Agent` | `spawn_agent` (needs `multi_agent=true`) | `invoke_agent` (`@generalist`) |
| task tracking | `TodoWrite` | `update_plan` | `write_todos` |

The validator scripts are pure command-line driven by `argv` (`python …/config_check.py …`), **independent of the harness** — any environment that can run a shell uses them the same way, as long as Python is present.

---

## 3. Two harness-related pitfalls (already generalized in the methodology/quick-ref, here are the concrete specifics)

### Tool-call format
Different harnesses have different function-call block syntax, and **using the wrong one silently doesn't execute** (file not written, command not run, yet you think it's done). Check the format your harness requires before sending:
- **Claude Code**: must carry the `antml:` namespace prefix (written as a bare `invoke`/`parameter` → "tool call was malformed", silently discarded).
- **Codex / Gemini**: per their respective tool-call protocols; after calling, confirm the artifact actually landed on disk (`shell ls` / `read_file` to double-check), don't assume it took effect.

### Write files as UTF-8 without BOM
A Chinese file getting a BOM added / turning into UTF-16 makes downstream read garbled. Per-environment specifics:
- **Claude Code**: `Write`/`Edit` default to no BOM, use them directly; **don't** use bare PowerShell `Out-File`/`Set-Content` (adds a BOM). On Windows, if you must use PowerShell to write Chinese → `New-Object System.Text.UTF8Encoding $false`.
- **Codex (apply_patch) / Gemini (write_file)**: default UTF-8 without BOM, use directly.
- General baseline: **confirm UTF-8 without BOM before writing to disk**, use `/` paths cross-platform.

---

## 4. Instruction files (CLAUDE.md / AGENTS.md / GEMINI.md)

**AIDD neither creates nor depends on any harness's instruction file** — stuffing "create CLAUDE.md/AGENTS.md" into the methodology would bind it to a particular harness. This package requires only one **change ledger** (default project-root `CHANGELOG.md`, see the methodology's "Project-environment prerequisite"), unrelated to instruction files. So when switching harness you can **ignore the instruction-file column**; just install the single `aidd/` folder + have Python.
