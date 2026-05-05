# promptly-prompt

A Claude Code skill that forces AI to **understand before executing**.

> AI answer quality depends on context quality, not prompt decoration.

## What It Does

A `UserPromptSubmit` hook that automatically intercepts complex requests and injects two disciplines:

1. **Restate, then pause if needed** — Forces AI to echo your request in its own words, surface implicit constraints, and name what would make the answer wrong. If anything is ambiguous or the planned approach might not be what you wanted, AI stops and asks before acting. Trivial requests skip the restatement.
2. **Super-dimensional view** — Forces AI to step back before solving from memory: name the domain the problem belongs to, search for existing methodologies, frameworks, libraries, and prior art, then bring that specialist knowledge to bear. Cite specific names, not vague gestures. If nothing fits, say so and explain why.

Simple commands (`git status`, `read file.py`, `/commit`) pass through untouched.

## Why

When your brain is foggy, you write bad prompts, get bad answers, and spiral. This hook acts as a guardrail — it forces AI to pause, restate, search the relevant domain, and confirm direction before diving in. The core insight: most bad AI answers come from missing context and skipped prior art, not missing prompt tricks.

## Install

### Plugin marketplace (recommended)

In your terminal:

```bash
claude plugin marketplace add recomby-ai/promptly-prompt
claude plugin install promptly-prompt@promptly-prompt
```

Or inside a Claude Code session, prefix with `!`:

```
! claude plugin marketplace add recomby-ai/promptly-prompt
! claude plugin install promptly-prompt@promptly-prompt
```

### Uninstall

```bash
claude plugin uninstall promptly-prompt@promptly-prompt
```

### One-line install

```bash
git clone https://github.com/recomby-ai/promptly-prompt.git && cd promptly-prompt && bash install.sh
```

### Manual install

1. Copy skill files:

```bash
mkdir -p ~/.claude/skills/promptly-prompt/scripts
cp skill/SKILL.md ~/.claude/skills/promptly-prompt/
cp skill/scripts/intercept.py ~/.claude/skills/promptly-prompt/scripts/
```

2. Add hook to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/promptly-prompt/scripts/intercept.py"
          }
        ]
      }
    ]
  }
}
```

3. Start a new Claude Code session.

## How It Works

The hook script scores every prompt's complexity using rule-based signals:

| Signal | Score |
|--------|-------|
| Long text (>80 words / chars for Chinese) | +2 |
| Medium text (40–80 words) | +1 |
| Multiple sentences (>3) | +1 |
| Multi-step words — each match ("then", "然后", …), cap +3 | +2 each |
| Ambiguity words — each match ("maybe", "大概", …), cap +3 | +1 each |
| Multiple questions (>1 `?`) | +1 |
| Code blocks / file paths | −2 |
| Imperative verb at start ("fix", "run", "git") | −1 |
| Slash command (`/commit`) | −3 |
| Very short (<10 chars) | −3 |

Score ≥ 3 triggers injection. Below 3 passes through silently.

No API calls. No dependencies beyond Python stdlib. Runs in < 50ms.

## Origin

Inspired by [promptly-prompt](https://www.promptly-prompt.com/), a prompt optimization project built during sophomore year. The original vision was a full prompt optimization pipeline — this skill distills the core insight: **understand first, find existing methods, then act**.

From prompt engineering to context engineering.

## License

MIT
