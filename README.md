# promptly-prompt

A Claude Code skill that forces AI to **understand before executing**.

> AI answer quality depends on context quality, not prompt decoration.

## What It Does

A `UserPromptSubmit` hook that automatically intercepts complex requests and injects three disciplines:

1. **AI Capability Boundaries** — Forces AI to state what it can and can't do for this specific task, what context it's missing, and what biases it has in this domain.
2. **Requirement Understanding** — Forces AI to deeply understand your request, surface implicit needs (audience, downstream use, unstated constraints, failure modes), flag ambiguities, and wait for your confirmation before executing.
3. **Method Search** — Forces AI to search for existing methodologies, frameworks, open-source projects, and proven patterns before building from scratch. Use tools to search, give specific names, not vague suggestions.

Simple commands (`git status`, `read file.py`, `/commit`) pass through untouched.

## Why

When your brain is foggy, you write bad prompts, get bad answers, and spiral. This hook acts as a guardrail — it forces AI to pause, think, and confirm understanding before diving in. The core insight: most bad AI answers come from missing context, not missing prompt tricks.

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

| Signal | Effect |
|--------|--------|
| Long text (>80 words) | +complex |
| Multiple sentences | +complex |
| Multi-step words ("then", "after that", "然后", "接着") | +complex |
| Ambiguity words ("maybe", "probably", "大概", "可能") | +complex |
| Code blocks / file paths | -complex |
| Imperative verbs ("fix", "run", "git") | -complex |
| Very short (<10 chars) | -complex |

Score >= 3 triggers injection. Below 3 passes through silently.

No API calls. No dependencies beyond Python stdlib. Runs in < 50ms.

## Origin

Inspired by [promptly-prompt](https://www.promptly-prompt.com/), a prompt optimization project built during sophomore year. The original vision was a full prompt optimization pipeline — this skill distills the core insight: **understand first, find existing methods, then act**.

From prompt engineering to context engineering.

## License

MIT
